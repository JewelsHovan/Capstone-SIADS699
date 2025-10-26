# Raw Texas Data - Data Dictionary

**Last Updated**: 2025-10-26

This directory contains raw, unprocessed data for Texas work zone safety analysis.

---

## Directory Structure

```
raw_texas/
├── crashes/
│   ├── us_accidents_texas.csv      (582,837 crashes, 213 MB)
│   └── austin_crashes.csv          (223,713 crashes, 80.8 MB)
├── traffic/
│   └── txdot_aadt_annual.gpkg      (41,467 stations, 9 MB)
├── workzones/
│   ├── workzones.csv               (2,180 work zones, 1.5 MB)
│   └── workzones.json              (2,180 work zones, 2.7 MB)
└── weather/
    └── weather.csv                 (17,532 daily records, 4.2 MB)
```

---

## 📁 crashes/

### us_accidents_texas.csv

**Source**: Kaggle US Accidents Dataset (Texas subset)
**Records**: 582,837 crashes
**Date Range**: 2016-2023
**Coverage**: Statewide Texas

**Key Columns** (49 total):

| Column | Type | Description |
|--------|------|-------------|
| `ID` | string | Unique crash identifier |
| `Severity` | int | Traffic impact severity (1-4) |
| `Start_Time` | datetime | Crash occurrence time |
| `Start_Lat`, `Start_Lng` | float | Crash location (WGS84) |
| `City`, `County`, `State` | string | Location details |
| `Temperature(F)` | float | Temperature at crash time |
| `Visibility(mi)` | float | Visibility distance |
| `Weather_Condition` | string | Weather description |
| `Junction` | bool | Intersection indicator |
| `Traffic_Signal` | bool | Signal present |

**Note**: This dataset measures traffic **impact severity**, not injury severity.

**Original Source**: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents

---

### austin_crashes.csv

**Source**: City of Austin Open Data Portal
**Records**: 223,713 crashes
**Date Range**: 2010-2025
**Coverage**: Austin city limits only

**Key Columns** (similar to US Accidents):

| Column | Type | Description |
|--------|------|-------------|
| `ID` | string | Unique identifier |
| `Start_Time` | datetime | Crash time |
| `Start_Lat`, `Start_Lng` | float | Location |
| `Severity` | int | Traffic impact (1-4) |
| `City` | string | "Austin" for all records |

**Source URL**: https://data.austintexas.gov/

---

## 📁 traffic/

### txdot_aadt_annual.gpkg

**Source**: Texas Department of Transportation (TxDOT)
**Format**: GeoPackage (spatial database)
**Records**: 41,467 traffic counting stations
**Coverage**: Statewide Texas

**Key Columns**:

| Column | Type | Description |
|--------|------|-------------|
| `RTE_ID` | string | Route identifier |
| `AADT` | int | Annual Average Daily Traffic (vehicles/day) |
| `AADT_YR` | int | Year of AADT measurement |
| `COUNTY_NM` | string | County name |
| `geometry` | Point | Station location (EPSG:4326) |

**AADT Definition**: Average number of vehicles per day over a year, measured at specific road segments.

**Usage**: Join to crash data by nearest spatial match to estimate traffic volume at crash locations.

**Source**: TxDOT Transportation Planning and Programming Division

---

## 📁 workzones/

### workzones.csv & workzones.json

**Source**: Texas Department of Transportation WZDx Feed
**Format**: CSV and JSON (same data, different formats)
**Records**: 2,180 active work zones
**Date**: October 2025 (current active work zones)

**Key Columns** (CSV):

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Work zone identifier |
| `road_name` | string | Road/highway name |
| `description` | string | Work zone description |
| `start_date` | datetime | Work zone start date |
| `end_date` | datetime | Planned end date |
| `geometry` | LineString/WKT | Work zone location |
| `direction` | string | Traffic direction |
| `vehicle_impact` | string | Impact level (e.g., "all-lanes-open", "some-lanes-closed") |

**WZDx Standard**: Work Zone Data Exchange specification for standardized work zone data.

**Note**: These are **current/active** work zones, not historical. Use for:
- Real-time risk prediction
- Planning future work zone locations
- Testing models on active zones

**Source**: https://txdot.public.ms2soft.com/

---

## 📁 weather/

### weather.csv

**Source**: NOAA Climate Data Online (CDO) API
**Records**: 17,532 daily weather summaries
**Date Range**: 2016-2023
**Coverage**: 6 major Texas metros (Austin, Houston, Dallas, San Antonio, El Paso, Fort Worth)

