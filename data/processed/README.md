# ML Datasets for Work Zone Crash Risk Prediction

This directory contains two complementary ML datasets for predicting work zone crash risk in Texas.

## Directory Structure

```
data/processed/
├── crash_level/        # Crash-level dataset (individual crashes)
│   ├── train_latest.csv → train_20251026_160909.csv
│   ├── val_latest.csv → val_20251026_160909.csv
│   └── test_latest.csv → test_20251026_160909.csv
│
└── segment_level/      # Segment-level dataset (aggregated by road segment + time)
    ├── segment_train_latest.csv → segment_train_20251026_162447.csv
    ├── segment_val_latest.csv → segment_val_20251026_162447.csv
    └── segment_test_latest.csv → segment_test_20251026_162447.csv
```

---

## 1. Crash-Level Dataset

**Purpose**: Learn which features predict crash severity at the individual crash level.

### Schema

- **Granularity**: 1 row = 1 crash event
- **Observations**: 1,135,762 crashes (2016-2023)
  - Train: 941,860 (2016-2021)
  - Val: 167,953 (2022)
  - Test: 25,949 (2023)
- **Features**: 78 columns
- **Target**: `high_severity` (binary: Severity >= 3)

### Key Feature Categories

| Category | Features | Source |
|----------|----------|--------|
| **Road Geometry** | highway_type, num_lanes, speed_limit, is_bridge, is_tunnel | OSMnx (OpenStreetMap) |
| **Traffic** | aadt, distance_to_aadt_m | TxDOT AADT Stations |
| **Temporal** | hour, day_of_week, month, year, is_weekend, is_rush_hour, time_of_day | Derived from crash timestamp |
| **Weather** | Temperature, Humidity, Visibility, Wind_Speed, weather_category, adverse_weather, low_visibility | Kaggle US Accidents |
| **Infrastructure** | Junction, Traffic_Signal, Stop, Crossing | OpenStreetMap tags |
| **Location** | City, Start_Lat, Start_Lng, is_urban | Crash report + derived |

### Target Variable

- **`Severity`**: 1-4 scale (1=minor, 4=severe traffic delay)
  - NOTE: This measures **traffic impact**, not injury severity
  - Source: Kaggle US Accidents dataset
- **`high_severity`**: Binary (1 if Severity >= 3, else 0)
  - Overall rate: 24.9% in train, 9.4% in val, 0.6% in test
  - ⚠️ Test set severely imbalanced (investigate why 2023 is different)

### Use Cases

✅ **Good for:**
- Feature importance analysis (which features matter most?)
- Understanding crash patterns
- Training crash severity classifiers
- Hypothesis testing (see FEATURE_HYPOTHESES.md)

❌ **Not suitable for:**
- Predicting risk for active work zones
- Interactive applications (need segment-level data)
- Deployment (row = crash that already happened)

### Example Usage

```python
import pandas as pd

# Load data
train = pd.read_csv('data/processed/crash_level/train_latest.csv')

# Features for modeling
feature_cols = [
    'highway_type', 'num_lanes', 'speed_limit', 'aadt',
    'is_rush_hour', 'adverse_weather', 'Temperature(F)',
    'is_urban', 'Junction', 'Traffic_Signal'
]

X = train[feature_cols]
y = train['high_severity']

# Train classifier
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)

# Feature importance
importances = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
```

---

## 2. Segment-Level Dataset

**Purpose**: Predict crash risk for road segments over time (for active work zones).

### Schema

- **Granularity**: 1 row = 1 road segment × 1 time period (quarterly)
- **Observations**: 303,281 segment-quarters (2016-2021)
  - Train: 303,281 (all data from train split)
  - Val: 0 (need to process val_latest.csv separately)
  - Test: 0 (need to process test_latest.csv separately)
- **Unique segments**: 75,650 road segments
- **Features**: 39 columns
- **Target**: Multiple risk metrics (crash_rate, severity_rate, traffic_impact, risk_score)

### Key Features

