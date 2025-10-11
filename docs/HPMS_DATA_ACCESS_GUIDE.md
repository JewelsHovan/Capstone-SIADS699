# HPMS Traffic Data Access Guide

**Purpose**: Get traffic volume (AADT) data for work zone locations
**Date**: October 10, 2025

---

## What is HPMS?

**Highway Performance Monitoring System (HPMS)** is a national database maintained by FHWA containing:
- Annual Average Daily Traffic (AADT) - vehicles per day
- Truck percentages (single unit and combination trucks)
- Vehicle classification
- Road characteristics (lanes, functional class, etc.)
- All Federal-Aid highways across the US

**Critical for your project**: AADT is essential for normalizing crash risk (crashes per million vehicle-miles traveled).

---

## Method 1: FHWA Official Shapefiles (RECOMMENDED)

### Access Point
**URL**: https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm

### What's Available
- **Format**: Shapefiles (GIS format)
- **Coverage**: All 50 states + DC + Puerto Rico
- **Most Recent**: 2018 data (as of the page)
- **Fields**: AADT, AADT_COMBINATION, AADT_SINGLE_UNIT, plus 60+ other road attributes

### Download Steps

**For California**:
1. Go to https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm
2. Find "California" in the state table
3. Click the "Feature Server" link
4. Options:
   - **Option A**: Use ArcGIS REST API to query/download
   - **Option B**: Open in QGIS and export as shapefile
   - **Option C**: Use Python to download (see script below)

**For Texas**:
- Same process, find "Texas" row

**For New York**:
- Same process, find "New York" row

---

## Method 2: Data.gov Portal

### Access Point
**URL**: https://catalog.data.gov/dataset/highway-performance-monitoring-system-hpms-b7a2f

### What's Available
- National HPMS dataset
- Can filter by state
- Multiple export formats: CSV, JSON, Shapefile

### Download Steps
1. Visit https://catalog.data.gov/dataset/highway-performance-monitoring-system-hpms-b7a2f
2. Click "Access & Use Information" or "Download"
3. Select format (Shapefile for GIS, CSV for tabular)
4. Apply filters:
   - State: California, Texas, or New York
   - Year: Most recent available
5. Export filtered data

---

## Method 3: State DOT Direct Sources (ALTERNATIVE)

Often state DOTs have more recent and detailed traffic count data than federal HPMS.

### California (Caltrans)
**URL**: https://dot.ca.gov/programs/traffic-operations/census

**What's Available**:
- Traffic volumes for all state highways
- More recent than federal HPMS (updated annually)
- Annual Average Daily Traffic (AADT)
- Peak hour volumes
- Truck percentages

**Access**:
- Interactive map: https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHhighway/Traffic_Volumes/MapServer
- Download: Available through ArcGIS REST services or contact Caltrans

**Contact**: Traffic Data Branch - traffic_ops@dot.ca.gov

---

### Texas (TxDOT)
**URL**: https://www.txdot.gov/data-maps/traffic-counts.html

**What's Available**:
- Statewide traffic counts
- Interactive map
- Download options for traffic count data

**Access**:
- Interactive Map: https://txdot.maps.arcgis.com/apps/webappviewer/index.html?id=...
- Data requests: TPP-TrafficData@txdot.gov

---

### New York (NYSDOT)
**URL**: https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/traffic-data-viewer

**What's Available**:
- Traffic counts for all state roads
- AADT data
- Traffic Data Viewer (GIS application)

**Access**:
- Traffic Data Viewer (online map tool)
- Data requests: https://www.dot.ny.gov/tdv

---

## Method 4: Python Script to Download HPMS (EASIEST)

I'll create a Python script to automate HPMS download using the ArcGIS REST API.

### Prerequisites
```bash
pip install geopandas requests arcgis pandas
```

### Python Script

Save this as `scripts/download_hpms_data.py`:

