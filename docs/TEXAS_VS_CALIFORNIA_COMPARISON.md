# Texas vs. California Work Zone Data Comparison

**Date**: October 10, 2025
**Purpose**: Multi-state work zone analysis for capstone project

---

## Executive Summary

This document compares work zone data from **Texas DOT (TxDOT)** and **California 511** to identify opportunities for multi-state safety analysis and research insights.

---

## Data Sources Comparison

| Aspect | California | Texas |
|--------|-----------|-------|
| **Source** | California 511 API | TxDOT Work Zone Data |
| **Format** | WZDx v4.2 (GeoJSON) | WZDx v2.0 (CSV) |
| **Coverage** | San Francisco Bay Area | Statewide (multiple districts) |
| **Total Records** | 1,186 work zones | 2,180 records (288 unique zones) |
| **Coordinates** | 100% (GeoJSON) | 83.9% |
| **Update Frequency** | Real-time (~10 min) | Snapshot (04/02/2024) |

---

## Dataset Statistics

### California Work Zones

**Coverage**: San Francisco Bay Area
**Records**: 1,186 work zones
**Data Quality**: ⭐⭐⭐⭐⭐ Excellent

**Key Statistics**:
- Geographic scope: Bay Area (localized)
- Worker presence data: 7 zones with workers
- Detailed vehicle impact data
- Active/live feed (continuously updated)

**Top Roads**:
1. Meridian Ave: 30 work zones
2. Urbano Dr: 14 work zones
3. Folsom St: 12 work zones
4. Market St: 10 work zones
5. Mercado Way: 10 work zones

**Vehicle Impact**:
- All-Lanes-Closed: Highest severity
- Some-Lanes-Closed: Moderate
- All-Lanes-Open: Minimal impact

### Texas Work Zones

**Coverage**: Statewide (5 major districts)
**Records**: 2,180 total (288 unique work zones)
**Data Quality**: ⭐⭐⭐⭐ Very Good

**Key Statistics**:
- Multiple records per zone (7.6 avg per zone)
- Statewide coverage across Texas
- Short-term focus (98% ≤7 days duration)
- No worker presence data
- No speed limit data

**Top Districts**:
1. ELP (El Paso): 1,239 records
2. SAT (San Antonio): 554 records
3. WAC_TTI: 294 records
4. DAL1 (Dallas): 84 records
5. FTW (Fort Worth): 9 records

**Top Roads**:
1. IH-10: 508 work zones
2. LP-375: 252 work zones
3. LP-1604: 202 work zones
4. I-35: 126 work zones
5. Joe Battle: 112 work zones

**Vehicle Impact**:
- Some-Lanes-Closed: 740 (33.9%)
- All-Lanes-Open: 736 (33.8%)
- All-Lanes-Closed: 542 (24.9%)
- Unknown: 162 (7.4%)

---

## Data Quality Comparison

### Field Completeness

| Field | California | Texas |
|-------|-----------|-------|
| **Road Name** | 100% | 100% |
| **Direction** | ⭐⭐⭐⭐ Good | 100% |
| **Vehicle Impact** | ⭐⭐⭐⭐⭐ Detailed | 100% |
| **Worker Presence** | ⭐⭐⭐⭐ Available | ❌ 0% |
| **Speed Limit** | ⭐⭐⭐ Some | ❌ 0% |
| **Coordinates** | ⭐⭐⭐⭐⭐ 100% | ⭐⭐⭐⭐ 83.9% |
| **Start/End Dates** | ⭐⭐⭐⭐⭐ 100% | 100% |
| **Description** | ⭐⭐⭐⭐ Good | 99.4% |

### Data Structure

**California (WZDx v4.2)**:
- ✅ GeoJSON format (standard)
- ✅ LineString geometry (road segments)
- ✅ Real-time updates
- ✅ Detailed lane-level data
- ✅ Worker presence tracking
- ⚠️ Limited to Bay Area

**Texas (WZDx v2.0)**:
- ✅ CSV format (easier to process)
- ✅ MULTIPOINT/LINESTRING geometry
- ✅ Statewide coverage
- ✅ Multiple districts
- ✅ Detailed lane information (JSON embedded)
- ⚠️ Snapshot data (not real-time)
- ⚠️ Multiple records per work zone
- ❌ No worker presence
- ❌ No speed limits

---

## Geographic Scope Comparison

### California
- **Region**: San Francisco Bay Area
- **Cities**: San Jose, Oakland, Fremont, etc.
- **Highways**: I-880, US-101, I-280, SR-85
- **Type**: Urban/suburban metropolitan area
- **Population Density**: High

