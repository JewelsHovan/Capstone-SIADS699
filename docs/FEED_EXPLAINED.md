# How the NY WZDx Feed Works - Explained

## Quick Answer

**The NY 511 WZDx feed is a CURRENT SNAPSHOT, not historical data.**

It shows:
- ✅ Currently active work zones (1,096 work zones)
- ✅ Recently completed work zones (42 work zones, kept briefly)
- ✅ Upcoming planned work zones (0 currently)
- ❌ NOT historical data from months/years ago

**Updates**: The feed updates continuously (every ~10 minutes based on timestamp changes)

---

## What We Discovered

### Live Test Results (Oct 10, 2025)

We fetched the feed twice, 11 minutes apart:

**First fetch (12:19 PM)**:
- Total: 1,138 work zones
- Currently active: 1,096
- Already ended: 42

**Second fetch (12:30 PM)**:
- Total: 1,137 work zones (-1)
- Currently active: 1,096
- Already ended: 41 (-1)

**Conclusion**: One completed work zone was removed from the feed in those 11 minutes!

---

## Feed Behavior

### What Gets Added to Feed
1. **New work zones** when they're planned/scheduled
2. **Active construction** as it happens
3. **Ongoing long-term projects**

### What Gets Removed from Feed
1. **Completed work zones** (after a brief retention period)
2. **Canceled projects**
3. **Old historical data**

### Timeline of a Work Zone in the Feed

```
Planning → Added to Feed → Active → Completed → Stays briefly → REMOVED
                ↑                                      ↑
         (You see this)                          (Gone after ~days)
```

---

## Current Feed Contents (Oct 10, 2025)

### Status Breakdown
- **Currently Active**: 1,096 work zones (96.3%)
  - These are happening RIGHT NOW
  - Workers on site, lanes closed, etc.

- **Recently Ended**: 42 work zones (3.7%)
  - Completed in last few days/weeks
  - Still in feed for recent historical context
  - Will be removed soon

- **Future/Planned**: 0 work zones
  - Would appear if scheduled for future

### Temporal Coverage
- **Earliest start date**: August 15, 2021 (long-term project still active)
- **Latest end date**: January 1, 2029 (planned multi-year project)
- **Current work zones**: Mostly started in 2024-2025

---

## Implications for Your Project

### ✅ What You CAN Do (Great Use Cases)

1. **Current State Analysis**
   - Map all active work zones RIGHT NOW
   - Identify current safety hotspots
   - Show drivers where work zones are today
   - Compare current conditions across states

2. **Work Zone Characteristics**
   - Analyze typical work zone durations
   - Study work types (bridge, paving, utility)
   - Geographic distribution patterns
   - Highway type analysis (Interstate vs. State Route)

3. **Safety Dashboard**
   - Real-time work zone viewer
   - Current risk assessment
   - Live traffic impact
   - Worker presence (if available in feed)

4. **Multi-State Comparison**
   - Compare NY vs. Colorado vs. Iowa (all current)
   - Data quality assessment
   - Best practices by state

5. **Snapshot Analysis**
   - "On any given day, how many work zones are active?"
   - Current burden on road network
   - Resources currently deployed

### ⚠️ What You CANNOT Do (Limited Use Cases)

1. **Long-Term Trends**
   - ❌ Can't analyze: "How have work zones changed over 5 years?"
   - ❌ Can't study: "Seasonal patterns over multiple years"
   - ❌ Can't track: "Historical safety improvements"

2. **Predictive Modeling**
   - ⚠️ Limited: No extensive historical data for training
   - ⚠️ Limited: Can't predict based on past patterns
   - ⚠️ But you CAN: Analyze planned future work zones

3. **Before/After Studies**
   - ❌ Can't compare: "2019 vs 2024 work zone practices"
   - ❌ Can't evaluate: Long-term policy impacts

---

## How to Get Historical Data

### Option 1: USDOT Archive (RECOMMENDED)
**USDOT ITS Work Zone Sandbox** - Free public access!

🔗 **Access**: https://usdot-its-workzone-publicdata.s3.amazonaws.com/index.html

**What's Available**:
- **Semi-processed data**: Monthly snapshots, change tracking
- **Raw data**: Original feed snapshots
- **Multiple states**: NY, CO, IA, MA, TX, and more
- **Time range**: Varies by state (some go back months/years)

**Data Structure**:
```
state={state}/feedName={feedName}/year={year}/month={month}/
```

Example:
```
state=NewYork/feedName=511ny/year=2024/month=08/
state=NewYork/feedName=511ny/year=2024/month=09/
state=NewYork/feedName=511ny/year=2024/month=10/
```

