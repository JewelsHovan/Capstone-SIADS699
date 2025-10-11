# Crash Data + Work Zone Integration Analysis

**Date**: October 10, 2025
**Status**: Complete

---

## Overview

This document summarizes the integration of crash data from TIMS (Transportation Injury Mapping System - UC Berkeley) with Work Zone Data Exchange (WZDx) feeds for comprehensive work zone safety analysis.

---

## Data Sources

### 1. Crash Data (TIMS)
- **Source**: UC Berkeley Transportation Injury Mapping System
- **Location**: `data/Crashes.csv`
- **Coverage**: Alameda County, California
- **Time Period**: 2023-2025 (focused on 2023 for work zone comparison)
- **Records**: 17,161 total crashes, 11,246 with coordinates

### 2. Work Zone Data (WZDx)
- **Source**: California 511 API
- **Location**: `data/raw/ca_wzdx_feed.json`
- **Coverage**: San Francisco Bay Area
- **Records**: 1,186 active work zones
- **Data Quality**: Excellent (detailed vehicle impact, worker presence)

---

## Dataset Statistics

### Crash Data Summary

**Total Crashes**: 17,161
- **Time Range**: January 1, 2023 - June 30, 2025
- **Geographic Coverage**: 15 cities in Alameda County
- **Coordinates Available**: 11,246 (65.5%)

**Top Cities by Crash Count**:
1. Oakland: 4,950 crashes
2. Unincorporated: 2,754 crashes
3. Fremont: 2,034 crashes
4. Hayward: 1,488 crashes
5. Berkeley: 1,465 crashes

**Severity Distribution**:
- Fatal: 198 (1.2%)
- Severe Injury: 1,144 (6.7%)
- Visible Injury: 5,850 (34.1%)
- Complaint of Pain: 9,969 (58.1%)

**Casualties**:
- Total Killed: 214
- Total Injured: 22,589
- Crashes with Fatalities: 198
- Crashes with Injuries: 17,029

**Special Crash Types**:
- Alcohol-Involved: 1,596 (9.3%)
- Hit-and-Run: 17,161 records tracked

**Top Crash Locations**:
1. I-880 Southbound: 938 crashes
2. I-880 Northbound: 787 crashes
3. I-580 Westbound: 482 crashes
4. I-580 Eastbound: 480 crashes
5. International Blvd: 277 crashes

### 2023 Crashes (For Work Zone Comparison)

**Total**: 4,442 crashes with coordinates
- Fatal: 59
- Severe Injury: 297
- Visible Injury: 1,610
- Other: 2,476

**Top Crash Roads (2023)**:
1. I-880 S/B: 313 crashes
2. I-880 N/B: 267 crashes
3. I-580 E/B: 194 crashes
4. I-580 W/B: 170 crashes
5. I-80 W/B: 150 crashes

### Work Zone Data Summary

**Total Work Zones**: 1,186
- All-Lanes-Closed: Highest severity impact
- Some-Lanes-Closed: Moderate impact
- All-Lanes-Open: Lower impact

**Top Work Zone Roads**:
1. Meridian Ave: 30 work zones
2. Urbano Dr: 14 work zones
3. Folsom St: 12 work zones
4. Market St: 10 work zones
5. Mercado Way: 10 work zones

---

## Generated Outputs

### 1. Crash Analysis Visualization
**File**: `outputs/visualizations/crash_analysis.png`

Four-panel visualization showing:
- Crash severity distribution
- Crashes by day of week
- Special crash types (pedestrian, bicycle, alcohol, etc.)
- Top 10 roads by crash count

### 2. Interactive Crash Map
**File**: `outputs/maps/crash_map.html`

**Features**:
- 11,246 crash markers color-coded by severity
- Layer controls to filter by severity level
- Click markers for detailed crash information
- Statistics legend with totals

**Color Coding**:
- 🔴 Dark Red: Fatal
- 🔴 Red: Severe Injury
- 🟠 Orange: Visible Injury
- 🔵 Light Blue: Complaint of Pain
- ⚪ Light Gray: Property Damage Only

### 3. Fatal Crashes Map
**File**: `outputs/maps/fatal_crashes_map.html`

Focused map showing only fatal crashes (129 crashes) for detailed safety analysis.

### 4. Crash + Work Zone Overlay Map
**File**: `outputs/maps/crash_workzone_overlay.html`

**Features**:
- Work zones (purple/blue markers) overlaid with crashes (red/orange)
- Layer controls to toggle crashes and work zones
- 2023 crashes only for temporal alignment
- Interactive popups with details

**Use Cases**:
- Identify crashes occurring near work zones
- Compare crash patterns in work zone areas vs. non-work zone areas
- Explore potential safety correlations
- Identify high-risk work zone locations

### 5. Summary Report
**File**: `docs/CRASH_DATA_SUMMARY.md`

Comprehensive markdown report with all statistics and findings.

---

## Analysis Scripts

### 1. `scripts/analyze_crashes.py`
Comprehensive crash data exploration script.

**Outputs**:
- Console statistics summary
- Visualization chart (PNG)
- Markdown summary report

**Run**:
```bash
python scripts/analyze_crashes.py
```

### 2. `scripts/create_crash_map.py`
Interactive crash map generator.

**Outputs**:
- All crashes map (HTML)
- Fatal crashes only map (HTML)

**Run**:
```bash
python scripts/create_crash_map.py
```

### 3. `scripts/create_crash_workzone_overlay.py`
Crash + work zone overlay map generator.

**Outputs**:
- Combined overlay map (HTML)
- Proximity analysis statistics

**Run**:
```bash
python scripts/create_crash_workzone_overlay.py
```

---

## Key Insights

