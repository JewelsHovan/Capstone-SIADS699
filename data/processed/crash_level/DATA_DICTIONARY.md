# Crash-Level Dataset - Data Dictionary

**Last Updated**: 2025-10-26
**Files**: train.csv, val.csv, test.csv
**Total Samples**: 1,135,762 crashes (2016-2023)
**Total Features**: 78 columns

---

## Dataset Overview

Each row represents **one individual crash event** with associated road, traffic, weather, and temporal features.

**Target Variable**: `high_severity` (binary classification: 1 = Severity >= 3, 0 = Severity < 3)

---

## Column Categories

- [Identifiers & Metadata](#identifiers--metadata)
- [Temporal Features](#temporal-features)
- [Location Features](#location-features)
- [Road Geometry (OSMnx)](#road-geometry-osmnx)
- [Traffic Features](#traffic-features)
- [Weather Features](#weather-features)
- [Infrastructure Features](#infrastructure-features)
- [Target Variables](#target-variables)

---

## Identifiers & Metadata

| Column | Type | Description |
|--------|------|-------------|
| `ID` | string | Unique crash identifier from source dataset |
| `Source` | string | Data source (e.g., "MapQuest") |
| `Description` | string | Brief description of crash event |

---

## Temporal Features

### Raw Timestamps

| Column | Type | Description |
|--------|------|-------------|
| `Start_Time` | datetime | Timestamp when crash occurred |
| `End_Time` | datetime | Timestamp when crash impact ended |
| `Weather_Timestamp` | datetime | Timestamp of weather observation |

### Derived Time Features

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `year` | int | Year of crash | 2016-2023 |
| `month` | int | Month of crash | 1-12 |
| `day_of_week` | int | Day of week | 0=Monday, 6=Sunday |
| `hour` | int | Hour of day | 0-23 |
| `is_weekend` | bool | Weekend indicator | 0=Weekday, 1=Weekend |
| `is_rush_hour` | bool | Rush hour indicator | 1 if hour in [7,8,9,16,17,18], else 0 |
| `time_of_day` | category | Time period | morning, afternoon, evening, night |

---

## Location Features

| Column | Type | Description |
|--------|------|-------------|
| `Start_Lat` | float | Latitude of crash location (WGS84) |
| `Start_Lng` | float | Longitude of crash location (WGS84) |
| `End_Lat` | float | Latitude of crash end point |
| `End_Lng` | float | Longitude of crash end point |
| `Distance(mi)` | float | Length of road affected by crash (miles) |
| `Street` | string | Street name where crash occurred |
| `City` | string | City name (Houston, Dallas, Austin, etc.) |
| `County` | string | County name |
| `State` | string | State (TX for all records) |
| `Zipcode` | string | ZIP code |
| `Country` | string | Country (US for all records) |
| `Timezone` | string | Timezone (e.g., "US/Central") |
| `Airport_Code` | string | Nearest airport code |
| `is_urban` | bool | Urban vs rural classification | 1=Urban, 0=Rural |

---

## Road Geometry (OSMnx)

Features extracted from OpenStreetMap via OSMnx library.

| Column | Type | Description | Completeness |
|--------|------|-------------|--------------|
| `highway_type` | category | Road classification | 68.3% |
| `num_lanes` | float | Number of lanes | 51.5% |
| `speed_limit` | float | Posted speed limit (mph) | 23.8% |
| `is_bridge` | bool | Bridge indicator | 100% |
| `is_tunnel` | bool | Tunnel indicator | 100% |
| `is_oneway` | bool | One-way street indicator | 100% |
| `road_name` | string | Road name from OSM | 68.3% |

### highway_type Values

| Value | Description | Frequency |
|-------|-------------|-----------|
| `motorway` | Interstate highways | ~15% |
| `motorway_link` | Interstate ramps | ~5% |
| `trunk` | Major highways | ~10% |
| `primary` | Major roads | ~20% |
| `secondary` | Secondary roads | ~15% |
| `tertiary` | Tertiary roads | ~10% |
| `residential` | Residential streets | ~20% |
| `service` | Service roads | ~5% |

---

## Traffic Features

| Column | Type | Description | Source | Completeness |
|--------|------|-------------|--------|--------------|
| `aadt` | int | Annual Average Daily Traffic (vehicles/day) | TxDOT AADT Stations | 100% |
| `distance_to_aadt_m` | float | Distance to nearest AADT station (meters) | Calculated | 100% |

**Note**: AADT values are from nearest traffic counting station (mean distance: 577m)

---

## Weather Features

Weather conditions at time of crash from Kaggle US Accidents dataset.

### Raw Weather Measurements

| Column | Type | Description | Units | Completeness |
|--------|------|-------------|-------|--------------|
| `Temperature(F)` | float | Temperature | Fahrenheit | 98.3% |
| `Wind_Chill(F)` | float | Wind chill temperature | Fahrenheit | 80% |
| `Humidity(%)` | float | Relative humidity | Percentage | 98% |
| `Pressure(in)` | float | Atmospheric pressure | Inches | 98% |
| `Visibility(mi)` | float | Visibility distance | Miles | 98.1% |
| `Wind_Direction` | string | Wind direction | Cardinal (N,S,E,W,etc.) | 97% |
| `Wind_Speed(mph)` | float | Wind speed | Miles per hour | 97% |
| `Precipitation(in)` | float | Precipitation amount | Inches | 95% |
| `Weather_Condition` | string | Weather description | Text (e.g., "Clear", "Rain") | 98% |

### Derived Weather Features

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `weather_category` | category | Grouped weather type | clear, rain, fog, snow, etc. |
| `adverse_weather` | bool | Adverse conditions indicator | 1=Rain/Snow/Fog, 0=Clear |
| `low_visibility` | bool | Low visibility indicator | 1 if Visibility < 5 miles, else 0 |
| `temp_category` | category | Temperature range | freezing, cold, mild, warm, hot |

---

## Infrastructure Features

Point-of-interest indicators from OpenStreetMap.

| Column | Type | Description |
|--------|------|-------------|
| `Junction` | bool | Junction/Intersection present |
| `Traffic_Signal` | bool | Traffic signal present |
| `Stop` | bool | Stop sign present |
| `Crossing` | bool | Pedestrian crossing present |
| `Railway` | bool | Railway crossing present |
| `Station` | bool | Transit station nearby |
| `Amenity` | bool | Amenity nearby |
| `Bump` | bool | Speed bump present |
| `Give_Way` | bool | Yield sign present |
| `No_Exit` | bool | Dead-end road |
| `Roundabout` | bool | Roundabout present |
| `Traffic_Calming` | bool | Traffic calming feature |
| `Turning_Loop` | bool | Turning loop present |

---

## Sunrise/Sunset Features

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `Sunrise_Sunset` | category | Daylight indicator | Day, Night |
| `Civil_Twilight` | category | Civil twilight | Day, Night |
| `Nautical_Twilight` | category | Nautical twilight | Day, Night |
| `Astronomical_Twilight` | category | Astronomical twilight | Day, Night |

---

## Target Variables

| Column | Type | Description | Distribution |
|--------|------|-------------|--------------|
| `Severity` | int | Traffic impact severity (1-4) | 1=minor, 4=severe |
| `high_severity` | bool | Binary target variable | 1 if Severity >= 3, else 0 |

### Severity Distribution

| Split | high_severity=1 | high_severity=0 | Total |
|-------|-----------------|-----------------|-------|
| Train (2016-2021) | 234,238 (24.9%) | 707,622 (75.1%) | 941,860 |
| Val (2022) | 15,843 (9.4%) | 152,110 (90.6%) | 167,953 |
| Test (2023) | 152 (0.6%) | 25,797 (99.4%) | 25,949 |

**Note**: Severity measures **traffic impact/delay**, NOT injury severity.

---

## OSMnx Road Network Features (Additional Metadata)

These columns are raw OSM tags, mostly for reference:

| Column | Description |
|--------|-------------|
| `u`, `v` | OSM node IDs (start, end of road segment) |
| `key` | Edge key in OSM graph |
| `edge_id` | Unique edge identifier |
| `highway` | Raw OSM highway tag |
| `name` | OSM road name |
| `lanes` | Raw lanes value from OSM |
| `maxspeed` | Raw speed limit from OSM |
| `oneway` | OSM oneway tag |
| `bridge` | OSM bridge tag |
| `tunnel` | OSM tunnel tag |

---

## Missing Data Strategy

| Feature | Missing % | Strategy |
|---------|-----------|----------|
| `highway_type` | 31.7% | Impute with 'unknown' or mode by city |
| `num_lanes` | 48.5% | Impute with median by highway_type |
| `speed_limit` | 76.2% | Impute with median by highway_type + city |
| `Temperature(F)` | 1.7% | Forward-fill by hour |
| `Visibility(mi)` | 1.9% | Forward-fill by hour |

---

## Usage Examples

### Loading Data

```python
import pandas as pd

# Load datasets
train = pd.read_csv('train.csv')
val = pd.read_csv('val.csv')
test = pd.read_csv('test.csv')

print(f"Train shape: {train.shape}")
print(f"Val shape: {val.shape}")
print(f"Test shape: {test.shape}")
```

### Feature Selection

```python
# Core features for modeling
feature_cols = [
    # Road
    'highway_type', 'num_lanes', 'speed_limit', 'is_bridge',
    # Traffic
    'aadt',
    # Temporal
    'hour', 'day_of_week', 'is_weekend', 'is_rush_hour',
    # Weather
    'Temperature(F)', 'Visibility(mi)', 'adverse_weather',
    # Infrastructure
    'Junction', 'Traffic_Signal',
    # Location
    'is_urban'
]

X_train = train[feature_cols]
y_train = train['high_severity']
```

### Handling Categorical Variables

```python
from sklearn.preprocessing import LabelEncoder

# Encode highway_type
le = LabelEncoder()
train['highway_type_encoded'] = le.fit_transform(train['highway_type'].fillna('unknown'))

# Or use one-hot encoding
train_encoded = pd.get_dummies(train, columns=['highway_type', 'weather_category'])
```

---

## Data Sources

- **Crash Data**: Kaggle US Accidents Dataset (Moosavi et al., 2019)
- **Road Network**: OpenStreetMap via OSMnx (Boeing, 2017)
- **Traffic Counts**: TxDOT AADT Annual Stations
- **Weather**: Included in Kaggle dataset (aggregated from multiple APIs)

---

## Contact

For questions about this dataset, see project documentation or `data/processed/README.md`.

**Dataset Version**: 20251026_160909
