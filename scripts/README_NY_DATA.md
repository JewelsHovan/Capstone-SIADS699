# New York Data Extractor

## Overview
`download_ny_data.py` downloads New York work zone and crash data from official public sources.

## Data Sources

### 1. Work Zone Data (WZDx Feed)
- **Source**: NY 511 Traffic Information
- **URL**: https://511ny.org/api/wzdx
- **Format**: WZDx v4.1 GeoJSON feed
- **Features**: ~800 active work zones with geographic coordinates
- **Update Frequency**: Real-time (feed updates regularly)

**Work Zone Fields Include:**
- Road names and directions
- Start/end dates
- Lane closure information
- Vehicle impact levels
- Worker presence indicators
- Geographic coordinates (LineString)
- Speed limit reductions

### 2. Crash Data (NY Open Data)
- **Source**: NY State Open Data Portal - Case Information
- **URL**: https://data.ny.gov/resource/e8ky-4vqe.json
- **Format**: JSON (Socrata API)
- **Records**: Millions of crash records from 2019+
- **Update Frequency**: Regularly updated by NY DMV

**Crash Fields Include:**
- Year, date, time, day of week
- Accident type (property damage, injury, fatal)
- Weather conditions
- Lighting conditions
- Road surface conditions
- Collision type
- County and municipality
- Number of vehicles involved
- Traffic control device

**Note**: NY crash data does **NOT** include geographic coordinates. Location is identified by:
- County name
- Municipality
- DOT reference marker (sometimes available)

## Usage

### Download Everything (Work Zones + Crashes)
```bash
python scripts/download_ny_data.py
```

### Download Work Zones Only
```bash
python scripts/download_ny_data.py --work-zones-only
```

### Download Crashes Only
```bash
# All available crash records (may take time)
python scripts/download_ny_data.py --crashes-only

# Limit to 10,000 records
python scripts/download_ny_data.py --crashes-only --crash-limit 10000

# Filter by specific years
python scripts/download_ny_data.py --crashes-only --years 2023 2024

# Combine filters
python scripts/download_ny_data.py --crashes-only --years 2023 2024 --crash-limit 50000
```

## Output Structure

```
data/
├── raw/
│   ├── ny_wzdx_feed.json              # Work zone feed (latest)
│   └── crashes/
│       ├── ny_crashes.csv             # Latest crash data (CSV)
│       ├── ny_crashes.json            # Latest crash data (JSON)
│       └── ny_crashes_YYYYMMDD_HHMMSS.csv  # Timestamped backup
└── processed/
    └── (integration outputs go here)
```

## Data Characteristics

### Work Zones
- **Count**: ~800 active work zones (as of Oct 2025)
- **Geographic Coverage**: Statewide New York
- **Geometry**: LineString coordinates (start/end points)
- **Completeness**: High quality with consistent WZDx schema

### Crashes
- **Volume**: Millions of records available (2019+)
- **Geographic Limitation**: **No lat/lon coordinates**
- **Location Granularity**: County + Municipality
- **Temporal Coverage**: Recent years (2019-2024+)
- **Completeness**: High - police-reported accidents

## Integration Considerations

### Work Zone + Crash Integration Challenges

Since NY crash data **lacks geographic coordinates**, direct spatial joins are not possible. Alternative approaches:

#### Option 1: County-Level Analysis
```python
# Group crashes by county
crashes_by_county = ny_crashes.groupby('county_name').size()

# Group work zones by county (requires extracting county from geometry)
wz_gdf = gpd.read_file('data/raw/ny_wzdx_feed.json')
# Use spatial join with NY county boundaries
```

#### Option 2: Municipality Matching
```python
# Match work zones to municipalities
# Requires NY municipality boundary shapefile
municipalities = gpd.read_file('ny_municipalities.shp')
wz_with_muni = gpd.sjoin(wz_gdf, municipalities)

# Join with crashes on municipality name
merged = crashes.merge(wz_with_muni,
                       left_on='municipality',
                       right_on='municipality_name')
```

#### Option 3: Use DOT Reference Markers (When Available)
```python
# Some crashes have dot_reference_marker_location
crashes_with_marker = crashes[crashes['dot_reference_marker_location'].notna()]
# Match to work zones near same markers
```

### Recommended Approach

For the MADS Capstone project, consider:

1. **Use Texas as primary state** (has coordinates for both work zones and crashes via TxDOT)
2. **Use NY for comparison/validation**:
   - County-level crash risk analysis
   - Temporal pattern analysis (time, day, weather)
   - Feature engineering (road conditions, weather, lighting)
3. **Document limitations** in project report

## Next Steps

### 1. Analyze Work Zone Data
```bash
python scripts/analyze_ny_feed.py
```

### 2. Explore Crash Data in Python
```python
import pandas as pd
import geopandas as gpd

# Load crashes
crashes = pd.read_csv('data/raw/crashes/ny_crashes.csv')

# Load work zones
wz = gpd.read_file('data/raw/ny_wzdx_feed.json')

# Explore
print(crashes['accident_descriptor'].value_counts())
print(crashes['county_name'].value_counts().head(10))
print(crashes['weather_conditions'].value_counts())
```

### 3. Obtain NY County Boundaries (for spatial join)
```python
# Option 1: Census TIGER/Line
import geopandas as gpd
url = "https://www2.census.gov/geo/tiger/TIGER2024/COUNTY/tl_2024_us_county.zip"
counties = gpd.read_file(url)
ny_counties = counties[counties['STATEFP'] == '36']  # NY state FIPS = 36

# Option 2: NY GIS Clearinghouse
# https://gis.ny.gov/
```

### 4. Feature Engineering for ML
```python
# From crashes
crash_features = [
    'weather_conditions',
    'lighting_conditions',
    'road_surface_conditions',
    'road_descriptor',
    'traffic_control_device',
    'time_of_day',  # derived from 'time'
    'day_of_week',
    'is_fatal',  # derived from 'accident_descriptor'
]

# From work zones
wz_features = [
    'vehicle_impact',
    'lanes_closed',
    'has_workers',
    'duration_days',  # derived from start/end dates
    'speed_reduction',
]
```

## API Limits and Performance

### Work Zone Feed
- No pagination needed (single API call)
- Fast download (~1 second)
- File size: ~1 MB

### Crash Data (Socrata API)
- Default limit: 50,000 records per request
- Pagination: Automatically handled by script
- Rate limits: Generally permissive for public use
- Full dataset download: May take several minutes
- **Recommendation**: Use `--crash-limit` and `--years` filters for faster testing

## Troubleshooting

### Work Zone Download Fails
```bash
# Test URL directly
curl -I https://511ny.org/api/wzdx

# Check if firewall/proxy blocking
# Try from different network
```

### Crash API Rate Limiting
```python
# Add delays between batches (modify script)
import time
time.sleep(1)  # Add after each request
```

### Out of Memory (Large Crash Downloads)
```bash
# Download in chunks by year
python scripts/download_ny_data.py --crashes-only --years 2024
python scripts/download_ny_data.py --crashes-only --years 2023
# ... etc
```

## References

- **NY 511 API**: https://511ny.org/
- **WZDx Specification**: https://github.com/usdot-jpo-ode/wzdx
- **NY Open Data Portal**: https://data.ny.gov/
- **Crash Dataset**: https://data.ny.gov/Transportation/Case-Information-Beginning-2009/e8ky-4vqe
- **Socrata API Docs**: https://dev.socrata.com/
