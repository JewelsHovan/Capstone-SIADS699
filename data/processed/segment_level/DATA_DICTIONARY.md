# Segment-Level Dataset - Data Dictionary

**Last Updated**: 2025-10-26
**Files**: train.csv, val.csv, test.csv
**Total Samples**: 303,281 segment-quarters (2016-2021 train data)
**Total Features**: 39 columns

---

## Dataset Overview

Each row represents **one road segment during one time period (quarter)** with aggregated crash statistics and environmental features.

**Granularity**: Road segment × Time period (quarterly)
**Unique Segments**: 75,650 road segments

**Target Variables** (Multiple):
- `crash_count` - Number of crashes in segment-quarter
- `severity_rate` - Proportion of high-severity crashes
- `traffic_impact` - AADT × severity_rate
- `risk_score_simple` - Composite risk score
- `risk_category` - LOW / MEDIUM / HIGH / VERY_HIGH

---

## Column Categories

- [Segment Identifiers](#segment-identifiers)
- [Temporal Features](#temporal-features)
- [Location Features](#location-features)
- [Crash Metrics (Targets)](#crash-metrics-targets)
- [Road Features](#road-features)
- [Traffic Features](#traffic-features)
- [Temporal Patterns](#temporal-patterns)
- [Weather Patterns](#weather-patterns)
- [Infrastructure Indicators](#infrastructure-indicators)
- [Historical Features](#historical-features)

---

## Segment Identifiers

| Column | Type | Description |
|--------|------|-------------|
| `segment_id` | string | Unique segment identifier: City_highway_lanes_lat_lon |
| `year_quarter` | string | Time period identifier (e.g., "2021_Q3") |
| `year` | int | Year |
| `quarter` | int | Quarter (1-4) |

**Example segment_id**: `Houston_motorway_4_29.758_-95.423`

### How Segments Are Defined

Segments are created by grouping crashes that occur on:
- Same city
- Same highway type
- Same number of lanes
- Same geographic bin (~100m × 100m grid)

This creates ~75,650 unique road segments across Texas.

---

## Temporal Features

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `year` | int | Year of time period | 2016-2021 (train) |
| `quarter` | int | Quarter of year | 1-4 |
| `year_quarter` | string | Combined identifier | "2021_Q3" |

---

## Location Features

| Column | Type | Description |
|--------|------|-------------|
| `City` | string | City name (Houston, Dallas, Austin, etc.) |
| `Start_Lat` | float | Mean latitude of crashes in segment |
| `Start_Lng` | float | Mean longitude of crashes in segment |
| `is_urban` | bool | Urban vs rural (max across crashes) |

---

## Crash Metrics (Targets)

### Primary Targets

| Column | Type | Description | Range | Mean (Train) |
|--------|------|-------------|-------|--------------|
| `crash_count` | int | Number of crashes in segment-quarter | 1-100+ | 3.11 |
| `Severity` | float | Mean severity score (1-4) | 1.0-4.0 | 2.32 |
| `high_severity` | int | Count of high-severity crashes | 0-50+ | 0.59 |
| `severity_rate` | float | Proportion of high-severity crashes | 0.0-1.0 | 0.19 (19%) |

### Derived Risk Metrics

| Column | Type | Description | Formula | Mean (Train) |
|--------|------|-------------|---------|--------------|
| `traffic_impact` | float | Traffic-weighted severity | aadt × severity_rate | 10,603 |
| `crash_density` | float | Crashes per 1000 vehicles | (crash_count / aadt) × 1000 | 0.60 |
| `risk_score_simple` | float | Composite risk score | See below | 10.13 |
| `risk_category` | category | Risk classification | LOW/MEDIUM/HIGH/VERY_HIGH | - |

**risk_score_simple Formula**:
```
risk_score = crash_count * 0.4 +
             severity_rate * 100 * 0.3 +
             traffic_impact / 1000 * 0.3
```

### Risk Category Distribution (Train)

| Category | Count | Percentage |
|----------|-------|------------|
| LOW | 209,057 | 68.9% |
| MEDIUM | 21,021 | 6.9% |
| HIGH | 3,973 | 1.3% |
| VERY_HIGH | 69,230 | 22.8% |

---

## Road Features

Aggregated from crashes in segment (mode/mean).

| Column | Type | Description | Completeness | Aggregation |
|--------|------|-------------|--------------|-------------|
| `highway_type` | category | Road classification | 100% | Mode |
| `num_lanes` | float | Number of lanes | 35.4% | Mean |
| `speed_limit` | float | Speed limit (mph) | 16.6% | Mean |
| `is_bridge` | bool | Bridge indicator | 100% | Max |
| `is_tunnel` | bool | Tunnel indicator | 100% | Max |

### highway_type Distribution

| Type | Description | Frequency |
|------|-------------|-----------|
| `motorway` | Interstate highways | 15% |
| `primary` | Major roads | 25% |
| `secondary` | Secondary roads | 20% |
| `residential` | Residential streets | 25% |
| Other | Various | 15% |

---

## Traffic Features

| Column | Type | Description | Completeness | Aggregation |
|--------|------|-------------|--------------|-------------|
| `aadt` | float | Average daily traffic volume | 100% | Mean |
| `distance_to_aadt_m` | float | Distance to AADT station (m) | 100% | Mean |

**AADT Interpretation**:
- < 10,000: Low traffic
- 10,000-50,000: Moderate traffic
- 50,000-100,000: High traffic
- > 100,000: Very high traffic (major highways)

---

## Temporal Patterns

Mean proportions of crashes in this segment-time that occurred during certain conditions.

| Column | Type | Description | Range |
|--------|------|-------------|-------|
| `is_rush_hour` | float | Proportion during rush hour (7-9am, 4-6pm) | 0.0-1.0 |
| `is_weekend` | float | Proportion on weekends | 0.0-1.0 |
| `hour` | float | Mean hour of crashes | 0-23 |

**Example Interpretation**:
- `is_rush_hour = 0.6` means 60% of crashes in this segment-quarter occurred during rush hour
- `is_weekend = 0.2` means 20% of crashes occurred on weekends

---

## Weather Patterns

Mean weather conditions across crashes in this segment-time.

| Column | Type | Description | Units | Completeness |
|--------|------|-------------|-------|--------------|
| `Temperature(F)` | float | Mean temperature | Fahrenheit | 98.8% |
| `Humidity(%)` | float | Mean humidity | Percentage | 98% |
| `Visibility(mi)` | float | Mean visibility | Miles | 98% |
| `Wind_Speed(mph)` | float | Mean wind speed | MPH | 97% |
| `adverse_weather` | float | Proportion with adverse weather | 0.0-1.0 | 100% |
| `low_visibility` | float | Proportion with low visibility | 0.0-1.0 | 100% |

---

## Infrastructure Indicators

Maximum values (1 if any crash in segment had this feature, else 0).

| Column | Type | Description |
|--------|------|-------------|
| `Junction` | bool | Junction/Intersection present |
| `Traffic_Signal` | bool | Traffic signal present |
| `Stop` | bool | Stop sign present |
| `Crossing` | bool | Pedestrian crossing present |

---

## Historical Features

Historical crash statistics for this segment across **all** time periods.

| Column | Type | Description | Use Case |
|--------|------|-------------|----------|
| `segment_crash_mean` | float | Mean crashes per quarter for this segment | Identify consistently dangerous segments |
| `segment_crash_std` | float | Standard deviation of crashes | Identify volatile segments |
| `segment_crash_max` | float | Maximum crashes in any quarter | Identify peak danger periods |

**Example Interpretation**:
- High `segment_crash_mean` (e.g., 10+): Consistently dangerous segment
- High `segment_crash_std` (e.g., 5+): Unpredictable/seasonal danger
- High `segment_crash_max` (e.g., 30+): Prone to extreme events

---

## Data Completeness Summary

| Feature Category | Completeness |
|------------------|--------------|
| Crash metrics | 100% |
| Location | 100% |
| Traffic (AADT) | 100% |
| Road type | 100% |
| Temporal patterns | 100% |
| Weather patterns | 98-99% |
| Road geometry (lanes, speed) | 16-35% |

---

## Usage Examples

### Loading Data

```python
import pandas as pd

# Load datasets
seg_train = pd.read_csv('train.csv')
seg_val = pd.read_csv('val.csv')
seg_test = pd.read_csv('test.csv')

print(f"Train: {len(seg_train):,} segment-quarters")
print(f"Unique segments: {seg_train['segment_id'].nunique():,}")
```

### Modeling Crash Count

```python
from sklearn.ensemble import GradientBoostingRegressor

# Features
feature_cols = [
    'highway_type', 'aadt', 'is_rush_hour', 'adverse_weather',
    'Temperature(F)', 'Junction', 'Traffic_Signal',
    'segment_crash_mean', 'segment_crash_std'
]

# Encode categorical
seg_train_encoded = pd.get_dummies(seg_train, columns=['highway_type'])

X = seg_train_encoded[feature_cols]
y = seg_train['crash_count']

# Train model
model = GradientBoostingRegressor(n_estimators=100, max_depth=5)
model.fit(X, y)
```

### Predicting for Active Work Zone

```python
# New work zone features
new_work_zone = pd.DataFrame({
    'highway_type': ['motorway'],
    'aadt': [75000],
    'is_rush_hour': [0.6],  # 60% of time in rush hour
    'adverse_weather': [0.2],  # 20% bad weather
    'Temperature(F)': [78],
    'Junction': [1],
    'Traffic_Signal': [0],
    'segment_crash_mean': [8.0],  # Historical average
    'segment_crash_std': [3.5]
})

# Predict
predicted_crashes = model.predict(new_work_zone)
print(f"Expected crashes per quarter: {predicted_crashes[0]:.1f}")

# Risk classification
if predicted_crashes[0] > 10:
    print("HIGH RISK: Extra precautions needed")
elif predicted_crashes[0] > 5:
    print("MEDIUM RISK: Standard precautions")
else:
    print("LOW RISK: Routine procedures")
```

### Time Series Analysis

```python
# Analyze one segment over time
segment = seg_train[seg_train['segment_id'] == 'Houston_motorway_4_29.758_-95.423']

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))
plt.plot(segment['year_quarter'], segment['crash_count'], marker='o')
plt.title('Crash Count Over Time for Specific Segment')
plt.xlabel('Quarter')
plt.ylabel('Crash Count')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('segment_timeseries.png')
```

### Risk Heatmap

```python
import seaborn as sns

# Create risk matrix: highway_type vs AADT
risk_matrix = seg_train.groupby(['highway_type', pd.cut(seg_train['aadt'], bins=[0, 10000, 50000, 100000, 200000])]).agg({
    'crash_count': 'mean',
    'severity_rate': 'mean'
}).reset_index()

pivot = risk_matrix.pivot(index='highway_type', columns='aadt', values='crash_count')

plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('Mean Crash Count by Road Type and Traffic Volume')
plt.tight_layout()
plt.savefig('risk_heatmap.png')
```

---

## Relationship to Crash-Level Dataset

```
Crash-Level Dataset                  Segment-Level Dataset
───────────────────                  ─────────────────────
Row = 1 crash                   →    Row = 1 segment × 1 quarter

Features:                            Features (aggregated):
  - Individual crash details          - Mean/mode of crash features
  - Point in time                     - Time period
  - Binary severity                   - Crash rate, severity rate

Target:                              Targets:
  - high_severity (0/1)               - crash_count (regression)
                                      - severity_rate (regression)
                                      - risk_score (regression)
                                      - risk_category (classification)
```

---

## Data Sources

Same as crash-level dataset:
- **Crash Data**: Kaggle US Accidents Dataset
- **Road Network**: OpenStreetMap via OSMnx
- **Traffic Counts**: TxDOT AADT Annual Stations

**Aggregation**: Created by `scripts/build_segment_dataset.py`

---

## Version Information

**Dataset Version**: 20251026_162447
**Script**: `scripts/build_segment_dataset.py`
**Source**: Crash-level train.csv (2016-2021)

---

## Contact

For questions, see `data/processed/README.md` or project documentation.