**Key Columns**:

| Column | Type | Description | Units |
|--------|------|-------------|-------|
| `date` | date | Observation date | - |
| `metro_name` | string | City name | - |
| `county_name` | string | County name | - |
| `precipitation_mm` | float | Daily precipitation | millimeters |
| `temp_max_f` | float | Maximum temperature | Fahrenheit |
| `temp_min_f` | float | Minimum temperature | Fahrenheit |
| `temp_avg_f` | float | Average temperature | Fahrenheit |
| `wind_speed_mph` | float | Average wind speed | mph |
| `snowfall_mm` | float | Snowfall amount | millimeters |
| `metro_lat`, `metro_lon` | float | Station location | WGS84 |

**Weather Stations**:
- Austin: Austin-Bergstrom International (USW00013904)
- Houston: George Bush Intercontinental (USW00012960)
- Dallas: DFW International (USW00013960)
- San Antonio: San Antonio International (USW00012921)
- El Paso: El Paso International (USW00023044)
- Fort Worth: DFW International (shared with Dallas)

**Usage**: Join to crash data by date and nearest metro area.

**Source**: NOAA National Centers for Environmental Information (NCEI)

---

## Data Collection Scripts

All raw data can be re-downloaded using these scripts:

```bash
# Crashes (Austin)
python scripts/download_austin_crashes.py --all

# Crashes (Kaggle)
# Manual download from Kaggle, then extract Texas subset

# Traffic (AADT)
python scripts/download_txdot_aadt_annual.py

# Work Zones
python scripts/download_texas_feed.py

# Weather
python scripts/download_noaa_weather.py --token YOUR_TOKEN
```

---

## Data Processing Pipeline

```
RAW DATA                         PROCESSED DATA
─────────                        ──────────────
us_accidents_texas.csv    ─┐
austin_crashes.csv        ─┤
                           ├──→  build_ml_training_dataset.py
txdot_aadt_annual.gpkg    ─┤         ↓
weather.csv               ─┘    crash_level/
                                  - train.csv
                                  - val.csv
                                  - test.csv
                                       ↓
                               build_segment_dataset.py
                                       ↓
                                segment_level/
                                  - train.csv
                                  - val.csv
                                  - test.csv
```

---

## Coordinate Reference Systems

All spatial data uses:
- **Input CRS**: EPSG:4326 (WGS84 lat/lon)
- **Processing CRS**: EPSG:3083 (Texas Centric, meters) for distance calculations
- **Output CRS**: EPSG:4326 for compatibility

---

## Data Quality Notes

### Known Issues

1. **Crash Data**:
   - Severity represents traffic impact, not injury
   - Some location precision varies (±10-100m)
   - Austin data has more complete attributes than Kaggle data

2. **AADT Data**:
   - Not all roads have stations (rural roads less covered)
   - AADT year varies by station (most are recent)
   - Join by nearest station (mean distance ~577m)

3. **Work Zones**:
   - Current data only (not historical)
   - Some work zones have imprecise geometries
   - Duration estimates may change

4. **Weather**:
   - Daily summaries (not hourly)
   - Metro-level only (not statewide coverage)
   - Some missing values (<2%)

---

## File Formats

| Format | Tools | Description |
|--------|-------|-------------|
| CSV | pandas, Excel | Comma-separated values |
| JSON | Python json, jq | JavaScript Object Notation |
| GPKG | QGIS, GeoPandas | GeoPackage spatial database |

---

## Citations

### Crash Data
Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. "A Countrywide Traffic Accident Dataset." 2019.

### OpenStreetMap
OpenStreetMap contributors. "Planet dump." https://www.openstreetmap.org

### TxDOT
Texas Department of Transportation. "Annual Average Daily Traffic (AADT) Data." Transportation Planning and Programming Division.

### NOAA
National Oceanic and Atmospheric Administration. "Climate Data Online." National Centers for Environmental Information.

---

## License & Usage

- **Crash Data (Kaggle)**: CC0 Public Domain
- **OpenStreetMap**: ODbL (Open Database License)
- **TxDOT Data**: Public domain (Texas Government Code)
- **NOAA Data**: Public domain (U.S. Government)

**Note**: Always verify current license terms when using this data.

---

## Contact

For questions about data sources or collection, see:
- Project README
- Individual download scripts in `scripts/`
- `docs/DATA_INTEGRATION_GUIDE.md`

**Last Updated**: 2025-10-26
