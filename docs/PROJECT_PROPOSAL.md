# MADS Capstone Project Proposal
## Work Zone Safety Prediction & Geospatial Visualization Platform

**Team Name**: Team Transport
**Date**: October 10, 2025

---

## 1. Project Name and Team

**Project Name**: SafeZone - Work Zone Safety Prediction Platform

**Team**: Team Transport

---

## 2. Project Overview

### Subject and Research Questions

Highway work zones are necessary for infrastructure maintenance but create significant safety risks. According to FHWA, work zone crashes result in approximately 70,000 injuries and 700 fatalities annually in the United States. Our project aims to develop a machine learning-powered prediction and visualization platform that provides **real-time safety risk assessments for active work zones**.

**Key Questions We Aim to Answer**:

1. **What factors most strongly predict crash risk in work zones?**
   - Vehicle impact level (lane closures)
   - Weather conditions (precipitation, visibility)
   - Traffic volume and congestion
   - Temporal patterns (time of day, day of week)
   - Road characteristics (geometry, speed limits)
   - Work zone characteristics (duration, worker presence)

2. **Can we predict crash likelihood in work zones before they occur?**
   - Build ML model to forecast crash probability given current conditions
   - Identify high-risk work zones requiring additional safety measures

3. **How can we effectively communicate risk to decision-makers?**
   - Create intuitive geospatial visualizations
   - Provide real-time risk scores accessible via web dashboard
   - Enable data-driven resource allocation (enforcement, signage, warnings)

**Target Audience**: State DOT traffic safety personnel, highway maintenance planners, policy makers, and transportation researchers seeking to reduce work zone crashes through predictive analytics.

**Impact**: By identifying high-risk work zones in near real-time, our tool enables proactive interventions (increased enforcement, enhanced signage, variable message boards, optimal scheduling) to prevent crashes before they occur.

---

## 3. Datasets

### Primary Datasets

#### 3.1 Work Zone Data
**Source**: Work Zone Data Exchange (WZDx) Feed Registry
**URL**: https://datahub.transportation.gov/Roadways-and-Bridges/Work-Zone-Data-Exchange-WZDx-Feed-Registry/69qe-yiui/about_data

**Coverage**:
- California 511 API: ~1,200 active work zones (Bay Area)
- Texas DOT: ~300 unique work zones (statewide)
- New York 511: ~1,100 work zones (statewide)
- Additional states available through registry

**Features**:
- Geographic location (coordinates, road segments)
- Temporal data (start date, end date, update frequency)
- Work zone characteristics (vehicle impact, lane closures, worker presence)
- Road identification (route names, directions, mileposts)
- Work type descriptions

**Access Method**:
- Real-time API feeds (California, some states)
- CSV/GeoJSON downloads (Texas, others)
- Historical archives via USDOT S3 bucket

**Plan**: Integrate feeds from 2-3 states, focus initially on California (best data quality) for model development, expand to Texas and New York for validation.

---

#### 3.2 Crash Data
**Source**: Transportation Injury Mapping System (TIMS - UC Berkeley) + NHTSA FARS
**URLs**:
- TIMS: https://tims.berkeley.edu/
- FARS: https://crashstats.nhtsa.dot.gov/#!/
- Data.gov: https://catalog.data.gov/dataset/?tags=crash

**Coverage**:
- Current: Alameda County, CA - 17,161 crashes (2023-2025)
- Plan to expand: Additional CA counties, Texas, New York

**Features**:
- Crash location (latitude, longitude)
- Date and time
- Severity (fatal, severe injury, visible injury, complaint of pain, PDO)
- Casualties (number killed, number injured)
- Contributing factors (alcohol, speeding, weather, road conditions)
- Crash type (rear-end, sideswipe, angle, etc.)
- Special circumstances (pedestrian, bicycle, motorcycle involved)

**Access Method**:
- TIMS: Educational account, CSV downloads
- FARS: Public API and bulk downloads
- State DOT databases: Request access for research

**Plan**: Use TIMS for California (detailed, complete), FARS for fatal crashes (nationwide), state DOTs for comprehensive coverage.

---

#### 3.3 Traffic Volume Data
**Source**: Federal Highway Administration Highway Performance Monitoring System (HPMS)
**URL**: https://www.fhwa.dot.gov/policyinformation/hpms.cfm

**Coverage**: All US highways and major roads

**Features**:
- Annual Average Daily Traffic (AADT)
- Truck percentage
- Vehicle classification
- Peak hour volumes
- Road functional class