### Texas
- **Region**: Statewide (focus on El Paso, San Antonio)
- **Cities**: El Paso, San Antonio, Dallas, Fort Worth
- **Highways**: IH-10, I-35, Loop roads
- **Type**: Mix of urban and rural
- **Population Density**: Varies (urban cores + highways)

---

## Temporal Patterns

### California
- **Feed Type**: Real-time snapshot
- **Update Frequency**: ~10 minutes
- **Duration**: Mix of short, medium, long-term projects
- **Historical Data**: Available via USDOT S3 bucket

### Texas
- **Feed Type**: Daily snapshots
- **Records**: Multiple dates for same work zone
- **Duration**: Predominantly short-term (98% ≤7 days)
- **Data Date**: April 2, 2024

**Duration Comparison**:

| Duration | California | Texas |
|----------|-----------|-------|
| Short (≤7 days) | Mixed | 2,144 (98.3%) |
| Medium (8-30 days) | Mixed | 30 (1.4%) |
| Long (>30 days) | Mixed | 6 (0.3%) |

*Note: Texas data heavily skewed toward short-term closures*

---

## Vehicle Impact Comparison

### California
- **Excellent detail** in vehicle impact classification
- Clear mapping to WZDx standard values
- Consistent categorization

### Texas
- **Good coverage** (92.6% non-unknown)
- Even distribution across impact types
- 7.4% unknown (still good)

**Impact Distribution**:

| Impact Level | California | Texas |
|-------------|-----------|-------|
| All-Lanes-Closed | Higher severity focus | 542 (24.9%) |
| Some-Lanes-Closed | Common | 740 (33.9%) |
| All-Lanes-Open | Common | 736 (33.8%) |
| Unknown | Low | 162 (7.4%) |

---

## Key Differences

### 1. Geographic Coverage
- **California**: Dense, localized (Bay Area only)
- **Texas**: Sparse, statewide (entire state)
- **Impact**: Texas provides broader geographic diversity

### 2. Data Granularity
- **California**: Real-time, detailed worker data
- **Texas**: Daily snapshots, no worker data
- **Impact**: California better for real-time safety analysis

### 3. Work Zone Characteristics
- **California**: Mix of project durations
- **Texas**: Predominantly short-term (daily/weekly)
- **Impact**: Different safety implications

### 4. Lane-Level Detail
- **California**: Core details in GeoJSON
- **Texas**: Detailed JSON in CSV field (embedded)
- **Impact**: Both have detailed lane info, different formats

### 5. Data Volume
- **California**: 1,186 unique work zones
- **Texas**: 288 unique zones, 2,180 records total
- **Impact**: Texas has temporal dimension (multiple dates per zone)

---

## Opportunities for Multi-State Analysis

