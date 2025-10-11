# ML/DL Data Sources Strategy for Work Zone Safety Prediction

**Project**: Work Zone Safety Prediction/Forecasting App
**Purpose**: Data integration strategy for machine learning models
**Date**: October 10, 2025

---

## Project Goal

Build a machine learning/deep learning tool to **predict crash risk** in work zones based on:
- Work zone characteristics (location, type, duration, lane closures)
- Environmental conditions (weather, time, traffic)
- Road characteristics (geometry, history)
- Real-time conditions (for forecasting)

---

## Current Data Inventory

### ✅ What You Have
1. **Work Zone Data** (3 states)
   - California: 1,186 zones (WZDx, excellent quality)
   - Texas: 288 unique zones (2,180 records)
   - New York: 1,138 zones

2. **Crash Data** (California only)
   - Alameda County: 17,161 crashes (2023-2025)
   - 214 fatalities, 22,589 injuries
   - 65% with coordinates

3. **Geographic Coverage**
   - Strong: Bay Area, California
   - Moderate: Texas cities, NY highways
   - Gap: Most other regions

### ❌ What's Missing (Critical for ML)
1. **Traffic volume/exposure** - Can't normalize risk without this
2. **Weather data** - Major crash contributor
3. **Road characteristics** - Geometry, baseline risk
4. **Temporal features** - Need more structured time data
5. **More crash data** - Only have 1 county, need more training data

---

## Recommended Data Sources (Prioritized)

### 🔴 TIER 1: Critical + Feasible (Must Have)

These are essential for any ML model and are publicly accessible.

#### 1. Traffic Volume (AADT - Annual Average Daily Traffic)

**Why Critical**:
- Exposure metric - 100K vehicles/day vs 10K has 10x exposure
- Can't compare crash risk without normalizing by traffic
- Feature for ML models + denominator for crash rate

**Sources**:
- **FHWA HPMS** (Highway Performance Monitoring System)
  - URL: https://www.fhwa.dot.gov/policyinformation/hpms.cfm
  - Coverage: All US highways
  - Format: CSV/Shapefile
  - Free: Yes
  - Contains: AADT, truck %, vehicle classification

- **State DOT Traffic Count Maps**
  - California: https://dot.ca.gov/programs/traffic-operations/census
  - Texas: https://www.txdot.gov/data-maps/traffic-counts.html
  - More detailed than HPMS

- **OpenTraffic** (crowdsourced)
  - URL: https://github.com/opentraffic
  - Real-time + historical

**What to Extract**:
- AADT (total vehicles/day)
- Truck percentage
- Peak hour volume
- Vehicle mix (cars vs trucks)

**Integration Approach**:
- Spatial join: Match work zones to nearest road segment
- Use AADT as feature for ML
- Calculate crash rate = crashes / (AADT × days × length)

---

#### 2. Weather Data (Historical + Real-time)

**Why Critical**:
- Rain, snow, fog increase crash risk 2-10x
- Temperature affects road conditions
- Wind affects large vehicles
- Essential feature for prediction

**Sources**:

**NOAA ISD (Integrated Surface Database)**
- URL: https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database
- Coverage: Global, 1901-present
- Format: CSV
- Free: Yes
- Contains: Temperature, precipitation, visibility, wind, pressure

**NOAA LCD (Local Climatological Data)**
- URL: https://www.ncdc.noaa.gov/cdo-web/datatools/lcd
- More detailed than ISD for US stations

**Weather.gov API** (Real-time)
- URL: https://www.weather.gov/documentation/services-web-api
- Free, no authentication required
- Current + 7-day forecast
- Perfect for real-time predictions

**OpenWeatherMap API**
- URL: https://openweathermap.org/api
- Free tier: 1000 calls/day
- Historical + forecast + current

**What to Extract**:
- Precipitation (yes/no, intensity)
- Visibility (fog indicator)
- Temperature
- Wind speed
- Road surface conditions (if available)
- Aggregated conditions (last 1hr, 3hr, 6hr before crash)

**Integration Approach**:
- Match weather station to crash location (nearest or interpolate)
- For each crash: get weather at time of crash
- For each work zone: get weather conditions (hourly snapshots)
- Features: precipitation_1hr, temp, visibility, wind
- Time-lagged features: weather_3hr_prior (captures changing conditions)

---

#### 3. Road Characteristics (Geometry + Infrastructure)

**Why Critical**:
- Some locations inherently more dangerous (curves, merges)
- Speed limit, lanes, road type affect base crash risk
- Work zones modify existing risk, need baseline

