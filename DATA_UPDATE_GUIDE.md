# Automatic Data Update System

## Overview

Your DT-GCN project now includes an **automatic data freshness checking system** that:
- ✅ Always uses the latest real-time traffic data
- ✅ Tracks when crime data was last updated
- ✅ Warns you when data is stale
- ✅ Attempts automatic downloads (when API available)
- ✅ Provides clear manual update instructions

## How It Works

### 1. Real-Time Traffic Data (Always Latest)
**No action needed!** The TomTom API is called every time you run the project, ensuring you always have the most current traffic information.

```python
# This ALWAYS fetches latest data
speed = dm.get_live_traffic(lat, lon)
```

### 2. Crime Data (Smart Caching with Freshness Checks)

#### Automatic Freshness Tracking
The system maintains a metadata file (`cache/data_metadata.json`) that tracks:
- When each dataset was last downloaded
- The data source
- The version/year

#### Freshness Thresholds
- **NCRB Crime Data:** Warns if >365 days old (annual updates)
- **Traffic Accidents:** Warns if >365 days old (annual updates)
- **Sample Data:** Warns if >90 days old

## Usage

### Check for Updates
```bash
python update_data.py
```

**Output:**
```
======================================================================
DATA FRESHNESS CHECK
======================================================================
⚠️  STALE - ncrb_crime
         Last updated: 2023-03-10
✓ FRESH - traffic_accidents
         Last updated: 2024-01-15
⚠️  STALE - sample_crime
======================================================================
```

### Run with Automatic Checking
```bash
python main.py
```

The main pipeline now automatically:
1. Checks data freshness at startup
2. Warns if data is stale
3. Uses cached data if available
4. Fetches real-time traffic data

### Manual Data Update

When `update_data.py` indicates stale data, follow these steps:

#### For NCRB Crime Data:
```bash
# 1. Visit the website
https://www.data.gov.in

# 2. Search for latest year
"Crime in India 2024"

# 3. Download CSV

# 4. Save as
cache/ncrb_crime_2024.csv

# 5. Update your code
dm.download_ncrb_crime_data(year=2024)
```

#### For Traffic Accident Data:
```bash
# 1. Visit
https://www.data.gov.in

# 2. Search
"State/UTs/City-wise Traffic Accidents"

# 3. Download CSV

# 4. Save as
cache/traffic_accidents_india.csv
```

## Automatic Download (When Available)

If you have a data.gov.in API key:

```python
# Set API key
dm = DataManager(
    api_key="your_tomtom_key",
    data_gov_api_key="your_datagovin_key"
)

# Attempt automatic download
crime_data = dm.download_ncrb_crime_data(year=2024)
# If API works: Downloads automatically
# If API fails: Shows manual instructions
```

### Get data.gov.in API Key:
1. Register at https://data.gov.in
2. Navigate to API section
3. Request API key
4. Set environment variable:
   ```bash
   export DATA_GOV_API_KEY='your_key_here'
   ```

## Data Metadata File

**Location:** `cache/data_metadata.json`

**Example:**
```json
{
  "ncrb_crime": {
    "last_updated": "2024-03-10T10:30:00",
    "source": "data.gov.in API",
    "year": 2024
  },
  "traffic_accidents": {
    "last_updated": "2024-01-15T14:20:00",
    "source": "manual download"
  }
}
```

## Workflow Examples

### Scenario 1: First Time Setup
```bash
# 1. Check what's needed
python update_data.py
# Output: All data sources are STALE

# 2. Create sample data for testing
python setup_indian_data.py

# 3. Run the project
python main.py
# Uses sample data + real-time traffic
```

### Scenario 2: Regular Usage
```bash
# 1. Check for updates (monthly)
python update_data.py

# 2. If data is fresh, just run
python main.py

# 3. If data is stale, update manually
# (follow instructions from update_data.py)
```

### Scenario 3: Production Deployment
```bash
# 1. Set up data.gov.in API key
export DATA_GOV_API_KEY='your_key'

# 2. Run with automatic updates
python main.py
# Automatically downloads latest data if stale
```

## Benefits

### 1. Always Current Traffic Data
- Real-time API calls ensure traffic data is never stale
- No manual updates needed for traffic information

### 2. Smart Crime Data Management
- Automatic freshness checking
- Clear warnings when data is outdated
- Attempts automatic download when possible
- Falls back to clear manual instructions

### 3. Transparency
- Know exactly when your data was last updated
- Track data sources and versions
- Make informed decisions about data freshness

### 4. Flexibility
- Use cached data for faster processing
- Force updates when needed
- Mix automatic and manual updates

## Configuration Options

### Disable Automatic Checking
```python
# Don't check if data is stale
crime_data = dm.download_ncrb_crime_data(auto_check=False)
```

### Force Re-download
```python
# Ignore cache, force fresh download
crime_data = dm.download_ncrb_crime_data(use_cache=False)
```

### Custom Freshness Thresholds
```python
# Check if data is older than 180 days
is_stale = dm._is_data_stale('ncrb_crime', max_age_days=180)
```

## Troubleshooting

### "API download failed"
**Cause:** data.gov.in API key not set or invalid  
**Solution:** Use manual download or get valid API key

### "Data is stale"
**Cause:** Cached data is older than threshold  
**Solution:** Run `update_data.py` and follow instructions

### "File not found"
**Cause:** No cached data available  
**Solution:** Download data manually or run `setup_indian_data.py`

## Best Practices

1. **Check monthly:** Run `update_data.py` once a month
2. **Update annually:** Crime data is typically released annually
3. **Use sample data:** For testing and development
4. **Use real data:** For production and research
5. **Track versions:** Note which year of data you're using

## Summary

Your project now intelligently manages data freshness:
- ✅ **Traffic data:** Always latest (automatic)
- ✅ **Crime data:** Smart caching with freshness warnings
- ✅ **Metadata tracking:** Know when data was last updated
- ✅ **Automatic attempts:** Downloads when API available
- ✅ **Clear instructions:** Manual fallback when needed

**Result:** You always know if you're working with current data, and the system helps you keep it updated!