```python
"""
Download HPMS Traffic Data from FHWA Feature Servers
Fetches AADT (traffic volume) data for California, Texas, New York
"""

import geopandas as gpd
import requests
import json
import os
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

def download_hpms_by_state(state_name, output_dir='data/raw/hpms'):
    """
    Download HPMS data for a specific state

    Parameters:
    -----------
    state_name : str
        State name (e.g., 'California', 'Texas', 'New York')
    output_dir : str
        Directory to save output files
    """

    # State FIPS codes for filtering
    state_fips = {
        'California': '06',
        'Texas': '48',
        'New York': '36',
        'Alabama': '01',
        'Alaska': '02',
        # Add more as needed
    }

    if state_name not in state_fips:
        print(f"Error: {state_name} not in state FIPS mapping")
        return None

    print(f"\nDownloading HPMS data for {state_name}...")

    # FHWA HPMS Feature Server URL (2018 data - most recent public release)
    # Note: URLs change by year, check https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm

    base_url = "https://geo.dot.gov/server/rest/services/Hosted/HPMS_2018/FeatureServer/0"

    # Alternative: Try state-specific endpoints
    # Example for California
    state_urls = {
        'California': 'https://geo.dot.gov/server/rest/services/Hosted/Highway_Performance_Monitoring_System_2018_California/FeatureServer/0',
        # Add others as found
    }

    url = state_urls.get(state_name, base_url)

    try:
        # Method 1: Use arcgis library
        print(f"Connecting to {url}...")

        # Connect to feature layer
        feature_layer = FeatureLayer(url)

        # Query for state data
        where_clause = f"STATE_CODE = '{state_fips[state_name]}'"

        # Query features (may need pagination for large states)
        print(f"Querying with: {where_clause}")
        feature_set = feature_layer.query(where=where_clause, out_fields='*')

        # Convert to GeoDataFrame
        gdf = feature_set.sdf

        print(f"✓ Downloaded {len(gdf):,} road segments")

        # Save to file
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{state_name.lower()}_hpms_2018.gpkg')

        gdf.to_file(output_file, driver='GPKG')
        print(f"✓ Saved to {output_file}")

        # Print summary
        print(f"\nData Summary:")
        print(f"  Total segments: {len(gdf):,}")
        if 'AADT' in gdf.columns:
            print(f"  AADT range: {gdf['AADT'].min():,.0f} - {gdf['AADT'].max():,.0f}")
            print(f"  Mean AADT: {gdf['AADT'].mean():,.0f}")

        return gdf

    except Exception as e:
        print(f"Error downloading via arcgis library: {e}")
        print("\nTrying alternative method...")

        # Method 2: Direct REST API query
        return download_via_rest_api(url, state_name, state_fips[state_name], output_dir)

def download_via_rest_api(url, state_name, state_fips, output_dir):
    """
    Download via direct REST API calls (more reliable, no authentication needed)
    """

    # Query parameters
    params = {
        'where': f"STATE_CODE = '{state_fips}'",
        'outFields': '*',
        'returnGeometry': 'true',
        'f': 'geojson',
        'resultRecordCount': 1000  # Max per request
    }

    all_features = []
    offset = 0

    print(f"Downloading in batches...")

    while True:
        params['resultOffset'] = offset

        response = requests.get(f"{url}/query", params=params, timeout=60)

        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            break

        data = response.json()

        if 'features' not in data or len(data['features']) == 0:
            break

        all_features.extend(data['features'])
        print(f"  Downloaded {len(all_features):,} segments so far...")

        offset += 1000

        # Safety limit
        if offset > 100000:
            print("Reached safety limit")
            break

    if len(all_features) == 0:
        print("No features downloaded")
        return None

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(all_features, crs='EPSG:4326')

    # Save
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{state_name.lower()}_hpms_2018.gpkg')

    gdf.to_file(output_file, driver='GPKG')
    print(f"✓ Saved {len(gdf):,} segments to {output_file}")

    return gdf

def main():
    """Download HPMS data for all target states"""

    states = ['California', 'Texas', 'New York']

    for state in states:
        try:
            gdf = download_hpms_by_state(state)
            if gdf is not None:
                print(f"✓ {state} complete\n")
        except Exception as e:
            print(f"✗ {state} failed: {e}\n")

    print("="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Load HPMS data: gdf = gpd.read_file('data/raw/hpms/california_hpms_2018.gpkg')")
    print("2. Spatial join with work zones to get AADT for each work zone")
    print("3. Use AADT as feature in ML model")

if __name__ == "__main__":
    main()
```