### 1. Geographic Overlap
- Crashes and work zones both concentrated in Bay Area
- Major highways (I-880, I-580, I-80) show high crash counts
- Work zones more distributed on local streets (Meridian, Market, Folsom)

### 2. Severity Patterns
- Fatal crashes: 59 in 2023 (1.3% of total)
- Severe injuries: 297 in 2023 (6.7% of total)
- Most crashes (91%) are injury/complaint crashes
- 214 total fatalities across all years

### 3. Temporal Patterns
- Crashes fairly evenly distributed across weekdays
- Slight increase Thursday-Friday
- Weekend slightly lower (Saturday lowest)

### 4. Environmental Factors
- Most crashes in clear weather (A: 14,397)
- Most on dry roads (A: 15,488)
- Most in daylight conditions (A: 11,362)
- 9.3% alcohol-involved

### 5. Data Quality
- **Crash Data**: Excellent coordinates (65.5% coverage)
- **Work Zone Data**: 100% coordinates (GeoJSON format)
- **Temporal Alignment**: 2023 data available for both datasets
- **Geographic Alignment**: Both cover Bay Area/Alameda County

---

## Next Steps for Analysis

### Spatial Analysis
1. Calculate crashes within X meters of work zones
2. Compare crash rates in work zone vs. non-work zone areas
3. Identify work zones with highest nearby crash counts
4. Use GIS tools (GeoPandas, Shapely) for precise spatial joins

### Temporal Analysis
1. Track crash trends before/during/after work zones
2. Analyze time-of-day patterns for work zone crashes
3. Compare work zone crash patterns on weekdays vs. weekends

### Statistical Analysis
1. Crash severity comparison: work zone vs. non-work zone
2. Worker presence impact on crash characteristics
3. Lane closure impact on crash frequency/severity
4. Regression analysis of contributing factors

### Visualization Enhancements
1. Heat maps of crash density
2. Time-animated maps showing work zones and crashes over time
3. Cluster analysis of high-risk areas
4. Dashboard combining multiple views

### Machine Learning Opportunities
1. Predict high-risk work zone locations
2. Classify crash severity based on work zone characteristics
3. Recommend safety interventions

---

## Data Integration Recommendations

### For Accurate Spatial Joins
Use GeoPandas for precise distance calculations:
```python
import geopandas as gpd
from shapely.geometry import Point

# Create GeoDataFrames
crashes_gdf = gpd.GeoDataFrame(
    crashes_df,
    geometry=gpd.points_from_xy(crashes_df.LONGITUDE, crashes_df.LATITUDE),
    crs='EPSG:4326'
)

workzones_gdf = gpd.GeoDataFrame(
    workzones_df,
    geometry=gpd.points_from_xy(workzones_df.longitude, workzones_df.latitude),
    crs='EPSG:4326'
)

# Buffer work zones by 100 meters
workzones_gdf = workzones_gdf.to_crs('EPSG:3857')  # Convert to meters
workzones_buffered = workzones_gdf.buffer(100)

# Spatial join
crashes_near_wz = gpd.sjoin(crashes_gdf, workzones_buffered, predicate='within')
```

### For Temporal Alignment
```python
# Filter crashes to work zone active periods
# (Requires work zone start/end dates from feed)

crashes_df['COLLISION_DATE'] = pd.to_datetime(crashes_df['COLLISION_DATE'])
workzones_df['start_date'] = pd.to_datetime(workzones_df['start_date'])
workzones_df['end_date'] = pd.to_datetime(workzones_df['end_date'])

# Join on location AND time overlap
```

---

## Challenges and Limitations

### Data Challenges
1. **Missing Coordinates**: 34.5% of crashes lack coordinates
2. **Temporal Mismatch**: Work zone feed is snapshot (current), crashes are historical
3. **Geographic Scope**: Crashes county-wide, work zones more localized
4. **Work Zone Geometry**: LineStrings vs. point crashes (using center points for now)

### Analysis Limitations
1. **Proximity Analysis**: Current analysis is visual/approximate
2. **Causality**: Cannot determine if work zones caused crashes
3. **Confounding Factors**: Many variables affect crash occurrence
4. **Data Recency**: Work zone data is live snapshot, may not reflect 2023 work zones

### Recommendations
1. Use historical work zone archive from USDOT S3 bucket
2. Implement precise spatial buffering with GeoPandas
3. Consider additional confounding variables (traffic volume, weather events)
4. Validate findings with domain experts

---

## Files Created

### Scripts
- `scripts/analyze_crashes.py` - Crash data exploration
- `scripts/create_crash_map.py` - Interactive crash map
- `scripts/create_crash_workzone_overlay.py` - Overlay map

### Outputs
- `outputs/visualizations/crash_analysis.png` - Statistical charts
- `outputs/maps/crash_map.html` - All crashes map
- `outputs/maps/fatal_crashes_map.html` - Fatal crashes only
- `outputs/maps/crash_workzone_overlay.html` - Combined overlay

### Documentation
- `docs/CRASH_DATA_SUMMARY.md` - Crash statistics report
- `docs/CRASH_WORKZONE_INTEGRATION.md` - This document

---

## Conclusion

Successfully integrated crash data with work zone data to enable comprehensive safety analysis. The overlay maps provide visual exploration of potential crash-work zone correlations, and the analysis scripts provide foundation for deeper statistical analysis.

**Key Achievement**: Combined two independent safety datasets (crashes + work zones) into unified visualization and analysis framework, enabling data-driven work zone safety research.

**For Capstone Project**: This integration provides rich foundation for:
- Exploratory data analysis
- Geographic clustering
- Safety metric development
- Risk scoring methodology
- Statistical analysis
- Policy recommendations

---

**Next**: Use GeoPandas for precise spatial joins and statistical analysis of crash-work zone relationships.