**Sources**:

**OpenStreetMap (OSM)**
- URL: https://www.openstreetmap.org
- Coverage: Global
- Format: XML/PBF, via Overpass API or Python libraries
- Free: Yes
- Contains: Road type, lanes, speed limit, geometry, intersections

**Python Libraries**:
```python
import osmnx as ox
# Get road network
G = ox.graph_from_place("Alameda County, California", network_type='drive')
# Extract features: lanes, speed limit, road type
```

**TIGER/Line (Census Bureau)**
- URL: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- US road network with attributes
- Shapefiles

**State DOT Road Inventory**
- California: https://dot.ca.gov/programs/design/highway-design-manual
- Contains: Functional class, design speed, shoulders, median

**What to Extract**:
- Number of lanes (baseline)
- Posted speed limit (not work zone reduced)
- Road type (interstate, arterial, local)
- Functional class
- Shoulder width
- Presence of median
- Intersection density
- Curvature (can calculate from geometry)
- Grade/slope (if available)

**Integration Approach**:
- Spatial join work zones/crashes to road network
- Extract features for each location
- Create "road complexity score" (curves, intersections, merges)

---

#### 4. Temporal Features (Engineered from Date/Time)

**Why Critical**:
- Rush hour vs off-peak dramatically different risk
- Weekday vs weekend patterns
- Seasonal patterns (summer road trips, winter conditions)
- Holidays affect traffic volume and driver behavior

**What to Create** (from existing datetime fields):
- Hour of day (0-23)
- Day of week (0-6)
- Month (1-12)
- Quarter (1-4)
- Weekend flag (yes/no)
- Rush hour flags:
  - Morning rush (6-9 AM)
  - Evening rush (4-7 PM)
  - Off-peak
- Holiday flags:
  - Federal holidays
  - School holidays
  - Local events (sports games, concerts)

**Additional Sources**:

**Holiday Calendar**
- Python: `holidays` library
```python
import holidays
us_holidays = holidays.US()
is_holiday = date in us_holidays
```

**School Calendar** (if near schools)
- State department of education websites
- Impact: Traffic patterns change during school sessions

**Event Data** (optional)
- Ticketmaster API for concerts/sports
- Local event calendars
- Captures traffic surges

**Integration Approach**:
- Feature engineering from crash/work zone datetime
- Cyclical encoding for hour/month (sin/cos transformation)
- Interaction features: rush_hour × rain (especially dangerous)

---

### 🟡 TIER 2: Important + Moderate Effort (Should Have)

These significantly improve model performance but require more effort.

#### 5. Real-Time Traffic Speed/Congestion

**Why Important**:
- Sudden slowdowns near work zones → rear-end crashes
- Speed variance = crash risk indicator
- Congestion affects driver frustration
- Critical for REAL-TIME prediction

**Sources**:

**HERE Traffic API**
- URL: https://developer.here.com/products/traffic-api
- Free tier available
- Real-time speeds + incidents + flow

**INRIX**
- URL: https://inrix.com
- Commercial (expensive)
- Best quality traffic data
- Used by DOTs

**State DOT 511 Systems**
- California 511: Traffic sensors every 0.5 mile on highways
- Texas: TxDOT Traffic Cameras
- Often have APIs (free but rate-limited)

**Waze for Cities**
- URL: https://www.waze.com/ccp
- Free for government/academic
- Crowdsourced speeds, incidents, hazards
- Must apply for access

**Google Traffic Data** (via Maps API)
- Not free, rate limited
- Accurate but expensive for large-scale

**What to Extract**:
- Current speed vs speed limit (speed ratio)
- Speed variance (standard deviation over 5-10 min)
- Deceleration rate approaching work zone
- Queue length (if available)
- Congestion level (free-flow, moderate, heavy, stopped)

**Integration Approach**:
- Real-time: Query API for work zone location, get current conditions
- Historical: Archive traffic data over time (build your own dataset)
- Features: speed_ratio, speed_variance, congestion_level
- Time-series features: speed_change_5min, speed_change_15min

---

#### 6. Historical Crash Baseline (Location-Specific Risk)

**Why Important**:
- Some locations inherently dangerous (poor visibility, sharp curves)
- Baseline crash rate before work zone = feature
- "Hot spot" identification

**Sources**:

**Expand Your TIMS Data**
- Get more counties in California
- Get more years (2020-2025 instead of just 2023-2025)
- Broader coverage = more training data