### Run the Script
```bash
cd /Users/julienh/Desktop/MADS/Capstone
python scripts/download_hpms_data.py
```

---

## Method 5: Manual Download (If Scripts Fail)

### Step-by-Step for California

1. **Visit FHWA Shapefiles Page**:
   https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm

2. **Find California Row**, click "Feature Server" link

3. **Copy the Feature Server URL** (something like):
   `https://geo.dot.gov/server/rest/services/.../FeatureServer/0`

4. **Use QGIS** (free GIS software):
   - Download QGIS: https://qgis.org/download/
   - Open QGIS
   - Layer → Add Layer → Add ArcGIS REST Server Layer
   - Paste the Feature Server URL
   - Click "Add"
   - Right-click layer → Export → Save Features As
   - Format: GeoPackage or Shapefile
   - Save to: `data/raw/hpms/california_hpms.gpkg`

5. **Repeat for Texas and New York**

---

## What Data Fields to Extract

### Critical Fields for Your Project

| Field Name | Description | Why You Need It |
|-----------|-------------|-----------------|
| **AADT** | Annual Average Daily Traffic | **PRIMARY**: Exposure metric for crash rate |
| **AADT_COMBINATION** | Average daily combination trucks | Truck involvement in crashes |
| **AADT_SINGLE_UNIT** | Average daily single-unit trucks | Heavy vehicle exposure |
| **STATE_CODE** | State FIPS code | Filter by state |
| **ROUTE_ID** | Route identifier | Match to work zone road names |
| **ROUTE_NUMBER** | Route number (e.g., I-80, US-101) | Match to work zones |
| **F_SYSTEM** | Functional system (1=Interstate, 2=Other freeways, etc.) | Road classification |
| **THROUGH_LANES** | Number of through lanes | Road capacity |
| **SPEED_LIMIT** | Posted speed limit | Baseline speed |
| **URBAN_CODE** | Urban area code | Urban vs rural |
| **geometry** | Road segment geometry (LineString) | Spatial join |

### Field Descriptions Reference
Full field manual: https://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/

---

## How to Use HPMS Data in Your Project

### Step 1: Load HPMS Data
```python
import geopandas as gpd

# Load California HPMS
ca_hpms = gpd.read_file('data/raw/hpms/california_hpms_2018.gpkg')

# Check columns
print(ca_hpms.columns)
print(f"Loaded {len(ca_hpms):,} road segments")
```

### Step 2: Spatial Join with Work Zones
```python
# Load your work zones
work_zones = gpd.read_file('data/processed/ca_work_zones_analysis.csv')
work_zones_gdf = gpd.GeoDataFrame(
    work_zones,
    geometry=gpd.points_from_xy(work_zones.longitude, work_zones.latitude),
    crs='EPSG:4326'
)

# Buffer work zones (e.g., 50 meters)
work_zones_gdf['geometry'] = work_zones_gdf.geometry.buffer(0.0005)  # ~50m in degrees

# Spatial join
work_zones_with_aadt = gpd.sjoin_nearest(
    work_zones_gdf,
    ca_hpms[['AADT', 'AADT_COMBINATION', 'THROUGH_LANES', 'SPEED_LIMIT', 'geometry']],
    how='left',
    max_distance=100  # meters
)

print(f"✓ Matched {work_zones_with_aadt['AADT'].notna().sum()} work zones to AADT data")
```

### Step 3: Use as ML Features
```python
# Add to your feature matrix
features_df['aadt'] = work_zones_with_aadt['AADT']
features_df['truck_pct'] = (
    work_zones_with_aadt['AADT_COMBINATION'] / work_zones_with_aadt['AADT'] * 100
)
features_df['lanes'] = work_zones_with_aadt['THROUGH_LANES']
features_df['speed_limit'] = work_zones_with_aadt['SPEED_LIMIT']

# Calculate crash rate (if you have crash counts)
features_df['crash_rate'] = (
    features_df['crash_count'] /
    (features_df['aadt'] * features_df['duration_days'] / 365.25 / 1000000)
)  # Crashes per million vehicle-days
```