### 1. **Comparative Safety Analysis**
- Compare crash rates near work zones: CA (Bay Area) vs. TX (major cities)
- Analyze if urban vs. rural work zones have different safety profiles
- Study impact of worker presence (CA has data, TX doesn't)

### 2. **Work Zone Duration Impact**
- California: Mix of durations
- Texas: Mostly short-term
- **Research Question**: Do short-term work zones have different crash patterns than long-term?

### 3. **Vehicle Impact Effectiveness**
- Both states classify vehicle impact
- **Research Question**: Does vehicle impact level correlate with crash severity?
- Can compare effectiveness of different closure strategies

### 4. **Regional Practices Comparison**
- Bay Area practices vs. Texas practices
- Urban vs. mixed urban/rural
- Dense vs. sparse work zone placement

### 5. **Lane Closure Strategies**
- Both datasets have detailed lane information
- **Research Question**: Which lane closure strategies are safest?
- Compare shoulder vs. lane closures

### 6. **Data Quality Impact**
- California: More complete data
- Texas: Broader coverage
- **Research Question**: Does data completeness affect safety outcomes?

---

## Recommendations for Capstone Project

### Option 1: **Multi-State Comparison Study**
Focus on comparing work zone practices and safety outcomes between California and Texas.

**Strengths**:
- Two diverse geographic regions
- Different data characteristics (quality vs. coverage)
- Rich comparison opportunities

**Challenges**:
- Different temporal characteristics
- Need crash data for both states (currently only have CA crashes)
- Geographic scale mismatch

### Option 2: **California Deep-Dive with Texas Validation**
Primary focus on California (crashes + work zones), use Texas for validation/generalization.

**Strengths**:
- Already have CA crash data
- Can do detailed spatial analysis
- Texas validates findings

**Challenges**:
- Need Texas crash data for validation
- Different work zone characteristics

### Option 3: **Work Zone Data Quality Analysis**
Study how data quality/completeness affects safety analysis capabilities.

**Strengths**:
- Novel research angle
- Both states provide good examples
- Practical implications for DOTs

**Challenges**:
- More methodological than safety-focused
- May need additional data sources

### Option 4: **Short-term vs. Long-term Work Zone Safety**
Use Texas (short-term focus) vs. California (mixed) to study duration impacts.

**Strengths**:
- Clear research question
- Both datasets support this
- Practical implications

**Challenges**:
- Need crash data for both states
- Confounding variables (location, traffic, etc.)

---

## Data Integration Possibilities

### Combined Dataset Potential
- **Total Work Zones**: 1,186 (CA) + 288 (TX unique) = **1,474 unique zones**
- **Total Records**: 1,186 (CA) + 2,180 (TX) = **3,366 records**
- **Geographic Diversity**: West Coast metro + Texas cities/highways
- **Temporal Diversity**: Real-time + dated snapshots

### Standardization Needs
1. Normalize vehicle impact categories
2. Standardize road names/types
3. Align temporal dimensions
4. Geocode to common coordinate system
5. Extract lane details from embedded JSON (Texas)

---

## Next Steps

### Immediate Actions
1. ✅ Analyze Texas data structure
2. ✅ Create Texas work zone map
3. ⏳ Obtain Texas crash data (if available from TIMS)
4. ⏳ Create multi-state comparison map
5. ⏳ Develop standardization pipeline

### Research Development
1. Define specific research questions
2. Identify confounding variables
3. Plan statistical analysis approach
4. Determine if additional states needed

### Data Acquisition
1. **Texas Crashes**: Check TIMS for Texas crash data
2. **Historical Work Zones**: Download from USDOT S3 (both states)
3. **Traffic Volume**: Add traffic data if needed for normalization
4. **Other States**: Consider adding NY, CO, or FL

---

## Strengths of Multi-State Approach

### For Your Capstone

**✅ Geographic Diversity**
- Urban vs. mixed urban/rural
- Different DOT practices
- Broader generalizability

**✅ Methodological Rigor**
- Cross-validation opportunities
- Comparative analysis
- Robustness checks

**✅ Practical Impact**
- Findings applicable to multiple states
- Can recommend best practices
- Policy-relevant insights

**✅ Data Richness**
- 3,366 total records
- Different temporal characteristics
- Complementary strengths (quality vs. coverage)

---

## Limitations to Consider

**⚠️ Different Temporal Scales**
- CA: Real-time
- TX: Snapshot (April 2024)
- May complicate direct comparisons

**⚠️ Geographic Mismatch**
- CA: Bay Area (localized, dense)
- TX: Statewide (sparse, distributed)
- Different contexts

**⚠️ Data Completeness Gaps**
- TX: No worker presence
- TX: No speed limits
- May limit some analyses

**⚠️ Crash Data Availability**
- Currently only have CA (Alameda County)
- Need TX crash data for full comparison
- Check TIMS availability

---

## Conclusion

Both datasets offer valuable but complementary perspectives:

**California** = **Quality + Detail**
- Excellent for detailed safety analysis
- Real-time worker presence
- High-quality coordinate data
- Perfect for crash correlation studies

**Texas** = **Coverage + Volume**
- Statewide perspective
- Multiple districts
- Temporal snapshot dimension
- Good for regional comparisons

**Together** = **Comprehensive Analysis**
- Geographic diversity
- Methodological rigor
- Cross-validation
- Generalizable findings

**Recommendation**: Pursue a **hybrid approach**:
1. **Primary analysis**: California (detailed crash + work zone integration)
2. **Validation**: Texas (test if findings generalize)
3. **Comparison**: Identify state-specific vs. universal patterns

This maximizes your existing CA crash data while leveraging TX for broader insights.

---

## Files Created

### Texas Analysis
- `scripts/analyze_texas_workzones.py` - Data exploration
- `scripts/create_texas_map.py` - Interactive map
- `outputs/visualizations/texas_workzone_analysis.png` - Charts
- `outputs/maps/texas_workzones_map.html` - Interactive map
- `docs/TEXAS_WORKZONE_SUMMARY.md` - Statistics summary
- `data/processed/texas_work_zones_analysis.csv` - Processed data

### Comparison
- `docs/TEXAS_VS_CALIFORNIA_COMPARISON.md` - This document

---

**Your Next Decision**: Choose research direction based on this comparison, then proceed with detailed analysis plan.
