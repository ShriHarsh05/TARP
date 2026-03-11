import pandas as pd
import requests
import os
from datetime import datetime, timedelta
import json

class DataManager:
    def __init__(self, api_key, data_gov_api_key=None):
        """
        Initialize DataManager with API keys.
        
        Args:
            api_key: TomTom API key for real-time traffic
            data_gov_api_key: Optional data.gov.in API key for government datasets
        """
        self.api_key = api_key
        self.data_gov_api_key = data_gov_api_key
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        self.metadata_file = f"{self.cache_dir}/data_metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata about cached data files."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata about cached data files."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _is_data_stale(self, cache_key, max_age_days=30):
        """
        Check if cached data is older than max_age_days.
        
        Args:
            cache_key: Key to identify the cached data
            max_age_days: Maximum age in days before data is considered stale
            
        Returns:
            True if data is stale or doesn't exist, False otherwise
        """
        if cache_key not in self.metadata:
            return True
        
        last_updated = datetime.fromisoformat(self.metadata[cache_key]['last_updated'])
        age = datetime.now() - last_updated
        
        return age.days > max_age_days
    
    def check_for_updates(self):
        """
        Check if any cached data needs updating.
        
        Returns:
            Dictionary with update status for each data source
        """
        status = {
            'ncrb_crime': self._is_data_stale('ncrb_crime', max_age_days=365),  # Annual data
            'traffic_accidents': self._is_data_stale('traffic_accidents', max_age_days=365),
            'sample_crime': self._is_data_stale('sample_crime', max_age_days=90)
        }
        
        print("\n" + "="*70)
        print("DATA FRESHNESS CHECK")
        print("="*70)
        
        for source, needs_update in status.items():
            status_icon = "⚠️  STALE" if needs_update else "✓ FRESH"
            print(f"{status_icon} - {source}")
            
            if source in self.metadata:
                last_update = self.metadata[source].get('last_updated', 'Unknown')
                print(f"         Last updated: {last_update}")
        
        print("="*70 + "\n")
        
        return status
    
    def download_ncrb_crime_data(self, year=None, use_cache=True, auto_check=True):
        """
        Download NCRB crime data with automatic freshness checking.
        
        Args:
            year: Year of crime data (defaults to latest available)
            use_cache: Whether to use cached data if available
            auto_check: Automatically check if data is stale
            
        Returns:
            DataFrame with Indian crime statistics or None
        """
        if year is None:
            year = datetime.now().year - 1  # Latest complete year
        
        cache_key = 'ncrb_crime'
        cache_file = f"{self.cache_dir}/ncrb_crime_{year}.csv"
        
        # Check if we have fresh cached data
        if use_cache and os.path.exists(cache_file):
            if auto_check and self._is_data_stale(cache_key, max_age_days=365):
                print(f"⚠️  Cached NCRB data is over 1 year old. Consider updating.")
            else:
                print(f"✓ Using cached NCRB data from {cache_file}")
            return pd.read_csv(cache_file)
        
        print(f"Attempting to download NCRB crime data for {year}...")
        
        # Try data.gov.in API if key is available
        if self.data_gov_api_key:
            try:
                # Note: Actual API endpoint may vary - check data.gov.in documentation
                api_url = f"https://api.data.gov.in/resource/crime-india-{year}"
                headers = {'api-key': self.data_gov_api_key}
                
                response = requests.get(api_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data.get('records', []))
                    
                    if not df.empty:
                        df.to_csv(cache_file, index=False)
                        self.metadata[cache_key] = {
                            'last_updated': datetime.now().isoformat(),
                            'source': f'data.gov.in API',
                            'year': year
                        }
                        self._save_metadata()
                        print(f"✓ Successfully downloaded NCRB data for {year}")
                        return df
            except Exception as e:
                print(f"⚠️  API download failed: {e}")
        
        # Fallback to manual instructions
        print("\n" + "="*70)
        print("MANUAL DOWNLOAD REQUIRED")
        print("="*70)
        print(f"NCRB crime data for {year} needs to be downloaded manually:")
        print(f"\n1. Visit: https://www.data.gov.in/catalog/crime-india-{year}")
        print(f"2. Click 'Download' and select CSV format")
        print(f"3. Save the file as: {cache_file}")
        print(f"4. Run this script again")
        print("="*70 + "\n")
        
        return None
    
    def download_traffic_accident_data(self, state=None, use_cache=True, auto_check=True):
        """
        Download traffic accident data with automatic freshness checking.
        
        Args:
            state: Specific state name (e.g., 'Tamil Nadu', 'Delhi')
            use_cache: Whether to use cached data
            auto_check: Automatically check if data is stale
            
        Returns:
            DataFrame with traffic accident statistics or None
        """
        cache_key = 'traffic_accidents'
        cache_file = f"{self.cache_dir}/traffic_accidents_india.csv"
        
        # Check if we have fresh cached data
        if use_cache and os.path.exists(cache_file):
            if auto_check and self._is_data_stale(cache_key, max_age_days=365):
                print(f"⚠️  Cached traffic accident data is over 1 year old. Consider updating.")
            else:
                print(f"✓ Using cached traffic accident data from {cache_file}")
            
            df = pd.read_csv(cache_file)
            if state:
                df = df[df['State'].str.contains(state, case=False, na=False)]
            return df
        
        print("Attempting to download traffic accident data...")
        
        # Try data.gov.in API if key is available
        if self.data_gov_api_key:
            try:
                api_url = "https://api.data.gov.in/resource/traffic-accidents"
                headers = {'api-key': self.data_gov_api_key}
                
                response = requests.get(api_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data.get('records', []))
                    
                    if not df.empty:
                        df.to_csv(cache_file, index=False)
                        self.metadata[cache_key] = {
                            'last_updated': datetime.now().isoformat(),
                            'source': 'data.gov.in API'
                        }
                        self._save_metadata()
                        print(f"✓ Successfully downloaded traffic accident data")
                        
                        if state:
                            df = df[df['State'].str.contains(state, case=False, na=False)]
                        return df
            except Exception as e:
                print(f"⚠️  API download failed: {e}")
        
        # Fallback to manual instructions
        print("\n" + "="*70)
        print("MANUAL DOWNLOAD REQUIRED")
        print("="*70)
        print("Traffic accident data needs to be downloaded manually:")
        print("\n1. Visit: https://www.data.gov.in")
        print("2. Search: 'State/UTs/City-wise Traffic Accidents'")
        print("3. Download the CSV file")
        print(f"4. Save as: {cache_file}")
        print("5. Run this script again")
        print("="*70 + "\n")
        
        return None

    def get_live_traffic(self, lat, lon):
        """
        Get real-time traffic speed from TomTom API.
        This always fetches the latest data.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Current speed in kmph
        """
        url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        params = {'key': self.api_key, 'point': f"{lat},{lon}", 'unit': 'kmph'}
        try:
            r = requests.get(url, params=params, timeout=5).json()
            return r['flowSegmentData']['currentSpeed']
        except Exception as e:
            print(f"Traffic API error: {e}")
            return 40.0  # Default free-flow speed fallback
    
    def get_delhi_transit_data(self, data_type='static'):
        """
        Placeholder for Delhi Open Transit Data integration.
        
        Args:
            data_type: 'static' or 'dynamic' transit data
            
        Returns:
            Transit data (requires API setup at otd.delhi.gov.in)
        """
        print("Delhi Open Transit Data requires registration at:")
        print("  https://otd.delhi.gov.in")
        print("  Contact: IIIT-Delhi for API access")
        
        return None
    
    def load_local_crime_data(self, filepath, auto_check=True):
        """
        Load crime data from local CSV file with freshness checking.
        
        Args:
            filepath: Path to CSV file
            auto_check: Check if file has been modified recently
            
        Returns:
            DataFrame with crime data
        """
        if os.path.exists(filepath):
            # Check file age
            if auto_check:
                file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(filepath))).days
                if file_age_days > 90:
                    print(f"⚠️  Warning: {filepath} is {file_age_days} days old. Consider updating.")
            
            print(f"Loading local crime data from {filepath}")
            return pd.read_csv(filepath)
        else:
            print(f"File not found: {filepath}")
            return None