**Access Method**: Annual bulk downloads (CSV, Shapefile), state DOT supplementary data

**Plan**: Download HPMS data for California, Texas, New York. Join spatially to work zones and crashes for traffic exposure normalization.

**Critical Use**: AADT enables crash rate calculation (crashes per 100 million vehicle-miles traveled), essential for comparing risk across different roads.

---

#### 3.4 Weather Data
**Source**: NOAA National Centers for Environmental Information
**URL**: https://www.ncdc.noaa.gov/cdo-web/datasets

**Coverage**: Historical weather for all US locations (1901-present) + real-time via Weather.gov API

**Features**:
- Precipitation (type, intensity)
- Temperature
- Visibility
- Wind speed and direction
- Weather conditions (clear, rain, fog, snow)

**Access Method**:
- Historical: NOAA LCD (Local Climatological Data) downloads
- Real-time: Weather.gov API (free, no authentication)

**Plan**:
- Match historical weather to crash times/locations
- Integrate real-time weather API for live predictions
- Create weather features: precipitation_1hr, temp, visibility, conditions

---

### Supplementary Datasets

#### 3.5 Road Characteristics
**Source**: OpenStreetMap (OSM)
**URL**: https://www.openstreetmap.org

**Features**:
- Number of lanes
- Speed limits
- Road type (motorway, trunk, primary, secondary)
- Geometry (curvature, intersections)
- Infrastructure (traffic signals, signs)

**Access Method**: Python library `osmnx` for querying OSM data

**Plan**: Extract road network features for work zone locations, use as static features in ML model.

---

#### 3.6 Demographics (Optional)
**Source**: US Census Bureau American Community Survey (ACS)
**URL**: https://www.census.gov/programs-surveys/acs/data.html

**Features**:
- Population density
- Income levels
- Vehicle ownership rates
- Commute patterns

**Access Method**: Census API or bulk downloads

**Plan**: If time permits, incorporate demographic features to capture regional differences in driving behavior.

---

## 4. Data Usage Restrictions and Licenses

### License Review Summary

| Dataset | License | Redistribution | API Restrictions |
|---------|---------|----------------|------------------|
| **WZDx Feeds** | CC0 1.0 (Public Domain) | ✅ Allowed | Rate limits vary by state |
| **TIMS Crashes** | Educational use only | ❌ No public redistribution | Account required |
| **FARS** | Public Domain | ✅ Allowed | None |
| **HPMS Traffic** | Public Domain | ✅ Allowed | None |
| **NOAA Weather** | Public Domain | ✅ Allowed | API rate limits (reasonable use) |
| **OpenStreetMap** | ODbL 1.0 | ✅ Allowed with attribution | Rate limits on API |

### Compliance Plan

1. **No Raw Data in Public Repo**: Will NOT include TIMS crash data in GitHub (educational use restriction)
2. **Data Preprocessing Only**: Share processed/aggregated data (e.g., "crash counts by work zone") rather than individual crash records
3. **API Rate Limiting**: Implement caching and respect rate limits for real-time APIs
4. **Attribution**: Provide proper attribution for OSM data in dashboard
5. **Documentation**: Include data sources and licenses in README and application

**Result**: All data sources comply with usage restrictions for academic research and tool development. Public-facing dashboard will use aggregated statistics and real-time API queries only.

---

## 5. Minimum Viable Product (MVP)

### Core Deliverable: Interactive Work Zone Safety Dashboard

A **Streamlit-based web application** that:

#### 5.1 Predictive Model Component
- **Trained ML model** (XGBoost) predicting crash risk for work zones
- **Input features** (~30-50 features):
  - Work zone: vehicle impact, lane closures, duration, worker presence
  - Traffic: AADT (exposure)
  - Weather: precipitation, temperature, visibility
  - Temporal: hour, day of week, rush hour flags, holidays
  - Road: speed limit, number of lanes, road type
- **Output**: Risk score (0-1 probability of crash) or risk category (Low/Medium/High/Extreme)
- **Performance**: Minimum AUC-ROC > 0.70 on test set

#### 5.2 Geospatial Visualization Component
- **Interactive map** displaying all active work zones in study area
- **Color-coded risk levels**:
  - 🔴 Red: High risk (>0.7 probability)
  - 🟠 Orange: Medium risk (0.4-0.7)
  - 🟡 Yellow: Moderate risk (0.2-0.4)
  - 🟢 Green: Low risk (<0.2)
