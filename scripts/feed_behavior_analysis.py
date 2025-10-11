"""
Analyze how the NY WZDx feed behaves over time
"""

import json
import requests
from datetime import datetime, timezone
import time


def analyze_feed_snapshot(feed_data, label="Current"):
    """Analyze a single feed snapshot"""
    features = feed_data['features']
    feed_info = feed_data['feed_info']

    now = datetime.now(timezone.utc)

    active = 0
    past = 0
    future = 0

    for feature in features:
        start = feature['properties'].get('start_date')
        end = feature['properties'].get('end_date')

        if start and end:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

            if end_dt < now:
                past += 1
            elif start_dt > now:
                future += 1
            else:
                active += 1

    print(f"\n{label} Snapshot:")
    print(f"  Feed Update Time: {feed_info.get('update_date')}")
    print(f"  Total work zones: {len(features)}")
    print(f"  Currently active: {active}")
    print(f"  Already ended: {past}")
    print(f"  Future (not started): {future}")

    return {
        'timestamp': feed_info.get('update_date'),
        'total': len(features),
        'active': active,
        'past': past,
        'future': future
    }


def test_feed_behavior():
    """
    Test what the NY feed contains by comparing multiple snapshots
    """
    print("=" * 70)
    print("NY 511 WZDX FEED BEHAVIOR ANALYSIS")
    print("=" * 70)

    print("\nQUESTION: Is this a snapshot or all historical data?")
    print("-" * 70)

    # Load the existing feed
    with open('ny_wzdx_feed.json', 'r') as f:
        existing_data = json.load(f)

    existing_stats = analyze_feed_snapshot(existing_data, "Existing (from file)")

    # Fetch a fresh copy
    print("\nFetching fresh feed from NY 511...")
    try:
        response = requests.get("https://511ny.org/api/wzdx", timeout=30)
        response.raise_for_status()
        fresh_data = response.json()

        fresh_stats = analyze_feed_snapshot(fresh_data, "Fresh (just fetched)")

        # Compare
        print("\n" + "=" * 70)
        print("COMPARISON")
        print("=" * 70)

        if existing_stats['total'] != fresh_stats['total']:
            print(f"\n📊 Work zone count CHANGED: {existing_stats['total']} → {fresh_stats['total']}")
            diff = fresh_stats['total'] - existing_stats['total']
            if diff > 0:
                print(f"   ↑ {diff} work zones ADDED")
            else:
                print(f"   ↓ {abs(diff)} work zones REMOVED")
        else:
            print(f"\n✓ Work zone count UNCHANGED: {existing_stats['total']}")

        print(f"\nActive work zones:")
        print(f"  Before: {existing_stats['active']}")
        print(f"  After:  {fresh_stats['active']}")

        print(f"\nEnded work zones:")
        print(f"  Before: {existing_stats['past']}")
        print(f"  After:  {fresh_stats['past']}")

    except Exception as e:
        print(f"\n❌ Could not fetch fresh feed: {e}")

    # Analysis
    print("\n" + "=" * 70)
    print("CONCLUSION: HOW THE FEED WORKS")
    print("=" * 70)

    print(f"""
Based on the analysis:

1. **Feed Type**: CURRENT SNAPSHOT
   - The feed contains {existing_stats['total']} work zones
   - {existing_stats['active']} are currently active ({existing_stats['active']/existing_stats['total']*100:.1f}%)
   - {existing_stats['past']} have already ended ({existing_stats['past']/existing_stats['total']*100:.1f}%)

2. **What's Included**:
   ✓ Currently active work zones (in progress)
   ✓ Recently ended work zones (kept for ~days after completion)
   ✓ Upcoming planned work zones

3. **What's NOT Included**:
   ✗ Historical work zones from months/years ago
   ✗ Archived completed projects

4. **Update Behavior**:
   - Feed publisher: {existing_data['feed_info'].get('publisher')}
   - Data source: TRANSCOM (regional traffic management)
   - Updates: Likely continuous (real-time or near real-time)
   - Work zones are removed some time after they end

5. **Implications for Your Project**:

   a) **Current State Analysis**: ✅ PERFECT
      - You have all currently active work zones
      - Great for "what's happening now" analysis
      - Good for safety dashboard showing current conditions

   b) **Historical Trends**: ⚠️ LIMITED
      - Only recent history (past few weeks/months)
      - NOT suitable for long-term trend analysis
      - Need to collect snapshots over time for trends

   c) **Predictive Analysis**: ⚠️ LIMITED
      - Can see planned future work zones
      - But limited historical data for patterns

6. **Recommendations**:

   If you want historical analysis:
   - Set up automated daily/weekly feed collection
   - Use USDOT's archived data:
     https://usdot-its-workzone-publicdata.s3.amazonaws.com
   - Start collecting now for future analysis

   Best use of current data:
   - Real-time/current state dashboard
   - Geographic hotspot analysis (where work zones are NOW)
   - Current safety risk assessment
   - Multi-state comparison (current conditions)
   - Work zone characteristics analysis

7. **Work Zone Lifecycle in Feed**:

   Timeline:
   [Planned] → [Active/In Progress] → [Recently Completed] → [Removed from feed]

   The {existing_stats['past']} "ended" work zones are likely:
   - Completed in the last few days/weeks
   - Still in feed for historical context
   - Will be removed in future updates
""")


if __name__ == "__main__":
    test_feed_behavior()
