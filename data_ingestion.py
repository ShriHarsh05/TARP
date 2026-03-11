import pandas as pd
import requests
import os
from datetime import datetime

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
        
    def download_ncrb_crime_data(self, year=2021, use_cache=True):
        """
        Download NCRB crime data from data.gov.in or use cached version.
        
        Args:
            year: Year of crime data (2021, 2022, 2023)
            use_cache: Whether to use cached data if available
            
        Returns:
            DataFrame with Indian crime statistics
        """
        cache_file = f"{self.cache_dir}/ncrb_crime_{year}.csv"
        
        if use_cache and os.path.exists(cache_file):
            print(f"Loading cached NCRB data from {cache_file}")
            return pd.read_csv(cache_file)
        
        # Data.gov.in resource IDs for NCRB data
        resource_urls = {
            2021: "https://www.data.gov.in/catalog/crime-india-2021",
            2022: "https://www.data.gov.in/catalog/crime-india-2022",
            2023: "https://www.data.gov.in/catalog/crime-india-2023"
        }
        
        print(f"Note: NCRB data for {year} needs to be manually downloaded from:")
        print(f"  {resource_urls.get(year, 'https://www.data.gov.in')}")
        print(f"  Save it as: {cache_file}")
        print(f"  Then run again with use_cache=True")
        
        return None
    
    def download_traffic_accident_data(self, state=None, use_cache=True):
        """
        Download traffic accident data from data.gov.in.
        
        Args:
            state: Specific state name (e.g., 'Tamil Nadu', 'Delhi')
            use_cache: Whether to use cached data
            
        Returns:
            DataFrame with traffic accident statistics
        """
        cache_file = f"{self.cache_dir}/traffic_accidents_india.csv"
        
        if use_cache and os.path.exists(cache_file):
            print(f"Loading cached traffic accident data from {cache_file}")
            df = pd.read_csv(cache_file)
            if state:
                df = df[df['State'].str.contains(state, case=False, na=False)]
            return df
        
        print("Note: Traffic accident data needs to be downloaded from:")
        print("  https://www.data.gov.in/resource/stateutscity-wise-number-cases-reported-and-persons-injured-died-due-traffic-accidents")
        print(f"  Save it as: {cache_file}")
        
        return None

    def get_live_traffic(self, lat, lon):
        """
        Get real-time traffic speed from TomTom API.
        
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
    
    def load_local_crime_data(self, filepath):
        """
        Load crime data from local CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with crime data
        """
        if os.path.exists(filepath):
            print(f"Loading local crime data from {filepath}")
            return pd.read_csv(filepath)
        else:
            print(f"File not found: {filepath}")
            return None