- **Click for details**: Popup showing:
  - Predicted risk score
  - Contributing factors (weather, traffic, work zone characteristics)
  - Recommended safety actions
  - Historical crash data at location (if available)

#### 5.3 Real-Time Prediction Component
- **Live data integration**:
  - Current weather conditions (Weather.gov API)
  - Active work zones (WZDx feeds)
  - Time-based features (current hour, day, rush hour status)
- **Automatic updates**: Dashboard refreshes every 10-15 minutes
- **Forecast mode**: Show predictions for next 1-6 hours given weather forecast

#### 5.4 Analytics Dashboard
- **Summary statistics**:
  - Total active work zones
  - Number in each risk category
  - Geographic distribution (by county/district)
- **Top risk locations**: Ranked list of highest-risk work zones
- **Temporal patterns**: Risk distribution by hour of day, day of week
- **Feature importance**: What factors drive predictions (for transparency)

#### 5.5 Documentation
- **Technical report** (15-20 pages):
  - Data sources and preprocessing
  - Feature engineering methodology
  - Model development and validation
  - Results and interpretation
  - Limitations and future work
- **User guide**: How to use dashboard
- **Code repository**: Well-documented, reproducible pipeline

---

### MVP Success Criteria (Does NOT Depend on "Exciting" Results)

✅ **Deliverable regardless of findings**:
- Dashboard deploys and runs
- Model makes predictions (even if accuracy is modest)
- Visualizations render correctly
- Real-time data integrates successfully

✅ **Not required for MVP**:
- "Discovering" that a particular factor is most important
- Achieving state-of-the-art prediction accuracy
- Finding dramatic differences between states
- Groundbreaking insights

✅ **Focus on technical execution and practical tool delivery**

---

## 6. Ethical Challenges and Mitigation Strategies

### 6.1 Potential for Misuse of Predictions

