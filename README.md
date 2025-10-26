# Work Zone Safety & Traffic Impact Prediction

**Team IntelliZone** - MADS Capstone Fall 2025

Predicting crash risk and traffic congestion near active highway work zones using machine learning.

---

## 🎯 Project Goal

Improve road safety and operations during highway construction by:
1. Predicting crash likelihood in work zones
2. Forecasting traffic congestion and delays
3. Providing actionable insights for DOT planners and drivers

**Value**: Show how data-driven intelligence makes road construction zones safer and more predictable.

---

## ❓ Research Questions

1. **Which factors influence crash risk during work zones?**
   - Lane closures, weather, traffic volume, time of day, work zone characteristics

2. **How accurately can we predict congestion and delays?**
   - Traffic slowdowns, bottlenecks, delay duration and severity

3. **How can we provide actionable insights?**
   - High-risk zone identification, data-driven decision support, traffic management

---

## 📊 Current Status

**Phase**: Data Exploration & Source Identification (Phase 0)

### ✅ Completed
- WZDx feed discovery (TX, CA, NY)
- Texas data collection: 1,829 work zones, 41K AADT stations
- Initial AADT integration (67.7% match rate)
- Exploratory dashboard (Texas-only)

### 🔄 In Progress
- Multi-state data source assessment
- Crash data source selection
- Project scope finalization

### ⏳ Next
- Data collection (2-3 states)
- Crash data integration
- Weather data collection
- ML model development

---

## 🚀 Quick Start

### Run Dashboard
```bash
# Install dependencies
pip install -r requirements.txt

# Run Texas exploratory dashboard
streamlit run app.py

# Opens at http://localhost:8501
```

### Data Collection Scripts
```bash
# Download Texas AADT data
python scripts/download_txdot_aadt_annual.py

# Integrate with work zones
python scripts/integrate_texas_aadt.py
```

---

## 📁 Project Structure

```
Capstone/
├── README.md                   # This file
├── PROJECT_STATUS.md           # ⭐ Master reference - detailed status
├── requirements.txt            # Dependencies
│
├── app.py                      # Streamlit dashboard (Texas)
├── config.py                   # Dashboard config
├── pages/ (3 files)            # Dashboard pages
├── utils/ (3 files)            # Dashboard utilities
│
├── data/
│   ├── processed/              # texas_work_zones_with_aadt.csv
│   └── raw/                    # Original data by state
│
├── scripts/                    # Data processing scripts
├── docs/                       # Documentation
└── src/                        # Source modules
```

---

## 📊 Data Sources

### 1. Work Zone Data
- **Source**: WZDx Feed Registry
- **States**: Texas ✅, California 🔄, New York 🔄
- **Features**: Location, lane closures, dates, work type

### 2. Crash Data
**Evaluating**:
- NCSA FARS (fatal crashes nationwide)
- State DOT databases (comprehensive)
- Kaggle US Accidents dataset

### 3. Traffic Data
- **Source**: HPMS / State DOT
- **Texas**: 41,467 AADT stations ✅
- **Features**: Traffic volume, vehicle classification

### 4. Weather Data
- **Source**: NOAA NCEI
- **Features**: Precipitation, temperature, visibility

### 5. Optional
- OpenStreetMap (road characteristics)
- Census data (demographics)

---

## 🎯 Deliverables (MVP)

### 1. Interactive Dashboard (Streamlit)
- Geospatial visualization
- Work zones, crashes, risk heatmaps
- ML predictions display
- Multi-state support

### 2. ML Model (Target: AUC-ROC > 0.70)
- **Crash Risk Classifier**: Predict crash likelihood
- **Congestion Predictor**: Predict traffic delays
- Feature importance analysis (SHAP)

### 3. Documentation
- Technical report
- Model methodology
- Code repository
- User guide

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **Pandas & GeoPandas**: Data processing
- **Streamlit**: Interactive dashboard
- **Plotly & Folium**: Visualizations
- **XGBoost**: ML models
- **SHAP**: Model interpretability