**FARS (Fatality Analysis Reporting System)**
- URL: https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars
- All US fatal crashes since 1975
- Free, detailed
- Good for severe outcomes

**State DOT Crash Databases**
- Most states publish crash data
- Texas: TxDOT CRIS (Crash Records Information System)
- New York: NYS DMV crash data
- Apply for access (usually free for research)

**NHTSA CRSS (Crash Report Sampling System)**
- URL: https://www.nhtsa.gov/research-data/crash-report-sampling-system-crss
- Sample of all police-reported crashes
- US-wide coverage

**What to Extract**:
- Crash history at each road segment (3-year lookback)
- Crash rate per mile per year (before work zone)
- Severity distribution (% fatal, injury, PDO)
- Crash types (rear-end, sideswipe, angle) at location

**Integration Approach**:
- Calculate baseline crash rate for each road segment
- Feature: `baseline_crash_rate` (crashes per 100M vehicle-miles)
- Feature: `location_risk_score` (percentile of crash rate)
- Then model predicts: work zone crash risk = f(baseline_risk, work_zone_features, weather, traffic, ...)

---

### 🟢 TIER 3: Nice-to-Have + High Effort (Future Work)

These are cutting-edge but may be too ambitious for capstone scope.

#### 7. Satellite/Aerial Imagery (for Deep Learning)

**Why Interesting**:
- Visual features hard to quantify (signage quality, visibility, barriers)
- CNN/Vision Transformer models
- Could detect poor work zone setup

**Sources**:
- Sentinel-2 (ESA): 10m resolution, free
- Landsat (NASA/USGS): 30m resolution, free
- Google Earth Engine: API access to imagery
- Mapbox Static Images API: Satellite + streets

**Challenges**:
- Large data volumes (GBs of imagery)
- Preprocessing complex (crop, align, augment)
- Need labeled dataset (work zones with/without crashes)
- Compute intensive (need GPU)

**Recommendation**: Skip for capstone unless you have CV experience.

---

#### 8. Connected Vehicle Data (CAV/CV)

**Why Cutting-Edge**:
- Hard braking events = near-miss proxy
- Speed variance from fleet data
- Leading indicators before crashes occur

**Sources**:
- USDOT Connected Vehicle Pilot Program
- Waze for Cities (some near-miss data)
- Fleet telematics (commercial trucks)

**Challenges**:
- Limited public availability
- Privacy restrictions
- Sparse coverage

**Recommendation**: Explore if time permits, but not critical.

---

## Data Integration Architecture

### Recommended Database Schema

```
┌─────────────────┐
│  work_zones     │
├─────────────────┤
│ id              │
│ location (geom) │
│ start_date      │
│ end_date        │
│ vehicle_impact  │
│ lanes_closed    │
│ workers_present │
│ aadt           │ ← from traffic data
│ speed_limit    │ ← from OSM
│ road_type      │ ← from OSM
│ baseline_crash │ ← from historical crashes
│ ...             │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│ work_zone_      │
│ conditions      │ (time-series)
├─────────────────┤
│ work_zone_id    │
│ timestamp       │
│ temperature     │ ← from weather API
│ precipitation   │
│ visibility      │
│ traffic_speed   │ ← from traffic API
│ congestion      │
│ ...             │
└─────────────────┘

┌─────────────────┐
│  crashes        │
├─────────────────┤
│ id              │
│ location (geom) │
│ datetime        │
│ severity        │
│ weather         │ ← joined from weather
│ road_type       │ ← joined from OSM
│ traffic_volume  │ ← joined from AADT
│ near_work_zone  │ ← spatial join (flag)
│ work_zone_id    │ ← if in work zone
│ ...             │
└─────────────────┘
```

### Data Pipeline (Recommended Tools)

```python
# 1. Data Collection
# - Work zones: WZDx feeds (existing)
# - Crashes: TIMS, FARS, state DOTs
# - Traffic: HPMS download, state DOT APIs
# - Weather: NOAA API, Weather.gov API
# - Roads: OSM via osmnx

# 2. Storage
# - PostgreSQL + PostGIS (spatial database)
# - Or: GeoPandas → Parquet files (simpler)

# 3. Feature Engineering
import pandas as pd
import geopandas as gpd
import numpy as np

# Spatial join work zones to crashes
work_zones_gdf = gpd.GeoDataFrame(...)
crashes_gdf = gpd.GeoDataFrame(...)

# Buffer work zones (e.g., 100m)
wz_buffered = work_zones_gdf.buffer(100)
crashes_in_wz = gpd.sjoin(crashes_gdf, wz_buffered, predicate='within')

# Temporal join weather
crashes['weather'] = crashes.apply(
    lambda row: get_weather(row['location'], row['datetime']),
    axis=1
)

# 4. Feature Store
# Save engineered features for ML
features_df.to_parquet('features.parquet')
```