**Concern**: Risk predictions could be misinterpreted or misused:
- Over-reliance on model (ignoring local knowledge)
- Discriminatory resource allocation (neglecting low-traffic but high-risk areas)
- False sense of security (low-risk predictions don't guarantee safety)

**Mitigation**:
- **Transparency**: Clearly communicate model limitations and confidence intervals
- **Explainability**: Show which features drive each prediction (SHAP values)
- **Guidance**: Provide recommendations, not mandates; emphasize human judgment
- **Calibration warnings**: Include confidence levels with all predictions
- **Documentation**: Explicitly state tool is decision-support, not decision-making

---

### 6.2 Privacy Concerns with Crash Data

**Concern**: Individual crash records contain personal information (location, time, circumstances)

**Mitigation**:
- **Aggregation**: Only publish aggregated crash statistics (counts, rates)
- **No identifying info**: Remove any personal identifiers before analysis
- **Spatial aggregation**: Report crashes by road segment, not exact coordinates
- **Temporal aggregation**: Use hourly/daily bins, not exact timestamps
- **Compliance**: Follow TIMS educational use terms, HIPAA-like protections

---

### 6.3 Equity and Fairness in Resource Allocation

**Concern**: Model predictions might reinforce existing disparities if trained on biased historical data (e.g., more enforcement in certain areas → more crash reports → higher predicted risk)

**Mitigation**:
- **Feature auditing**: Check for demographic correlations (income, race) with predictions
- **Fairness metrics**: Evaluate model performance across different communities
- **Contextual features**: Include infrastructure quality, not just crash history
- **Transparency**: Disclose any observed biases in documentation
- **Stakeholder engagement**: If possible, seek input from diverse communities

---

### 6.4 Liability and Accountability

**Concern**: If tool is used for decision-making, who is responsible if prediction is wrong?

**Mitigation**:
- **Clear disclaimers**: Tool is for research/planning, not operational safety decisions
- **No guarantees**: Explicitly state predictions are probabilistic, not certain
- **Version control**: Track model versions, document when predictions were made
- **Human-in-the-loop**: Always require human review before actions
- **Liability language**: Include standard research disclaimer in dashboard

---

### 6.5 Unintended Consequences

**Concern**: DOTs might reduce safety measures at "low-risk" work zones, increasing actual risk

**Mitigation**:
- **Baseline recommendations**: Emphasize minimum safety standards apply everywhere
- **Positive framing**: Focus on identifying where ADDITIONAL measures needed, not reductions
- **Education**: Train users that "low risk" is relative, not absolute

---

## 7. Technical Challenges

### 7.1 Large Dataset Management (>1 GB)

**Challenge**:
- Work zone feeds: ~10-50 MB per state (manageable)
- Crash data: 17,161 records so far, expect 100K+ when expanding
- HPMS traffic data: ~500 MB per year (nationwide)
- Weather data: Potentially TBs if downloading all NOAA archives
- Combined: Easily >5-10 GB

**Mitigation**:
- **Efficient storage**: Use Parquet format (compressed columnar storage)
- **Database**: PostgreSQL + PostGIS for spatial queries (instead of in-memory)
- **Selective loading**: Only load relevant geographic regions and time periods
- **Lazy loading**: Load data on-demand in dashboard (not all at once)
- **Sampling**: For exploration, use representative samples; full data for training
- **Cloud storage**: If needed, use AWS S3 or Google Cloud Storage for data lake

**Tools**:
- `dask` for out-of-core processing
- `vaex` for lazy evaluation of large dataframes
- `geopandas` with spatial indexing for efficient joins

---

### 7.2 Difficult Data Cleaning and Integration

**Challenge**:
- **Spatial alignment**: Crashes, work zones, roads, weather stations at different coordinate systems
- **Temporal alignment**: Weather at crash time (need precise timestamps), work zones active when crash occurred
- **Missing data**: Not all crashes have coordinates (~35%), weather stations sparse in rural areas
- **Inconsistent schemas**: WZDx v2.0 (Texas) vs v4.2 (California), different field names
- **Embedded JSON**: Texas lane data in JSON strings within CSV (complex parsing)

**Mitigation**:
- **Standardization pipeline**: Convert all data to common schema (WZDx v4.2)
- **Coordinate system**: Standardize to WGS84 (EPSG:4326) for all spatial data
- **Spatial joins**: Use buffering (100m radius around work zones) to handle GPS uncertainty
- **Temporal joins**: Match to nearest hour for weather (acceptable for daily weather patterns)
- **Missing data strategies**:
  - Imputation: Use KNN or interpolation for missing coordinates
  - Feature flags: Indicator variable for missing weather data
  - Exclusion: Remove records missing critical fields (lat/lon)
- **Automated validation**: Unit tests for data quality checks (e.g., coordinates in US bounding box)

**Tools**:
- `geopandas` for spatial joins
- `pandas` merge with tolerances for temporal joins
- `geopy` for geocoding missing coordinates
- `great_expectations` for data validation

---

### 7.3 Complex ML Pipeline

**Challenge**:
- **Feature engineering**: ~30-50 features from multiple sources
- **Spatial features**: Distance calculations, buffering, aggregations
- **Temporal features**: Lag features (weather 1hr/3hr prior), cyclical encoding (hour, day)
- **Class imbalance**: Crashes are rare events (99%+ of work zone hours have no crashes)
- **Model selection**: Need to try multiple algorithms (XGBoost, Random Forest, LSTM)
- **Hyperparameter tuning**: Large search space
- **Model deployment**: Serving predictions in real-time dashboard

**Mitigation**:
- **Modular pipeline**: Separate scripts for data collection, cleaning, feature engineering, modeling
- **Pipeline automation**: Use `scikit-learn Pipeline` for reproducible preprocessing
- **Version control**: Track feature definitions, model versions (MLflow or DVC)
- **Class imbalance**:
  - Undersampling: Sample negative examples (no crash) to balance classes
  - Class weights: Use `scale_pos_weight` in XGBoost
  - Stratified sampling: Preserve class distribution in train/val/test splits
- **Cross-validation**: Time-series aware split (no future data leakage)
- **Model registry**: Save trained models with metadata (features used, hyperparameters, metrics)
- **API wrapper**: Flask/FastAPI for model serving

**Tools**:
- `scikit-learn` for ML pipeline
- `xgboost`, `lightgbm`, `catboost` for gradient boosting
- `keras`/`tensorflow` if pursuing LSTM
- `mlflow` for experiment tracking
- `FastAPI` for model serving

---

### 7.4 Real-Time API Integration

**Challenge**:
- **Rate limits**: Weather.gov API, traffic APIs have request limits
- **Latency**: Dashboard must respond quickly (<3 seconds)
- **API failures**: External services may be unavailable
- **API changes**: Weather API schema might change

**Mitigation**:
- **Caching**: Store recent API responses (Redis or in-memory cache)
- **Background updates**: Fetch API data every 10 minutes, serve from cache
- **Graceful degradation**: If API fails, show predictions with last known conditions + warning
- **Retry logic**: Exponential backoff for failed requests
- **Mock mode**: Fake API responses for development/testing
- **API abstraction**: Wrapper functions so switching APIs is easy

**Tools**:
- `requests` with `requests-cache` for HTTP requests
- `redis` for caching
- `celery` for background tasks (if needed)

---

### 7.5 Geospatial Visualization Performance

**Challenge**:
- Rendering 1,000+ work zones on map may be slow
- Interactive features (zooming, clicking) need to be responsive

**Mitigation**:
- **Map library**: Use `folium` (Leaflet.js) for interactive maps (proven with your existing maps)
- **Clustering**: Use `MarkerCluster` for dense areas (zoom in to see individual markers)
- **Lazy loading**: Only load visible markers (viewport-based filtering)
- **Simplification**: Use circle markers, not complex polygons
- **Caching**: Pre-render maps for common views

**Tools**:
- `folium` for maps
- `streamlit-folium` for Streamlit integration
- `mapbox` if better performance needed (commercial)

---

### 7.6 Model Interpretability

**Challenge**:
- Stakeholders (DOT personnel) need to understand WHY a work zone is high-risk
- Black-box models (XGBoost, neural networks) are hard to interpret

**Mitigation**:
- **Feature importance**: Use XGBoost built-in feature importance
- **SHAP values**: Show contribution of each feature to individual predictions
- **Partial dependence plots**: Visualize how predictions change with feature values
- **Example explanations**: "This work zone is high risk because: heavy rain (30% contribution), rush hour (25%), all lanes closed (20%)"

**Tools**:
- `shap` library for SHAP values
- `eli5` for feature importance visualization
- Custom explanations in dashboard

---

### 7.7 Computational Resources

**Challenge**:
- Model training on 100K+ crashes may take hours
- Hyperparameter tuning (grid search) computationally expensive

**Mitigation**:
- **Sampling**: Use stratified sample (10-20K crashes) for rapid iteration, full data for final model
- **Efficient algorithms**: XGBoost is fast, prefer over neural networks for tabular data
- **Parallel processing**: Use `n_jobs=-1` for parallel training
- **Cloud resources**: Google Colab (free GPU), AWS (if needed)
- **Incremental development**: Start with small dataset (Alameda County), expand later

**Hardware**:
- Development: Personal laptop (16GB RAM should suffice)
- Training: Google Colab (free tier) or local machine
- Deployment: Streamlit Cloud (free) or Heroku

---

## 8. Evaluation and Success Metrics

### 8.1 Model Performance Metrics

**Primary Metric: AUC-ROC (Area Under ROC Curve)**
- **Target**: AUC > 0.70 (good), AUC > 0.80 (excellent)
- **Why**: Balanced metric for imbalanced classes, interpretable

**Secondary Metrics**:
- **Precision-Recall AUC**: Emphasizes positive class (crashes)
- **F1 Score**: Balance of precision and recall
- **Calibration**: Are predicted probabilities accurate? (Brier score)
- **Top-K Accuracy**: Are actual high-risk zones in top 10% of predictions?

**Baseline Comparisons**:
1. **Naive baseline**: Predict crash risk = historical crash rate at location
2. **Simple baseline**: Logistic regression with 5 features
3. **Random Forest**: Compare to XGBoost
4. **Published research**: Compare to similar studies (if available)

**Success Threshold**:
- ✅ MVP: Model performs better than naive baseline (historical rate)
- ✅ Good: Model AUC > 0.70, outperforms simple logistic regression
- 🎯 Excellent: Model AUC > 0.80, competitive with research literature

---

### 8.2 Feature Importance Analysis

**Evaluation**:
- Identify top 10 most predictive features
- Verify features make intuitive sense (weather, traffic, rush hour expected to be important)
- Check for unexpected relationships (investigate if counterintuitive)

**Success Criteria**:
- ✅ Can explain to non-technical stakeholders why model makes predictions
- ✅ Feature importance aligns with domain knowledge
- ✅ No single feature dominates (indicates robust model)

---

### 8.3 Dashboard Functionality

**User Testing Checklist**:
- [ ] Dashboard loads within 5 seconds
- [ ] Map renders all work zones
- [ ] Click on marker shows prediction details
- [ ] Risk colors update when filters applied
- [ ] Real-time weather data integrates successfully
- [ ] Predictions refresh on schedule (10-15 min)
- [ ] Works on mobile devices (responsive design)

**Success Criteria**:
- ✅ All checklist items pass
- ✅ No crashes or errors during 30-minute session
- ✅ Feedback from 3+ test users (positive usability)

---

### 8.4 Geospatial Visualizations

**Quality Metrics**:
- Clarity: Can users quickly identify high-risk zones?
- Accuracy: Do visualizations correctly represent data?
- Interactivity: Are tooltips, filters, zoom intuitive?

**Evaluation Method**:
- Show dashboard to classmates/instructors
- Ask: "Which work zones need attention?" (should identify high-risk ones)
- Time to complete task: <30 seconds

**Success Criteria**:
- ✅ 80% of users correctly identify high-risk zones
- ✅ Positive feedback on clarity and usefulness

---

### 8.5 Real-Time Prediction Accuracy

**Evaluation** (if time permits for validation):
- Collect data on work zones for 1 week
- Make hourly predictions
- Compare to actual crashes (if any occur)

**Success Criteria**:
- ✅ High-risk predictions are more likely to have crashes than low-risk
- ✅ No false negatives (crashes in "low risk" zones) if possible

**Note**: This is stretch goal, not required for MVP.

---

### 8.6 Documentation Quality

**Evaluation Criteria**:
- Technical report covers all required sections
- Code is documented (docstrings, comments)
- README explains how to run project
- Results are reproducible

**Success Criteria**:
- ✅ Another student could replicate results with provided instructions
- ✅ Report clearly explains methods and findings
- ✅ Visualizations have appropriate labels, legends, captions

---

### 8.7 Impact and Insights

**Success is NOT dependent on "surprising" findings**, but we will evaluate:

**Analytical Questions Answered**:
- Which factors most predict crashes? (weather, traffic, closures, etc.)
- Do California vs Texas work zones differ in risk?
- Are there temporal patterns (rush hour, weekends)?

**Policy Implications Identified**:
- Recommendations for high-risk work zones (e.g., increase enforcement, improve signage)
- Cost-benefit analysis (if feasible): Prioritize safety improvements

**Success Criteria**:
- ✅ Report includes actionable recommendations (even if obvious, like "rain increases risk")
- ✅ Results are communicated clearly to non-technical audience

---

## 9. Team Contributions

**Team Size**: 1 (Solo project)

**Role Assignments** (Single Person):

### Project Manager
- Define scope and milestones
- Track progress against timeline
- Adjust plan as needed
- Communicate with instructors

### Data Engineer
- Collect and clean all datasets
- Build ETL pipeline (Extract, Transform, Load)
- Integrate APIs (weather, traffic, work zones)
- Manage data storage (database or files)

### Machine Learning Engineer
- Feature engineering
- Model training and tuning
- Model evaluation
- Deploy model for predictions

### Data Analyst
- Exploratory data analysis (EDA)
- Statistical analysis
- Visualizations (charts, plots)
- Interpret results

### Software Developer
- Build Streamlit dashboard
- Implement geospatial visualizations
- Create prediction API
- Deploy web application

### Technical Writer
- Write project proposal (this document)
- Document code and pipeline
- Create user guide
- Write final report

---

**Time Allocation Strategy** (16 weeks total):
- **Weeks 1-4**: Data collection and integration (40%)
- **Weeks 5-8**: Feature engineering and EDA (20%)
- **Weeks 9-11**: Model development and tuning (20%)
- **Weeks 12-14**: Dashboard development (15%)
- **Weeks 15-16**: Documentation and presentation (5%)

---

## 10. Cloud Computing and Resource Needs

### 10.1 Cloud Computing Requirements

**Expected to Use**:

**Google Colab** (Free Tier)
- **Purpose**: Model training (if laptop insufficient)
- **Resources**: Free GPU/TPU access
- **Usage**: Hyperparameter tuning, training on full dataset
- **Estimated hours**: 10-20 hours total

**Streamlit Cloud** (Free Tier)
- **Purpose**: Dashboard deployment
- **Resources**: Free hosting for Streamlit apps
- **Limitations**: 1 GB RAM, GitHub-based deployment
- **Alternative**: Heroku free tier or local deployment

**GitHub** (Free)
- **Purpose**: Version control, code storage
- **Resources**: Unlimited public repos
- **Plan**: Use private repo during development, public for final submission

**Unlikely to Need** (but available if necessary):
- AWS S3: Data storage (if >1 GB)
- AWS EC2: Compute for intensive tasks
- Google Cloud Platform: BigQuery for large data processing

**Budget**: $0 (all free tiers sufficient for MVP)

---

### 10.2 Teaching Team Support Requests

**Advising Needs**:

1. **Data Access Assistance**:
   - If TIMS access encounters issues, guidance on alternative crash data sources
   - Letters of support if requesting data from state DOTs

2. **Domain Expertise**:
   - Office hours discussion on work zone safety factors (if instructors have transportation background)
   - Feedback on feature selection (are these features reasonable?)

3. **Model Evaluation Guidance**:
   - Review model performance metrics (is AUC 0.75 good enough?)
   - Advice on handling severe class imbalance (99% non-crash)

4. **Geospatial Analysis Support**:
   - Best practices for spatial joins (buffering strategies)
   - Performance optimization for large geospatial datasets

5. **API Integration**:
   - Troubleshooting API rate limits or failures
   - Best practices for caching and error handling

6. **Deployment Support**:
   - Assistance with Streamlit Cloud deployment if issues arise
   - Guidance on serving ML models in web apps

7. **Scope Management**:
   - Checkpoint reviews to ensure MVP is achievable
   - Advice on what features to defer to "future work"

**Office Hours Plan**:
- Bi-weekly check-ins (Weeks 2, 4, 6, 8, 10, 12, 14)
- Topics: Data integration (Week 2), Feature engineering (Week 4), Model evaluation (Week 8), Dashboard feedback (Week 12)

**Communication**:
- Slack for quick questions
- Email for data access or formal requests
- Office hours for technical discussions

---

## 11. Project Timeline

### Phase 1: Data Foundation (Weeks 1-4)
**Week 1-2**:
- Expand crash data (more counties/states)
- Download HPMS traffic volume data
- Set up NOAA weather API access

**Week 3-4**:
- Extract OSM road characteristics
- Build spatial join pipeline (crashes ↔ work zones ↔ roads)
- Temporal join (weather at crash times)

**Deliverable**: Integrated dataset ready for ML

---

### Phase 2: Feature Engineering (Weeks 5-8)
**Week 5-6**:
- Engineer temporal features (hour, day, rush hour, holidays)
- Create weather features (precipitation, temp, visibility)
- Calculate traffic exposure features (AADT, vehicle mix)

**Week 7-8**:
- Exploratory Data Analysis (EDA)
- Feature correlation analysis
- Handle missing data
- Create train/val/test splits

**Deliverable**: Feature matrix (samples × features) ready for modeling

---

### Phase 3: Model Development (Weeks 9-11)
**Week 9**:
- Train baseline models (logistic regression, naive)
- Train XGBoost classifier
- Hyperparameter tuning (grid search or Bayesian optimization)

**Week 10**:
- Model evaluation (AUC, precision-recall, calibration)
- Feature importance analysis
- Error analysis (where does model fail?)

**Week 11**:
- Model refinement (add features, try ensemble)
- Final model selection
- Save trained model for deployment

**Deliverable**: Trained ML model achieving target metrics

---

### Phase 4: Dashboard Development (Weeks 12-14)
**Week 12**:
- Build Streamlit dashboard structure
- Integrate trained model
- Create geospatial visualizations (Folium maps)

**Week 13**:
- Add real-time API integration (weather, work zones)
- Implement risk color-coding
- Create summary statistics and charts

**Week 14**:
- User testing and refinement
- Mobile responsiveness
- Deploy to Streamlit Cloud

**Deliverable**: Live, functional dashboard

---

### Phase 5: Documentation & Presentation (Weeks 15-16)
**Week 15**:
- Write technical report
- Create user guide
- Document code and pipeline
- Prepare presentation slides

**Week 16**:
- Final testing and bug fixes
- Presentation rehearsal
- Submit project

**Deliverable**: Complete project submission

---

## 12. Risk Mitigation and Contingency Plans

### Risk 1: Data Access Issues
**What if**: State DOT denies data access or TIMS restricts downloads?

**Contingency**:
- Use FARS (federal, always available) for fatal crashes
- Focus on California only (already have data)
- Use synthetic data generation if necessary (less ideal)

---

### Risk 2: Model Performance Below Target
**What if**: Model AUC < 0.70?

**Contingency**:
- Shift focus to descriptive analysis (which factors matter?)
- Frame as "feature importance study" rather than prediction tool
- Emphasize dashboard and visualization (still valuable)
- Adjust expectations: "Crash prediction is hard, our model identifies risk factors"

---

### Risk 3: API Integration Failures
**What if**: Weather API goes down or changes?

**Contingency**:
- Have backup weather source (OpenWeatherMap)
- Implement graceful degradation (show predictions with cached weather + warning)
- If all APIs fail, use historical weather (less real-time but still functional)

---

### Risk 4: Insufficient Time for All States
**What if**: Data integration takes longer than expected?

**Contingency**:
- Reduce scope to California only (Bay Area)
- Still ~18K data points (sufficient for ML)
- Frame as "California case study with methodology generalizable to other states"

---

### Risk 5: Dashboard Performance Issues
**What if**: Map rendering is too slow?

**Contingency**:
- Use marker clustering (hide individual markers until zoom in)
- Limit visible work zones (top 100 highest risk)
- Pre-render static maps for common views
- Simplify markers (circles instead of complex icons)

---

## 13. Expected Outcomes and Contributions

### Technical Contributions
1. **Open-source prediction tool** for work zone safety
2. **Reproducible ML pipeline** for crash risk modeling
3. **Data integration framework** combining multiple public datasets
4. **Geospatial visualization techniques** for transportation safety

### Research Contributions
1. **Feature importance analysis**: Which factors most predict work zone crashes?
2. **Multi-state comparison**: Do California, Texas, New York differ in risk patterns?
3. **Temporal patterns**: Rush hour, weather, seasonal effects quantified
4. **Baseline metrics**: Establish benchmark for future work zone safety prediction research

### Practical Impact
1. **Decision support tool** for DOT safety personnel
2. **Risk visualization** for public awareness and planning
3. **Data-driven resource allocation** (where to deploy enforcement, signage)
4. **Replicable methodology** for other states/regions

### Learning Outcomes
1. End-to-end ML project experience (data → model → deployment)
2. Geospatial data science skills (GIS, spatial joins, mapping)
3. Real-world API integration and web development
4. Communication of technical results to non-technical stakeholders

---

## 14. Conclusion

SafeZone represents a comprehensive capstone project integrating data science, machine learning, geospatial analysis, and web development to address a critical public safety challenge. By developing a predictive model and interactive dashboard for work zone crash risk, this project aims to provide actionable insights for transportation decision-makers while demonstrating proficiency in the MADS program's core competencies.

The project is designed to be deliverable regardless of analytical "surprises"—the MVP is a functional tool with documented methodology, not groundbreaking discoveries. Success is measured by technical execution (working dashboard, validated model, clear documentation) and practical utility (tool provides value to stakeholders), not by finding unexpected patterns in the data.

We look forward to feedback on this proposal and guidance throughout the project lifecycle.

---

**Submitted by**: Team Transport
**Date**: October 10, 2025
**Contact**: [Your email here]

---

## Appendices

### Appendix A: Preliminary Data Exploration Results

Already completed exploratory analysis:
- California work zones: 1,186 zones analyzed
- Texas work zones: 288 unique zones analyzed
- Alameda County crashes: 17,161 crashes mapped
- Interactive visualizations: 6 maps created
- Data quality assessment: Completeness and accuracy verified

See `docs/` folder for detailed exploration reports.

---

### Appendix B: Technical Stack

**Languages**: Python 3.9+

**Data Processing**:
- pandas, geopandas (data manipulation)
- shapely, pyproj (spatial operations)
- osmnx (road network data)
- requests (API calls)

**Machine Learning**:
- scikit-learn (pipeline, preprocessing, metrics)
- xgboost, lightgbm (gradient boosting)
- shap (explainability)
- mlflow (experiment tracking)

**Visualization**:
- matplotlib, seaborn (charts)
- folium (interactive maps)
- plotly (interactive charts)

**Web Development**:
- streamlit (dashboard framework)
- fastapi (model API, if needed)

**Development Tools**:
- Git/GitHub (version control)
- Jupyter notebooks (exploration)
- VS Code (IDE)

---

### Appendix C: Related Work

**Research Papers**:
1. FHWA Work Zone Safety Data Initiative (2020)
2. "Predicting Crash Risk in Work Zones Using Machine Learning" (various DOT studies)
3. WZDx specification and implementation guides

**Existing Tools**:
- FHWA Work Zone Safety Analysis Tools
- State DOT dashboards (various states)

**Our Contribution**: First open-source, multi-state, ML-powered work zone safety prediction dashboard with real-time integration.

---

**END OF PROPOSAL**