| Category | Features | Aggregation |
|----------|----------|-------------|
| **Crash Metrics** | crash_count, severity_rate, high_severity | Count, mean across crashes in segment-time |
| **Traffic Impact** | traffic_impact (= aadt × severity_rate), crash_density (per 1000 vehicles) | Calculated |
| **Road Features** | highway_type, num_lanes, speed_limit, is_bridge, is_tunnel | Mode/mean of crashes on segment |
| **Traffic** | aadt, distance_to_aadt_m | Mean across segment |
| **Temporal Patterns** | is_rush_hour, is_weekend, hour (all averaged across crashes in segment-time) | Mean proportion |
| **Weather Patterns** | adverse_weather, low_visibility, Temperature, Humidity, Visibility, Wind_Speed | Mean across crashes in segment-time |
| **Historical** | segment_crash_mean, segment_crash_std, segment_crash_max | Aggregated from all time periods for segment |

### Target Variables (Multiple)

1. **`crash_count`**: Number of crashes in segment-time
   - Mean: 3.1 crashes per segment-quarter
   - Range: 1 to 100+ for high-risk segments

2. **`severity_rate`**: Proportion of high-severity crashes
   - Mean: 19.02%
   - Use for: Predicting severity given a crash occurs

3. **`traffic_impact`**: AADT × severity_rate
   - Mean: 10,603
   - Use for: Estimating congestion risk
   - Interpretation: Higher = more vehicles affected by severe crashes

4. **`risk_score_simple`**: Composite score
   - Formula: `crash_count * 0.4 + severity_rate * 100 * 0.3 + traffic_impact / 1000 * 0.3`
   - Mean: 10.13
   - Range: 0 to 100+

5. **`risk_category`**: LOW / MEDIUM / HIGH / VERY_HIGH
   - Distribution: 68.9% LOW, 6.9% MEDIUM, 1.3% HIGH, 22.8% VERY_HIGH

### Segment Identifier

Segments are identified by:
- City
- highway_type (road class)
- num_lanes
- Geographic bin (lat/lon rounded to ~100m)

Example segment_id: `Houston_motorway_4_29.758_-95.423`

### Use Cases

✅ **Good for:**
- Predicting risk for active work zones
- Interactive applications (user draws polygon → get risk score)
- Resource allocation (which work zones need extra precautions?)
- Temporal analysis (best time to schedule work zones)

❌ **Not suitable for:**
- Understanding individual crash factors (use crash-level)
- Fine-grained severity prediction (segment averages smooth details)

### Example Usage

```python
import pandas as pd

# Load data
seg_train = pd.read_csv('data/processed/segment_level/segment_train_latest.csv')

# Features for modeling
feature_cols = [
    'highway_type', 'num_lanes', 'speed_limit', 'aadt',
    'is_rush_hour', 'adverse_weather', 'Temperature(F)',
    'segment_crash_mean', 'segment_crash_std'
]

X = seg_train[feature_cols]

# Multiple targets
y_crash_count = seg_train['crash_count']
y_severity_rate = seg_train['severity_rate']
y_traffic_impact = seg_train['traffic_impact']

# Train regressor for crash count
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor()
model.fit(X, y_crash_count)

# Predict for new work zone
new_work_zone = pd.DataFrame({
    'highway_type': ['motorway'],
    'num_lanes': [4],
    'speed_limit': [65],
    'aadt': [75000],
    'is_rush_hour': [0.6],  # 60% of crashes in this segment are rush hour
    'adverse_weather': [0.2],  # 20% of time has adverse weather
    'Temperature(F)': [78],
    'segment_crash_mean': [5.0],
    'segment_crash_std': [2.3]
})

predicted_crashes = model.predict(new_work_zone)
print(f"Expected crashes per quarter: {predicted_crashes[0]:.1f}")
```

---

## Dataset Relationship

The two datasets are **complementary**:

```
┌─────────────────────────────────────┐
│     Crash-Level Dataset             │
│  (Learn feature importance)         │
│                                     │
│  Input: Individual crash features   │
│  Output: Severity classification    │
│  Use: Feature discovery             │
└─────────────────────────────────────┘
              ↓
         Features that matter most
              ↓
┌─────────────────────────────────────┐
│    Segment-Level Dataset            │
│  (Predict work zone risk)           │
│                                     │
│  Input: Road segment features       │
│  Output: Crash rate, severity, etc. │
│  Use: Deployment & planning         │
└─────────────────────────────────────┘
```

### Recommended Workflow

1. **Phase 1: Feature Discovery**
   - Use crash-level dataset
   - Train classifiers (Random Forest, XGBoost, etc.)
   - Analyze feature importances
   - Validate hypotheses (FEATURE_HYPOTHESES.md)

2. **Phase 2: Segment Modeling**
   - Use segment-level dataset
   - Train regressors for crash_count, severity_rate, traffic_impact
   - Build ensemble model for composite risk score
   - Evaluate on different road types, cities, time windows

3. **Phase 3: Deployment**
   - Interactive application
   - User draws work zone polygon on map
   - System extracts segment features (OSMnx + AADT)
   - Model predicts risk score
   - Recommendations: "HIGH RISK: Schedule at night, add extra signage"

---

## Data Quality Notes

### Completeness

| Feature | Crash-Level | Segment-Level |
|---------|-------------|---------------|
| highway_type | 68.3% | 100% |
| num_lanes | 51.5% | 35.4% |
| speed_limit | 23.8% | 16.6% |
| aadt | 100% | 100% |
| Temperature | 98.3% | 98.8% |

### Known Issues

1. **Test set imbalance**: 2023 test set has only 0.6% high-severity crashes (vs 24.9% in train)
   - Investigation needed: Why is 2023 different?
   - Possible causes: Data collection change, COVID recovery patterns, reporting changes

2. **Missing road features**:
   - speed_limit: 76% missing (OSM data incomplete)
   - num_lanes: 49% missing (crash-level), 65% missing (segment-level)
   - Strategies: Imputation, auxiliary data sources, or exclude from models

3. **Segment val/test splits**: Currently empty
   - Need to run `build_segment_dataset.py` on val_latest.csv and test_latest.csv
   - Command: `python scripts/build_segment_dataset.py --input data/processed/crash_level/val_latest.csv`

---

## Building Datasets

### Crash-Level Dataset

```bash
# Build from raw crash data
python scripts/build_ml_training_dataset.py \
  --crash-file data/raw/texas/crashes/kaggle_us_accidents_texas.csv \
  --aadt-file data/raw/texas/traffic/txdot_aadt_annual.gpkg \
  --cities Houston Dallas Austin "San Antonio" "Fort Worth" "El Paso" Arlington Mesquite Irving \
  --output-dir data/processed/crash_level

# Test with sample
python scripts/build_ml_training_dataset.py --sample 10000
```

### Segment-Level Dataset

```bash
# Build from crash-level data
python scripts/build_segment_dataset.py

# Options
python scripts/build_segment_dataset.py --time-window monthly  # or quarterly, yearly
python scripts/build_segment_dataset.py --min-crashes 5        # filter low-crash segments
python scripts/build_segment_dataset.py --sample 10000         # test with sample

# Build val and test splits
python scripts/build_segment_dataset.py --input data/processed/crash_level/val_latest.csv
python scripts/build_segment_dataset.py --input data/processed/crash_level/test_latest.csv
```

---

## Citations

### Data Sources

- **Crash Data**: Kaggle US Accidents Dataset (Moosavi et al., 2019)
- **Traffic Data**: TxDOT AADT Annual Stations
- **Road Networks**: OpenStreetMap via OSMnx (Boeing, 2017)
- **Work Zones**: TxDOT WZDx Feed (Work Zone Data Exchange)

### References

- Moosavi, Sobhan, et al. "A Countrywide Traffic Accident Dataset." 2019.
- Boeing, G. "OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks." Computers, Environment and Urban Systems, 2017.

---

## Contact

For questions or issues with these datasets, see project documentation or open an issue.

**Last Updated**: 2025-10-26