---

## Troubleshooting

### Problem: Feature Server URLs Don't Work

**Solution**: URLs change annually. Check the latest:
1. Go to https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm
2. Look for most recent year (2019, 2020, 2021, etc.)
3. Update URLs in script

### Problem: Download Times Out

**Solution**: Large states (CA, TX) have many road segments
1. Download in smaller chunks (use bounding box filter)
2. Or use state DOT sources (often faster)

### Problem: Can't Match Work Zones to Roads

**Solution**: Road name matching is tricky
1. Use spatial join (nearest neighbor) instead of name matching
2. Buffer work zone points (50-100 meters)
3. Join to nearest HPMS segment
4. Validate: Check if matched road names make sense

### Problem: AADT Data Missing for Some Roads

**Solution**: HPMS only covers Federal-Aid highways
1. Local roads may not have AADT
2. Use state DOT data for local roads (more complete)
3. Or impute AADT based on road functional class averages

---

## Alternative: Use OpenStreetMap for Traffic Estimates

If HPMS is too difficult, OSM has traffic indicators:

```python
import osmnx as ox

# Download road network for Bay Area
G = ox.graph_from_place("Alameda County, California", network_type='drive')

# Get road attributes (lanes, maxspeed, highway type)
edges = ox.graph_to_gdfs(G, nodes=False)

# Estimate AADT based on road type (rough proxy)
aadt_estimates = {
    'motorway': 50000,
    'trunk': 30000,
    'primary': 15000,
    'secondary': 5000,
    'tertiary': 2000,
    'residential': 500
}

edges['aadt_estimate'] = edges['highway'].map(aadt_estimates)
```

**Note**: OSM estimates are ROUGH. HPMS is much better if available.

---

## Expected File Sizes

- **California HPMS**: ~50-100 MB (30,000-50,000 road segments)
- **Texas HPMS**: ~150-200 MB (larger state, more roads)
- **New York HPMS**: ~40-80 MB

**Storage needed**: ~500 MB for all three states

---

## Data Freshness

**Important**: HPMS has 2-year lag
- 2024 data → submitted by states in 2025 → published in 2026
- Most recent public data is typically 2018-2020

**For your project**: 2018 HPMS is fine! AADT doesn't change dramatically year-to-year. Your crash data is 2023-2025, so 2018 AADT is a reasonable approximation.

---

## Contact Information

If all else fails, contact FHWA directly:

**HPMS Program Manager**:
- Name: Thomas Roff
- Email: thomas.roff@dot.gov
- Phone: (202) 366-5035

**General HPMS Questions**:
- Email: PolicyInfoFeedback@dot.gov

**Request**: "I'm a graduate student working on work zone safety research. Could you provide download links for California, Texas, and New York HPMS shapefiles (most recent available year)? Specifically need AADT fields."

---

## Summary: Recommended Approach

**For Your Capstone (Easiest Path)**:

1. **Try Python script first** (Method 4)
   - Run `scripts/download_hpms_data.py`
   - Should work for 2018 data
   - 30 minutes to download all three states

2. **If script fails, use QGIS** (Method 5)
   - Manual but reliable
   - 1 hour for all three states

3. **If HPMS unavailable, use State DOTs** (Method 3)
   - California: https://dot.ca.gov/programs/traffic-operations/census
   - Texas: https://www.txdot.gov/data-maps/traffic-counts.html
   - New York: https://www.dot.ny.gov/tdv

4. **Last resort: OSM estimates**
   - Not ideal but better than nothing
   - Takes 10 minutes

**Timeline**: Budget 1-2 days to get HPMS data integrated into your project.

---

**Next Steps**:
1. Try the Python download script
2. If successful, spatial join with work zones
3. Add AADT as feature in your ML model
4. Calculate crash rates (crashes per million vehicle-miles)

Good luck! Let me know if you hit any issues.