---

## 📅 Timeline

### October 2025 (Current)
- ✅ Data source exploration
- ✅ Texas data collection
- 🔄 Multi-state assessment
- 🔄 Crash data source selection

### November 2025
- Multi-state data collection
- Crash data integration
- Weather data collection
- Feature engineering
- ML dataset creation

### December 2025
- ML model training
- Model evaluation
- Dashboard with predictions
- Final report & presentation

---

## 👥 Team

**Team IntelliZone**
- Julien Hovan (jhovan@umich.edu) - Data Engineer, Software Engineer
- Zahra Ahmed (zahraf@umich.edu)
- Deepthi Kurup (drkurup@umich.edu)

**Team Number**: SIADS 699 234 FA 2025

---

## 📚 Documentation

**Essential Docs**:
- **PROJECT_STATUS.md** ⭐ - Comprehensive status, roadmap, decisions
- **docs/DATA_INTEGRATION_GUIDE.md** - Data integration technical details
- **docs/DASHBOARD_GUIDE.md** - Dashboard usage guide
- **docs/PROJECT_PROPOSAL.md** - Original detailed proposal

**Quick Reference**:
```bash
# View master status document
cat PROJECT_STATUS.md

# Data integration details
cat docs/DATA_INTEGRATION_GUIDE.md

# Dashboard guide
cat docs/DASHBOARD_GUIDE.md
```

---

## 📊 Texas Dataset (Current)

**File**: `data/processed/texas_work_zones_with_aadt.csv`

**Stats**:
- 1,829 work zones (Jan-Apr 2024)
- 254 counties
- 67.7% AADT direct match rate
- Mean AADT: 31,887 vehicles/day
- 25 feature columns

**Features**:
- Location, temporal, work zone characteristics
- Traffic volume (AADT), categories (5 levels)
- Risk metrics (exposure score, VMT)

---

## 🎯 Success Criteria

### Model Performance
- AUC-ROC > 0.70
- Outperform baseline models
- F1 score optimization

### Feature Importance
- Top 5-10 predictive features
- Intuitive interpretability
- SHAP value analysis

### Dashboard
- Error-free operation
- Interactive functionality
- Usability validation

---

## ⚠️ Known Challenges

### Data
- Spatial alignment across states
- Temporal joins (weather to crashes)
- Missing data handling
- Inconsistent schemas

### Model
- Class imbalance (rare crash events)
- Model interpretability
- Overfitting risk

### Ethics
- Privacy concerns (PII in crash data)
- Prediction misuse potential
- Historical bias in data

**Mitigation**: See PROJECT_STATUS.md for detailed strategies

---

## 🔗 Key Resources

- **WZDx Specification**: https://github.com/usdot-jpo-ode/wzdx
- **WZDx Feed Registry**: https://datahub.transportation.gov/
- **NCSA FARS**: https://crashstats.nhtsa.dot.gov/
- **HPMS**: https://www.fhwa.dot.gov/policyinformation/hpms.cfm
- **NOAA Weather**: https://www.ncei.noaa.gov/access

---

## 📝 Key Decisions Needed

1. **Which states?** TX only vs. TX+CA vs. TX+CA+NY
2. **Crash data source?** FARS vs. State DOT vs. Kaggle
3. **Real-time strategy?** Historical data with optional live display

**See PROJECT_STATUS.md for detailed decision framework**

---

## 🚧 Project Notes

- **Current Phase**: Data exploration (Phase 0)
- **Focus**: Multi-state data assessment
- **Priority**: Finalize data sources this week
- **Dashboard**: Texas-only exploratory tool (will expand)

---

**For comprehensive project details, status, and roadmap, see `PROJECT_STATUS.md` ⭐**

**University of Michigan - MADS Capstone - Fall 2025**
