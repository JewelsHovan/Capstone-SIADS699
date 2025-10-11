# Work Zone Safety - Capstone Project Scope

## Project Overview
Analysis of Work Zone Data Exchange (WZDx) feeds to improve highway work zone safety through data-driven insights and visualizations.

---

## What We've Discovered

### 1. **Data Availability**
- **Real-world feeds**: Successfully accessed NY 511 WZDx feed with **1,138 active work zones**
- **Example scenarios**: 8 different scenario types from specification examples
- **Data sources**: Multiple state DOTs publish WZDx feeds (Colorado, Florida, Iowa, Massachusetts, Texas, Utah, etc.)
- **Format**: Standardized GeoJSON with consistent schema (WZDx v4.1/v4.2)

### 2. **Key Data Fields Available**

#### Work Zone Properties
- **Location**: Road names, geographic coordinates, cross streets, mileposts
- **Timing**: Start/end dates, update frequency, verification status
- **Impact**: Vehicle impact type, lane closures, speed reductions
- **Safety**: Worker presence indicators, work zone types (static/moving)
- **Lane Details**: Number of lanes, lane status (open/closed), lane restrictions
- **Descriptions**: Rich text descriptions of work activities

#### Current Data Quality (NY Feed)
- ✅ **Strong**: Geographic coordinates, temporal data, descriptions
- ⚠️ **Limited**: Direction (marked as "unknown"), vehicle impact details
- ❌ **Missing**: Worker presence data, detailed lane information, speed limits

### 3. **Real-World Insights from NY Feed**
- **1,138 active work zones** across New York state
- Work zone durations vary from days to **years** (one from 2023-2026)
- Major highways covered: I-81, I-91, I-481, I-691, Taconic Parkway, US Routes
- Work types: Bridge rehabilitation, utility work, barrier repairs, lane restrictions
- Geographic coverage: Entire state with precise coordinates

---

## Potential Project Directions

### **Option 1: Work Zone Safety Dashboard** 🎯 *RECOMMENDED*

**Goal**: Create an interactive dashboard for work zone safety analysis

**Key Features**:
1. **Geographic Visualization**
   - Map of active work zones with clustering
   - Heat maps of work zone density
   - Highway corridor analysis

2. **Safety Metrics**
   - Work zones with workers present
   - Lane closure statistics
   - Speed reduction zones
   - Duration analysis (long-term vs. short-term)

3. **Temporal Analysis**
   - Work zone scheduling patterns (day/night, seasonal)
   - Recurring work zones
   - Historical trends

4. **Risk Assessment**
   - High-risk zones (workers + lane closures + high traffic)
   - Vehicle impact classification
   - Work zone complexity scoring

**Technical Stack**:
- Python (pandas, geopandas)
- Visualization: Plotly/Folium for maps, Streamlit/Dash for dashboard
- Data: Multiple state WZDx feeds

**Deliverables**:
- Interactive web dashboard
- Analysis report with safety insights
- Data pipeline for feed updates

---

### **Option 2: Predictive Work Zone Analysis**

**Goal**: Predict work zone characteristics and potential safety issues

**Analyses**:
1. Duration prediction (planned vs. actual)
2. Work zone impact classification
3. Optimal scheduling recommendations
4. Resource allocation optimization

**Challenges**:
- Requires historical data (may need to collect over time)
- Data quality varies by state

---

### **Option 3: Work Zone Data Quality Assessment**

**Goal**: Evaluate and improve WZDx feed data quality across states

**Components**:
1. Compare completeness across different state feeds
2. Identify missing critical safety fields
3. Create data quality scoring system
4. Recommendations for data providers

**Value**:
- Helps DOTs improve their data
- Identifies best practices
- Useful for policy recommendations

---

### **Option 4: Multi-Source Integration**

**Goal**: Combine WZDx data with other datasets for comprehensive safety analysis

**Data Sources**:
- WZDx feeds (work zones)
- Traffic volume data
- Crash data (if available)
- Weather data
- Construction permits

**Insights**:
- Correlation between work zones and incidents
- Traffic pattern changes around work zones
- Weather impact on work zone safety