**Benefits**:
- ✅ Free and public
- ✅ Already collected for you
- ✅ Standardized format
- ✅ Multiple states available

### Option 2: Collect Your Own
Set up automated daily/weekly snapshots:

```python
import requests
import json
from datetime import datetime

def collect_daily_snapshot():
    url = "https://511ny.org/api/wzdx"
    response = requests.get(url)
    data = response.json()

    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ny_wzdx_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(data, f)
```

Run this daily with cron/scheduler to build your own archive.

**Benefits**:
- ✅ Most recent data
- ✅ You control frequency
- ✅ Can start NOW for future analysis

**Drawbacks**:
- ❌ No past data
- ❌ Takes time to accumulate
- ❌ Requires ongoing automation

---

## Recommended Project Approach

Given that you have **snapshot data**, here's what works best:

### Best Project Types

#### 1. **Real-Time Safety Dashboard** ⭐ (HIGHLY RECOMMENDED)
**Why it works**: Uses current snapshot perfectly
- Map showing all 1,096 active work zones
- Filter by work type, highway type, duration
- Show high-risk zones (long duration + major highways)
- Compare across multiple states (all current)
- Calculate current safety metrics

**Deliverable**: Interactive web dashboard

#### 2. **Geographic Analysis**
**Why it works**: Snapshot shows spatial patterns
- Work zone density heat maps
- Highway corridor analysis (I-81, I-84, I-95)
- Regional hotspot identification
- Urban vs. rural patterns
- Multi-state comparison

**Deliverable**: Maps + analysis report

#### 3. **Work Zone Characterization Study**
**Why it works**: Current data shows typical characteristics
- Duration analysis (short vs. long-term)
- Work type distribution
- Lane closure patterns
- Complexity analysis
- Data quality assessment across states

**Deliverable**: Research paper with recommendations

#### 4. **Enhanced with Historical Archive** ⭐⭐
**Best of both worlds**: Current + USDOT archive
- Download historical data from USDOT S3 bucket
- Combine with current snapshot
- Show trends over time
- Seasonal pattern analysis
- Policy impact evaluation

**Deliverable**: Comprehensive dashboard + trend analysis

---

## Next Steps Based on Feed Type

### If Using Current Snapshot Only

1. **Fetch multiple state feeds** (CO, IA, MA, TX)
   - Get current snapshot from each
   - Compare data quality
   - Analyze regional differences

2. **Create geographic visualizations**
   - Map all work zones
   - Identify hotspots
   - Show current conditions

3. **Build interactive dashboard**
   - Let users explore current work zones
   - Filter and search
   - Display safety metrics

### If Adding Historical Data

1. **Explore USDOT S3 bucket**
   ```
   https://usdot-its-workzone-publicdata.s3.amazonaws.com/index.html
   ```

2. **Download historical snapshots**
   - Pick your state(s)
   - Download monthly data
   - Parse and combine

3. **Enhanced analysis**
   - Trend analysis
   - Seasonal patterns
   - Before/after comparisons
   - Predictive modeling

---

## Summary

**Feed Type**: Live snapshot (refreshed every ~10 minutes)

**Contains**:
- ✅ Active work zones
- ✅ Recently ended (brief retention)
- ✅ Planned future work
- ❌ NO long-term historical archive

**Best For**:
- Current state analysis
- Geographic patterns
- Multi-state comparison
- Real-time dashboards
- Work zone characteristics

**Not Ideal For**:
- Long-term trends (without archive)
- Historical comparisons
- Predictive modeling (without archive)

**Solution for Historical Data**:
- Use USDOT's Work Zone Sandbox archive
- OR start collecting daily snapshots now

**Your Data** (as of Oct 10, 2025):
- 1,096 currently active work zones
- Statewide NY coverage
- Rich descriptions and coordinates
- Perfect for capstone dashboard!

---

## Questions?

**Q: Will my analysis be outdated quickly?**
A: For current snapshot analysis - yes, it changes daily. But that's the point! You're showing "current conditions" which is valuable. For historical analysis, use the USDOT archive.

**Q: Should I collect my own historical data?**
A: Only if you want data newer than what USDOT has archived. Check their archive first - it likely has what you need.

**Q: Can I still do a good capstone with just snapshot data?**
A: Absolutely! A real-time safety dashboard with current data from 5+ states is an excellent capstone project.

**Q: How often should I refresh my dashboard?**
A: Daily is fine for a capstone. Real-world applications might update hourly or more frequently.
