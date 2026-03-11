"""
Helper script to set up Indian government data sources.

This script provides instructions and utilities for downloading
NCRB crime data and traffic accident data from data.gov.in
"""

import os
import pandas as pd

def setup_instructions():
    """Print setup instructions for Indian government data sources."""
    
    print("=" * 70)
    print("INDIAN GOVERNMENT DATA SETUP GUIDE")
    print("=" * 70)
    
    print("\n1. DATA.GOV.IN API KEY (Optional but recommended)")
    print("-" * 70)
    print("   Visit: https://data.gov.in")
    print("   - Click 'Register' and create an account")
    print("   - Navigate to 'API' section to get your API key")
    print("   - Store it in your environment or config file")
    
    print("\n2. NCRB CRIME DATA")
    print("-" * 70)
    print("   Download from: https://www.data.gov.in/catalog/crime-india-2021")
    print("   Or search: 'Crime in India 2021' on data.gov.in")
    print("   - Download the CSV file")
    print("   - Save as: cache/ncrb_crime_2021.csv")
    print("   - Available years: 2021, 2022, 2023")
    
    print("\n3. TRAFFIC ACCIDENT DATA")
    print("-" * 70)
    print("   Download from: https://www.data.gov.in")
    print("   Search: 'State/UTs/City-wise Traffic Accidents'")
    print("   - Download the CSV file")
    print("   - Save as: cache/traffic_accidents_india.csv")
    
    print("\n4. DELHI OPEN TRANSIT DATA (Optional - for Delhi region)")
    print("-" * 70)
    print("   Visit: https://otd.delhi.gov.in")
    print("   - Register for access")
    print("   - Accept terms and conditions")
    print("   - Download static/dynamic transit datasets")
    
    print("\n5. ALTERNATIVE: Use Sample Data")
    print("-" * 70)
    print("   If you can't access data.gov.in, you can:")
    print("   - Use the existing Kaggle dataset (already configured)")
    print("   - Or manually create sample Indian crime data")
    
    print("\n" + "=" * 70)
    print("After downloading, your cache/ folder should contain:")
    print("  - ncrb_crime_2021.csv")
    print("  - traffic_accidents_india.csv")
    print("=" * 70)

def create_sample_indian_data():
    """Create sample Indian crime data for testing."""
    
    print("\nCreating sample Indian crime data for testing...")
    
    # Sample data for major Indian cities
    sample_data = {
        'State': ['Tamil Nadu', 'Tamil Nadu', 'Delhi', 'Delhi', 'Maharashtra', 
                  'Maharashtra', 'Karnataka', 'Karnataka', 'West Bengal', 'West Bengal'],
        'City': ['Chennai', 'Vellore', 'New Delhi', 'Delhi', 'Mumbai', 
                 'Pune', 'Bangalore', 'Mysore', 'Kolkata', 'Howrah'],
        'Crime_Type': ['Theft', 'Robbery', 'Assault', 'Theft', 'Robbery',
                       'Assault', 'Theft', 'Robbery', 'Assault', 'Theft'],
        'Incidents': [1250, 340, 890, 1450, 2100, 780, 1680, 420, 1340, 560],
        'Year': [2021] * 10,
        'Latitude': [13.0827, 12.9165, 28.6139, 28.7041, 19.0760,
                     18.5204, 12.9716, 12.2958, 22.5726, 22.5958],
        'Longitude': [80.2707, 79.1325, 77.2090, 77.1025, 72.8777,
                      73.8567, 77.5946, 76.6394, 88.3639, 88.2636]
    }
    
    df = pd.DataFrame(sample_data)
    
    os.makedirs('cache', exist_ok=True)
    df.to_csv('cache/sample_indian_crime.csv', index=False)
    
    print("✓ Sample data created: cache/sample_indian_crime.csv")
    print(f"  Contains {len(df)} sample records for Indian cities")
    
    return df

def verify_setup():
    """Verify that data files are in place."""
    
    print("\nVerifying data setup...")
    
    cache_dir = 'cache'
    required_files = {
        'ncrb_crime_2021.csv': 'NCRB Crime Data',
        'traffic_accidents_india.csv': 'Traffic Accident Data',
        'sample_indian_crime.csv': 'Sample Indian Crime Data'
    }
    
    found = []
    missing = []
    
    for filename, description in required_files.items():
        filepath = os.path.join(cache_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            found.append(f"✓ {description}: {filename} ({size:,} bytes)")
        else:
            missing.append(f"✗ {description}: {filename}")
    
    if found:
        print("\nFound:")
        for item in found:
            print(f"  {item}")
    
    if missing:
        print("\nMissing:")
        for item in missing:
            print(f"  {item}")
    
    return len(missing) == 0

if __name__ == "__main__":
    setup_instructions()
    
    print("\n" + "=" * 70)
    response = input("\nCreate sample Indian crime data for testing? (y/n): ")
    
    if response.lower() == 'y':
        create_sample_indian_data()
    
    print("\n")
    verify_setup()
    
    print("\n" + "=" * 70)
    print("Setup complete! You can now use DataManager with Indian data.")
    print("=" * 70)