---

## ML Model Recommendations

### Phase 1: Baseline (Start Here)

**Task**: Binary classification (crash vs no crash) or crash risk score (0-1)

**Model**: Gradient Boosting (XGBoost, LightGBM, CatBoost)

**Why**:
- Best performance on tabular data
- Handles mixed feature types
- Feature importance built-in
- Fast training, good interpretability

**Features** (aim for 30-50 features):
- Work zone: vehicle_impact, lanes_closed, duration, workers_present
- Traffic: aadt, truck_pct, peak_hour_flag
- Weather: precipitation, temperature, visibility, wind
- Temporal: hour, day_of_week, month, rush_hour_flag, holiday_flag
- Road: speed_limit, lanes, road_type, functional_class, baseline_crash_rate
- Spatial: distance_to_intersection, curvature, urban_rural_flag

**Target Variable Options**:
1. Binary: crash occurred (yes/no) in work zone
2. Multi-class: crash severity (none/PDO/injury/fatal)
3. Count: number of crashes (Poisson regression)
4. Risk score: predicted crash rate per 1000 vehicle-days

**Code Skeleton**:
```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_recall_curve

# Prepare data
X = features_df[feature_columns]
y = features_df['crash_occurred']  # or 'crash_severity'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = xgb.XGBClassifier(
    max_depth=6,
    learning_rate=0.1,
    n_estimators=100,
    objective='binary:logistic',
    eval_metric='auc'
)

model.fit(X_train, y_train)

# Evaluate
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_proba)
print(f"AUC: {auc:.3f}")

# Feature importance
import matplotlib.pyplot as plt
xgb.plot_importance(model, max_num_features=20)
plt.show()
```

---

### Phase 2: Time-Series (If You Have Sequential Data)

**Task**: Predict crashes in next hour/day given recent conditions

**Model**: LSTM, GRU, or Temporal Convolutional Network (TCN)

**Why**:
- Capture temporal dependencies (traffic building up → crash)
- Model sequences of weather/traffic changes
- Good for forecasting

**Data Structure**:
- Sequences of traffic/weather conditions (e.g., last 24 hours in 1-hour intervals)
- Each sequence → crash outcome (yes/no)

**Features**:
- Time-series: traffic_speed[t-24:t], weather[t-24:t]
- Static: work_zone_features, road_features

**Code Skeleton**:
```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Prepare sequences
X_sequences = []  # shape: (n_samples, 24, n_features)
y_targets = []    # shape: (n_samples,)

# For each work zone hour
for wz in work_zones:
    for t in range(24, len(wz.conditions)):
        X_sequences.append(wz.conditions[t-24:t])  # last 24 hours
        y_targets.append(wz.had_crash_at[t])

X_sequences = np.array(X_sequences)
y_targets = np.array(y_targets)

# Build LSTM model
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(24, n_features)),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['AUC'])
model.fit(X_sequences, y_targets, epochs=20, batch_size=32, validation_split=0.2)
```

**When to Use**: If you collect hourly traffic/weather data for work zones.

---

### Phase 3: Spatial Models (Advanced)

**Task**: Predict crashes considering spatial relationships (nearby work zones, network effects)

**Model**: Graph Neural Networks (GNN) or Spatial Autoregressive Models

**Why**:
- Crashes can cluster spatially
- Work zone on one road affects nearby roads (detours, spillover)
- Road network structure matters

**Challenges**: Complex implementation, may be too advanced for capstone.

---

## Implementation Roadmap for Capstone

### Month 1-2: Data Collection & Integration
**Week 1-2**:
- ✅ Collect work zone data (done!)
- ✅ Collect crash data (done for CA!)
- ⏳ Expand crash data (more counties/states if possible)

**Week 3-4**:
- Download HPMS traffic volume data
- Set up NOAA weather API access
- Extract OSM road characteristics for study areas

**Week 5-6**:
- Build data integration pipeline
- Spatial joins (work zones ↔ crashes ↔ roads)
- Temporal joins (weather at crash time)

**Week 7-8**:
- Feature engineering
- Handle missing data
- Exploratory data analysis (correlations, distributions)

### Month 3: Modeling
**Week 9-10**:
- Train baseline XGBoost model
- Cross-validation, hyperparameter tuning
- Feature importance analysis

