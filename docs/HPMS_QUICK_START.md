# HPMS Data - Quick Start

## 🚀 Fastest Way to Get Traffic Volume Data

### Option 1: Run the Download Script (5 minutes)

```bash
# Install required libraries
pip install geopandas requests

# Run the download script
cd /Users/julienh/Desktop/MADS/Capstone
python scripts/download_hpms_data.py
```

**What it does**:
- Downloads HPMS 2018 data for California, Texas, New York
- Saves as GeoPackage files (`.gpkg`) in `data/raw/hpms/`
- Includes AADT (traffic volume) for all Federal-Aid highways

**Expected output**:
- `data/raw/hpms/california_hpms_2018.gpkg` (~50-100 MB)
- `data/raw/hpms/texas_hpms_2018.gpkg` (~150-200 MB)
- `data/raw/hpms/new_york_hpms_2018.gpkg` (~40-80 MB)

**Time**: 5-15 minutes depending on internet speed

---

### Option 2: Manual Download via Web Browser (if script fails)

1. **Go to**: https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm

2. **Find your state** in the table (California, Texas, New York)

3. **Click "Feature Server" link** - Opens ArcGIS REST endpoint

4. **Use one of these methods**:

   **Method A - Download via Web Interface**:
   - Click "Query" tab at bottom
   - Set "Where" = `1=1` (get all records)
   - Set "Out Fields" = `*` (all fields)
   - Set "Format" = `GeoJSON`
   - Click "Query (GET)"
   - Save the result as a `.geojson` file

   **Method B - Use QGIS** (recommended if you have it):
   - Download QGIS: https://qgis.org/download/
   - Layer → Add Layer → Add ArcGIS REST Server Layer
   - Paste Feature Server URL
   - Export as GeoPackage

---

## 📊 What You Get

### Key Fields in HPMS Data

| Field | Description | Example |
|-------|-------------|---------|
| `AADT` | Annual Average Daily Traffic | 50,000 vehicles/day |
| `AADT_COMBINATION` | Daily combination trucks | 5,000 trucks/day |
| `AADT_SINGLE_UNIT` | Daily single-unit trucks | 2,000 trucks/day |
| `ROUTE_NUMBER` | Road number | "101", "I-880", "US-50" |
| `THROUGH_LANES` | Number of lanes | 4 |
| `SPEED_LIMIT` | Posted speed limit | 65 mph |
| `F_SYSTEM` | Functional class | 1=Interstate, 2=Other freeway |
| `URBAN_CODE` | Urban area code | Urban vs rural |
| `geometry` | Road geometry | LineString |

---

## 🔗 How to Use with Your Work Zones

### Step 1: Load HPMS Data

```python
import geopandas as gpd
import pandas as pd

# Load HPMS
ca_hpms = gpd.read_file('data/raw/hpms/california_hpms_2018.gpkg')
print(f"Loaded {len(ca_hpms):,} road segments")

# Check AADT range
print(f"AADT range: {ca_hpms['AADT'].min():,} - {ca_hpms['AADT'].max():,}")
```

### Step 2: Spatial Join with Work Zones

```python
# Load your work zones (with coordinates)
work_zones = pd.read_csv('data/processed/ca_work_zones_analysis.csv')

# Convert to GeoDataFrame
work_zones_gdf = gpd.GeoDataFrame(
    work_zones,
    geometry=gpd.points_from_xy(work_zones.longitude, work_zones.latitude),
    crs='EPSG:4326'
)

# Spatial join to nearest road segment
work_zones_with_traffic = gpd.sjoin_nearest(
    work_zones_gdf,
    ca_hpms[['AADT', 'AADT_COMBINATION', 'THROUGH_LANES', 'SPEED_LIMIT', 'geometry']],
    how='left',
    max_distance=100  # meters
)

print(f"✓ Matched {work_zones_with_traffic['AADT'].notna().sum()} work zones to traffic data")
```

### Step 3: Add to Features

```python
# Now you have AADT for each work zone!
work_zones_with_traffic.to_csv('data/processed/work_zones_with_traffic.csv', index=False)

# Use in ML model
features_df['aadt'] = work_zones_with_traffic['AADT']
features_df['truck_percent'] = (
    work_zones_with_traffic['AADT_COMBINATION'] /
    work_zones_with_traffic['AADT'] * 100
)
features_df['lanes'] = work_zones_with_traffic['THROUGH_LANES']
```

---

## 🎯 Why AADT is Critical

**Without AADT**: "This work zone had 5 crashes" → Is that a lot?

**With AADT**: "This work zone had 5 crashes per 10 million vehicle-miles" → Now you can compare!

**Crash Rate Formula**:
```python
crash_rate = (
    crash_count /
    (AADT * duration_days * segment_length_miles / 1_000_000)
)
# Result: Crashes per million vehicle-miles traveled (standard metric)
```

---

## 🐛 Troubleshooting

### Issue: Script fails with connection error

**Solution**: FHWA server might be down. Try:
1. Check server status: https://geo.dot.gov/server/rest/services
2. Wait 30 minutes and retry
3. Use manual download (Option 2)

### Issue: Downloaded but AADT field is missing

**Solution**: Field names vary by year
- Try: `AADT`, `aadt`, `ADT`, `ANNUAL_AVERAGE_DAILY_TRAFFIC`
- Check: `print(gdf.columns)` to see all available fields

### Issue: Can't match work zones to HPMS roads

**Solution**: Use spatial join with buffer
```python
# Buffer work zone points to 100m radius
work_zones_gdf['geometry'] = work_zones_gdf.geometry.buffer(0.001)  # ~100m

# Then spatial join
matched = gpd.sjoin(work_zones_gdf, ca_hpms, predicate='intersects')
```

### Issue: Download takes forever (>1 hour)

**Solution**: State data is large. Try:
1. Download only your study area (filter by county)
2. Use state DOT source instead (often faster)
3. Download overnight

---

## 📦 Alternative: State DOT Data

If FHWA HPMS is too slow/difficult:

### California (Caltrans)
- **URL**: https://dot.ca.gov/programs/traffic-operations/census
- **Faster**: More direct access
- **More recent**: Updated annually

### Texas (TxDOT)
- **URL**: https://www.txdot.gov/data-maps/traffic-counts.html
- **Includes**: Interactive map + downloads

### New York (NYSDOT)
- **URL**: https://www.dot.ny.gov/tdv
- **Tool**: Traffic Data Viewer (online GIS)

---

## ⏱️ Time Budget

- **Option 1 (Script)**: 5-15 minutes
- **Option 2 (Manual)**: 30-60 minutes
- **Processing/Joining**: 10-30 minutes

**Total**: ~1-2 hours to get AADT integrated into your project

---

## 📝 Next Steps After Getting HPMS

1. ✅ Run download script or manual download
2. ✅ Spatial join with work zones
3. ✅ Add AADT as ML feature
4. ✅ Calculate crash rates
5. ⏭️ Move on to weather data (easier!)

---

## 💬 Need Help?

**Contact FHWA**:
- Thomas Roff: thomas.roff@dot.gov
- Phone: (202) 366-5035

**Request**: "Graduate student working on work zone safety research. Need HPMS shapefiles for California, Texas, New York with AADT fields. Most recent year available."

---

**See full guide**: `docs/HPMS_DATA_ACCESS_GUIDE.md`
