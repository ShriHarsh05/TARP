"""
Automated data updater for DT-GCN project.
Checks for stale data and provides instructions for updating.
"""

from data_ingestion import DataManager
import sys

def main():
    print("="*70)
    print("DT-GCN DATA UPDATER")
    print("="*70)
    print("\nThis script checks if your data sources need updating.")
    print("Note: Most Indian government data requires manual download.\n")
    
    # Initialize DataManager (no API key needed for checking)
    dm = DataManager(api_key="dummy", data_gov_api_key=None)
    
    # Check for updates
    status = dm.check_for_updates()
    
    # Provide specific instructions for stale data
    needs_update = [source for source, stale in status.items() if stale]
    
    if not needs_update:
        print("✓ All data sources are up to date!")
        return 0
    
    print("\n" + "="*70)
    print("UPDATE INSTRUCTIONS")
    print("="*70)
    
    if 'ncrb_crime' in needs_update:
        print("\n📊 NCRB CRIME DATA")
        print("-" * 70)
        print("1. Visit: https://www.data.gov.in")
        print("2. Search: 'Crime in India 2023' (or latest year)")
        print("3. Download CSV file")
        print("4. Save as: cache/ncrb_crime_2023.csv")
        print("\nAlternative sources:")
        print("- NCRB Official: https://ncrb.gov.in/")
        print("- Open City: https://data.opencity.in/dataset/crime-in-india-2023")
    
    if 'traffic_accidents' in needs_update:
        print("\n🚗 TRAFFIC ACCIDENT DATA")
        print("-" * 70)
        print("1. Visit: https://www.data.gov.in")
        print("2. Search: 'State/UTs/City-wise Traffic Accidents'")
        print("3. Download CSV file")
        print("4. Save as: cache/traffic_accidents_india.csv")
    
    if 'sample_crime' in needs_update:
        print("\n📝 SAMPLE CRIME DATA")
        print("-" * 70)
        print("Run: python setup_indian_data.py")
        print("This will regenerate sample data for testing.")
    
    print("\n" + "="*70)
    print("AUTOMATIC UPDATES (If Available)")
    print("="*70)
    print("\nTo enable automatic downloads (when API is available):")
    print("1. Register at: https://data.gov.in")
    print("2. Get your API key")
    print("3. Set environment variable:")
    print("   export DATA_GOV_API_KEY='your_key_here'")
    print("\nOr pass it to DataManager:")
    print("   dm = DataManager(tomtom_key, data_gov_api_key='your_key')")
    
    print("\n" + "="*70)
    print(f"Total sources needing update: {len(needs_update)}")
    print("="*70)
    
    return len(needs_update)

if __name__ == "__main__":
    sys.exit(main())