**Week 11-12**:
- Improve model (more features, ensemble methods)
- Evaluate on test set
- Interpret results (SHAP values)

### Month 4: Application & Presentation
**Week 13-14**:
- Build prediction API/tool (Flask or Streamlit)
- Create dashboard for visualizing predictions
- Real-time prediction demo (using weather API)

**Week 15-16**:
- Final report/presentation
- Document methodology
- Discuss limitations & future work

---

## Quick Start: Minimum Viable Dataset

If you want to start modeling NOW with what you have:

### Option A: California-Only Model (Feasible This Week)

**Data You Have**:
- ✅ CA work zones (1,186)
- ✅ CA crashes (17,161)
- ✅ Coordinates for both

**Add These (Easy Wins)**:
1. **Temporal features** (engineer from datetime) - 1 hour work
2. **Weather data** (NOAA API for past dates) - 1-2 days work
3. **OSM road features** (python osmnx) - 1 day work

**Result**: ~30-40 features, ready for XGBoost

**Quick Implementation**:
```python
# 1. Spatial join crashes to work zones
crashes_near_wz = gpd.sjoin(crashes_gdf, workzones_gdf.buffer(100), predicate='within')

# 2. Get weather for each crash
def get_historical_weather(lat, lon, datetime):
    # Use NOAA LCD or OpenWeatherMap historical API
    pass

crashes['weather'] = crashes.apply(lambda row: get_historical_weather(...), axis=1)

# 3. Get OSM road features
import osmnx as ox
G = ox.graph_from_place("Alameda County, California", network_type='drive')
# Extract features for each crash location

# 4. Feature engineering
crashes['hour'] = crashes['datetime'].dt.hour
crashes['day_of_week'] = crashes['datetime'].dt.dayofweek
crashes['is_weekend'] = crashes['day_of_week'] >= 5
crashes['is_rush_hour'] = crashes['hour'].isin([7,8,9,16,17,18])

# 5. Create samples
# Positive: crashes near work zones
# Negative: random points near work zones without crashes (or time periods without crashes)

# 6. Train model
import xgboost as xgb
model = xgb.XGBClassifier()
model.fit(X_train, y_train)
```

---

## Key Recommendations Summary

### Must-Have Data (Priority 1):
1. ✅ Work zones (you have)
2. ✅ Crashes (you have, expand if possible)
3. ⚠️ **Traffic volume (AADT)** - GET THIS FIRST
4. ⚠️ **Weather data** - GET THIS SECOND
5. ⚠️ **Road characteristics (OSM)** - GET THIS THIRD
6. ✅ Temporal features (engineer from datetime) - EASY

### Should-Have Data (Priority 2):
7. Real-time traffic speeds (nice for real-time predictions)
8. Historical crash baseline (improve accuracy)

### Nice-to-Have (Priority 3):
9. Satellite imagery (if doing deep learning)
10. Connected vehicle data (if available)

### Recommended First Model:
- **XGBoost classifier**: Predict crash likelihood in work zone
- **Features**: Work zone characteristics + weather + temporal + road + traffic volume
- **Target**: Binary (crash yes/no) or severity (none/injury/fatal)
- **Evaluation**: AUC-ROC, precision-recall, feature importance

### For Your App:
- Backend: Flask API serving XGBoost model
- Frontend: Map showing work zones color-coded by predicted risk
- Real-time: Query weather API, traffic API → generate prediction → display
- Offline: Batch predictions for all work zones daily

---

## Resources & APIs Quick Reference

| Data Type | Best Source | Cost | Ease |
|-----------|------------|------|------|
| Traffic Volume | FHWA HPMS | Free | Easy |
| Weather | NOAA/Weather.gov | Free | Easy |
| Roads | OpenStreetMap | Free | Easy |
| Crashes | TIMS, FARS, State DOTs | Free | Moderate |
| Real-time Traffic | State 511, Waze | Free* | Moderate |
| Satellite Imagery | Sentinel, Landsat | Free | Hard |

*Rate limited or application required

---

## Next Steps

1. **Decide on scope**: CA-only or multi-state?
2. **Get traffic data**: Download HPMS for your states
3. **Get weather data**: Set up NOAA API, backfill historical weather
4. **Feature engineering**: Build the feature matrix
5. **Baseline model**: Train XGBoost, evaluate, iterate

Want me to help you implement any of these data integrations? I can create scripts to fetch HPMS data, query weather APIs, or extract OSM features!