---

## Recommended Scope for Capstone

### **Phase 1: Data Foundation** (Weeks 1-2)
- ✅ Set up WZDx data parser (DONE)
- ✅ Fetch and analyze example feeds (DONE)
- ✅ Fetch real-world feed (NY 511) (DONE)
- 🔲 Collect additional state feeds (3-5 states)
- 🔲 Create unified data pipeline
- 🔲 Build data cleaning and validation

### **Phase 2: Analysis** (Weeks 3-4)
- 🔲 Exploratory data analysis
- 🔲 Geographic analysis (clustering, hotspots)
- 🔲 Temporal patterns (seasonal, day/night)
- 🔲 Safety metric development
- 🔲 Statistical analysis

### **Phase 3: Visualization** (Weeks 5-6)
- 🔲 Interactive map with work zones
- 🔲 Dashboard with key metrics
- 🔲 Time-series visualizations
- 🔲 Comparative analysis across states

### **Phase 4: Insights & Reporting** (Weeks 7-8)
- 🔲 Safety recommendations
- 🔲 Policy implications
- 🔲 Data quality assessment
- 🔲 Final report and presentation

---

## Data Gaps to Address

### Current Limitations (based on NY feed):
1. **Direction**: Mostly marked as "unknown"
2. **Vehicle Impact**: All marked as "unknown"
3. **Worker Presence**: No data available
4. **Lane Details**: Missing in many records
5. **Speed Limits**: Not provided

### Mitigation Strategies:
1. Use multiple state feeds (some have better data quality)
2. Focus on available fields (location, timing, descriptions)
3. Extract information from description text using NLP
4. Cross-reference with other data sources

---

## Key Research Questions

1. **Geographic**: Where are work zones most concentrated?
2. **Temporal**: When do most work zones occur? (seasonal patterns, time of day)
3. **Duration**: How long do work zones typically last?
4. **Safety**: What characteristics correlate with higher-risk work zones?
5. **Accessibility**: How well does WZDx data serve its purpose for navigation/AVs?
6. **Quality**: Which states provide the most complete data?

---

## Success Metrics

### Technical:
- Successfully parse and analyze 5+ state WZDx feeds
- Create automated data pipeline
- Build functional interactive dashboard
- Achieve >90% data processing accuracy

### Analytical:
- Identify 3-5 actionable safety insights
- Compare data quality across states
- Develop work zone risk scoring methodology
- Provide policy recommendations

### Presentation:
- Professional dashboard/visualization
- Clear, data-driven insights
- Actionable recommendations for DOTs
- Demonstration of data science skills

---

## Tools & Technologies

### Data Processing:
- Python (pandas, geopandas, numpy)
- JSON/GeoJSON parsing
- Spatial analysis (shapely, folium)

### Visualization:
- **Maps**: Folium, Plotly, Kepler.gl
- **Dashboards**: Streamlit or Plotly Dash
- **Charts**: Matplotlib, Seaborn, Plotly

### Optional Advanced:
- NLP for description text analysis (spaCy, BERT)
- Time series analysis (statsmodels)
- Machine learning (scikit-learn)

---

## Next Steps

1. **Decide on primary focus** (Dashboard recommended)
2. **Collect additional state feeds** (3-5 states with good data quality)
3. **Perform comprehensive EDA** on combined dataset
4. **Identify specific safety questions** to answer
5. **Design dashboard mockup**
6. **Build prototype**

---

## Resources

- WZDx Specification: https://github.com/usdot-jpo-ode/wzdx
- Feed Registry: https://datahub.transportation.gov (search "WZDx")
- Current feeds collected:
  - ✅ NY 511: https://511ny.org/api/wzdx
  - 🔲 Colorado, Iowa, Massachusetts, Texas (to be added)

---

## Questions to Consider

1. **Scope**: Dashboard only, or include predictive modeling?
2. **Geography**: Single state vs. multi-state comparison?
3. **Time Range**: Current snapshot vs. historical trends?
4. **Audience**: DOTs, planners, general public, or researchers?
5. **Focus**: Safety, efficiency, data quality, or all three?
