# Quick Form Responses for Project Proposal

Use these condensed responses to fill out your actual proposal form.

---

## Team Name
**Team Transport**

---

## Project Subject and Questions (Brief Paragraph)

Highway work zones create significant safety risks, resulting in ~70,000 injuries and 700 fatalities annually in the US. Our project develops a machine learning-powered platform that predicts crash risk in active work zones and provides real-time risk assessments through an interactive geospatial dashboard. We aim to answer: (1) What factors most strongly predict work zone crashes? (2) Can we forecast crash likelihood before they occur? (3) How can we effectively visualize risk for transportation decision-makers? By identifying high-risk work zones in near real-time, our tool enables proactive safety interventions, providing data-driven insights for policy makers to reduce work zone crashes through predictive analytics.

---

## Datasets

### Work Zone Data
- **Source**: WZDx Feed Registry (https://datahub.transportation.gov/Roadways-and-Bridges/Work-Zone-Data-Exchange-WZDx-Feed-Registry/69qe-yiui/about_data)
- **Access**: Real-time APIs (CA, NY), CSV downloads (TX)
- **Features**: Location, vehicle impact, lane closures, worker presence, dates, work type
- **Coverage**: California (1,186 zones), Texas (288 zones), New York (1,138 zones)

### Crash Data
- **Source**: TIMS - UC Berkeley (https://tims.berkeley.edu/), NHTSA FARS (https://crashstats.nhtsa.dot.gov)
- **Access**: Educational account (TIMS), public API (FARS)
- **Features**: Location, datetime, severity, casualties, contributing factors, crash type
- **Coverage**: Currently Alameda County (17,161 crashes), expanding to additional counties/states

### Traffic Volume
- **Source**: FHWA HPMS (https://www.fhwa.dot.gov/policyinformation/hpms.cfm)
- **Access**: Annual bulk downloads (CSV, Shapefile)
- **Features**: AADT, truck %, vehicle classification, peak volumes
- **Coverage**: All US highways

### Weather Data
- **Source**: NOAA NCEI (https://www.ncdc.noaa.gov/cdo-web/datasets), Weather.gov API
- **Access**: Historical downloads, real-time API (free)
- **Features**: Precipitation, temperature, visibility, wind, conditions
- **Coverage**: All US locations, 1901-present + real-time

### Supplementary
- **OpenStreetMap**: Road characteristics (lanes, speed, geometry)
- **US Census ACS**: Demographics (optional, if time permits)

---

## Usage Restrictions

**Compliant with all restrictions**:
- WZDx, FARS, HPMS, NOAA, OSM: Public domain or open licenses, redistribution allowed
- TIMS: Educational use only, will NOT redistribute raw data in public repo
- Will use aggregated/processed data only in dashboard
- Respect API rate limits with caching
- Include proper attributions

**Mitigation**: No raw TIMS data in GitHub, only aggregated statistics; document all sources and licenses in README.

---

## Minimum Viable Product (MVP)

**Interactive Streamlit web dashboard** with:

1. **Predictive ML model** (XGBoost) predicting crash risk (0-1 probability) for work zones using ~30-50 features (work zone characteristics, weather, traffic, temporal, road features)

2. **Geospatial visualization**: Interactive map showing all active work zones color-coded by predicted risk level (Red=High, Orange=Medium, Yellow=Moderate, Green=Low) with clickable popups showing risk score, contributing factors, and recommendations

3. **Real-time predictions**: Integration with Weather.gov API and WZDx feeds for live risk assessments, updating every 10-15 minutes

4. **Analytics dashboard**: Summary statistics (total zones, risk distribution), top risk locations ranked list, temporal patterns, feature importance explanations

5. **Technical documentation**: 15-20 page report covering data sources, methodology, model validation, results, and limitations; plus user guide and code repository

**Success criteria**: Dashboard deploys and runs, model makes predictions (AUC > 0.70), visualizations render correctly, real-time data integrates—deliverable regardless of "exciting" findings.

---

## Ethical Challenges and Mitigation

**1. Misuse of predictions**: Risk of over-reliance, false security
- **Mitigation**: Clear disclaimers, confidence intervals, emphasize decision-support not decision-making, show model limitations

**2. Privacy concerns**: Crash data contains personal information
- **Mitigation**: Aggregate data only, remove identifiers, spatial/temporal aggregation, follow TIMS educational use terms

**3. Equity and fairness**: Model might reinforce existing disparities
- **Mitigation**: Feature auditing for demographic correlations, fairness metrics, transparency about biases, stakeholder engagement

**4. Liability**: Accountability if predictions are wrong
- **Mitigation**: Research disclaimers, probabilistic framing, version control, human-in-the-loop requirement, no operational guarantees

**5. Unintended consequences**: DOTs might reduce safety at "low-risk" zones
- **Mitigation**: Emphasize minimum standards everywhere, positive framing (where ADDITIONAL measures needed), education that "low risk" is relative

---

## Technical Challenges

**1. Large datasets (>5 GB)**: Crashes (100K+ records), HPMS (500 MB/year), weather archives
- **Mitigation**: Parquet format, PostgreSQL+PostGIS, selective loading, lazy evaluation (dask/vaex), cloud storage if needed

**2. Difficult data cleaning**: Spatial alignment (different coordinate systems), temporal joins (weather at crash time), missing data (35% crashes lack coordinates), inconsistent schemas (WZDx v2.0 vs v4.2)
- **Mitigation**: Standardization pipeline, WGS84 coordinates, buffered spatial joins (100m), nearest-hour temporal joins, imputation/exclusion for missing data, automated validation tests

**3. Complex ML pipeline**: 30-50 features from multiple sources, class imbalance (99% non-crash), model deployment
- **Mitigation**: Modular pipeline (scikit-learn Pipeline), undersampling/class weights for imbalance, MLflow for tracking, FastAPI for serving

**4. Real-time API integration**: Rate limits, latency (<3s response), API failures
- **Mitigation**: Caching (Redis), background updates every 10min, graceful degradation, retry logic, mock mode for development

**5. Geospatial visualization performance**: 1,000+ markers may be slow
- **Mitigation**: MarkerCluster, lazy loading, circle markers not polygons, pre-rendered caching

**6. Model interpretability**: Stakeholders need to understand WHY
- **Mitigation**: SHAP values, feature importance plots, partial dependence, example explanations

**7. Computational resources**: Model training may take hours
- **Mitigation**: Stratified sampling for iteration, efficient algorithms (XGBoost), parallel processing, Google Colab if needed

---

## Evaluation and Success Criteria

**Model Performance**:
- **Primary**: AUC-ROC > 0.70 (good), > 0.80 (excellent)
- **Secondary**: Precision-Recall AUC, F1 score, calibration (Brier score), Top-K accuracy
- **Baselines**: Naive (historical crash rate), simple logistic regression, Random Forest
- **Success**: Model outperforms baselines, AUC > 0.70

**Feature Importance**:
- Identify top 10 predictive features
- Verify intuitive sense (weather, traffic, rush hour expected)
- Explain to non-technical stakeholders

**Dashboard Functionality**:
- Loads <5 seconds, renders all zones, clickable markers work, risk colors accurate, real-time data integrates, no crashes in 30-min session, mobile responsive
- 80% of test users identify high-risk zones correctly

**Documentation**:
- Technical report covers all sections, code documented, reproducible results, README clear

**Impact** (NOT required for success, but evaluated):
- Identify which factors predict crashes, compare CA/TX/NY, temporal patterns, actionable recommendations

**Overall**: Success = working tool + validated model + clear documentation, NOT "surprising findings"

---

## Team Contributions

**Solo project** - All roles filled by one person:

- **Project Manager**: Define scope, track milestones, communicate with instructors
- **Data Engineer**: Collect/clean datasets, build ETL pipeline, integrate APIs
- **ML Engineer**: Feature engineering, model training/tuning, deployment
- **Data Analyst**: EDA, statistical analysis, visualizations, interpret results
- **Software Developer**: Build Streamlit dashboard, geospatial visualizations, prediction API
- **Technical Writer**: Proposal, code documentation, user guide, final report

**Time allocation** (16 weeks):
- Weeks 1-4: Data collection (40%)
- Weeks 5-8: Feature engineering (20%)
- Weeks 9-11: Modeling (20%)
- Weeks 12-14: Dashboard (15%)
- Weeks 15-16: Documentation (5%)

---

## Cloud Computing

**Will use**:
- **Google Colab** (free): Model training if laptop insufficient, 10-20 hours total
- **Streamlit Cloud** (free): Dashboard deployment and hosting
- **GitHub** (free): Version control, private during development

**Unlikely to need** (available if necessary):
- AWS S3, EC2, or Google Cloud Platform

**Budget**: $0 (all free tiers sufficient)

---

## Support Requests for Teaching Team

**Advising needs**:
1. **Data access**: Guidance if TIMS has issues, letters of support for state DOT requests
2. **Domain expertise**: Work zone safety factors, feature selection feedback
3. **Model evaluation**: Review metrics (is AUC 0.75 good enough?), handling class imbalance
4. **Geospatial analysis**: Spatial join best practices, performance optimization
5. **API integration**: Troubleshooting rate limits, caching strategies
6. **Deployment**: Streamlit Cloud assistance, ML model serving guidance
7. **Scope management**: Checkpoint reviews, advice on deferring features

**Office hours plan**: Bi-weekly check-ins (Weeks 2, 4, 6, 8, 10, 12, 14)

**Communication**: Slack for quick questions, email for formal requests, office hours for technical discussions

---

## Additional Notes

**Project uniqueness**: First open-source, multi-state, ML-powered work zone safety prediction dashboard with real-time integration

**Risk mitigation**: Contingency plans for data access issues, low model performance, API failures, time constraints

**Expected outcomes**: Functional tool, reproducible pipeline, research contributions (feature importance, multi-state comparison), practical impact for DOT personnel

---

**END OF FORM RESPONSES**

Use the full PROJECT_PROPOSAL.md for detailed reference!
