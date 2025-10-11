"""
Create quick visualizations of WZDx data to explore possibilities
"""

import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_ny_data():
    """Load the NY WZDx feed data"""
    with open('ny_wzdx_feed.json', 'r') as f:
        data = json.load(f)

    work_zones = []
    for feature in data['features']:
        props = feature['properties']
        core = props['core_details']

        wz = {
            'id': feature['id'],
            'road_name': ', '.join(core.get('road_names', [])),
            'description': core.get('description', ''),
            'start_date': pd.to_datetime(props.get('start_date')),
            'end_date': pd.to_datetime(props.get('end_date')),
            'update_date': pd.to_datetime(core.get('update_date')),
            'beginning_cross_street': props.get('beginning_cross_street', ''),
            'ending_cross_street': props.get('ending_cross_street', ''),
            'latitude': feature['geometry']['coordinates'][0][1] if feature['geometry']['coordinates'] else None,
            'longitude': feature['geometry']['coordinates'][0][0] if feature['geometry']['coordinates'] else None,
        }

        # Calculate duration
        if wz['start_date'] and wz['end_date']:
            wz['duration_days'] = (wz['end_date'] - wz['start_date']).days

        # Extract work type from description
        desc_lower = wz['description'].lower()
        if 'bridge' in desc_lower:
            wz['work_type'] = 'Bridge'
        elif 'utility' in desc_lower or 'utilities' in desc_lower:
            wz['work_type'] = 'Utility'
        elif 'paving' in desc_lower or 'pavement' in desc_lower:
            wz['work_type'] = 'Paving'
        elif 'barrier' in desc_lower:
            wz['work_type'] = 'Barrier'
        elif 'milling' in desc_lower:
            wz['work_type'] = 'Milling'
        else:
            wz['work_type'] = 'Other'

        # Extract highway type
        road = wz['road_name']
        if road.startswith('I-'):
            wz['highway_type'] = 'Interstate'
        elif road.startswith('US '):
            wz['highway_type'] = 'US Highway'
        elif road.startswith('NY '):
            wz['highway_type'] = 'State Route'
        elif 'parkway' in road.lower() or 'pkwy' in road.lower():
            wz['highway_type'] = 'Parkway'
        else:
            wz['highway_type'] = 'Other'

        work_zones.append(wz)

    return pd.DataFrame(work_zones)


def create_visualizations(df):
    """Create exploratory visualizations"""

    print("Creating visualizations...")

    # 1. Work Zone Duration Distribution
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    duration_bins = [0, 7, 30, 90, 180, 365, df['duration_days'].max()]
    duration_labels = ['<1 week', '1-4 weeks', '1-3 months', '3-6 months', '6-12 months', '>1 year']
    df['duration_category'] = pd.cut(df['duration_days'], bins=duration_bins, labels=duration_labels)
    df['duration_category'].value_counts().sort_index().plot(kind='bar', color='steelblue')
    plt.title('Work Zone Duration Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Duration')
    plt.ylabel('Number of Work Zones')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 2. Work Type Distribution
    plt.subplot(1, 2, 2)
    df['work_type'].value_counts().plot(kind='bar', color='coral')
    plt.title('Work Type Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Work Type')
    plt.ylabel('Number of Work Zones')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('work_zone_analysis_1.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: work_zone_analysis_1.png")
    plt.close()

    # 3. Highway Type Distribution
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    df['highway_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Work Zones by Highway Type', fontsize=14, fontweight='bold')
    plt.ylabel('')

    # 4. Duration by Work Type
    plt.subplot(1, 2, 2)
    work_type_duration = df.groupby('work_type')['duration_days'].mean().sort_values()
    work_type_duration.plot(kind='barh', color='teal')
    plt.title('Average Duration by Work Type', fontsize=14, fontweight='bold')
    plt.xlabel('Average Duration (days)')
    plt.ylabel('Work Type')
    plt.tight_layout()

    plt.savefig('work_zone_analysis_2.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: work_zone_analysis_2.png")
    plt.close()

    # 5. Start Date Timeline
    plt.figure(figsize=(14, 6))
    df['start_month'] = df['start_date'].dt.to_period('M')
    monthly_counts = df.groupby('start_month').size()
    monthly_counts.plot(kind='line', marker='o', linewidth=2, markersize=4, color='darkblue')
    plt.title('Work Zone Start Dates Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Number of Work Zones Started')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('work_zone_timeline.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: work_zone_timeline.png")
    plt.close()

    # 6. Top Roads with Most Work Zones
    plt.figure(figsize=(12, 6))
    top_roads = df['road_name'].value_counts().head(15)
    top_roads.plot(kind='barh', color='darkgreen')
    plt.title('Top 15 Roads by Number of Work Zones', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Active Work Zones')
    plt.ylabel('Road Name')
    plt.tight_layout()

    plt.savefig('top_roads.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: top_roads.png")
    plt.close()


def print_summary_stats(df):
    """Print summary statistics"""
    print("\n" + "=" * 70)
    print("NY WORK ZONE DATA - SUMMARY STATISTICS")
    print("=" * 70)

    print(f"\nTotal Work Zones: {len(df)}")
    print(f"Date Range: {df['start_date'].min().date()} to {df['end_date'].max().date()}")

    print(f"\nDuration Statistics:")
    print(f"  Average: {df['duration_days'].mean():.1f} days")
    print(f"  Median: {df['duration_days'].median():.1f} days")
    print(f"  Min: {df['duration_days'].min()} days")
    print(f"  Max: {df['duration_days'].max()} days")

    print(f"\nWork Types:")
    for work_type, count in df['work_type'].value_counts().items():
        print(f"  - {work_type}: {count} ({count/len(df)*100:.1f}%)")

    print(f"\nHighway Types:")
    for hwy_type, count in df['highway_type'].value_counts().items():
        print(f"  - {hwy_type}: {count} ({count/len(df)*100:.1f}%)")

    print(f"\nLongest Duration Work Zones:")
    longest = df.nlargest(5, 'duration_days')[['road_name', 'duration_days', 'work_type', 'start_date']]
    for idx, row in longest.iterrows():
        print(f"  - {row['road_name']}: {row['duration_days']} days ({row['work_type']}, started {row['start_date'].date()})")

    print(f"\nMost Common Roads:")
    for road, count in df['road_name'].value_counts().head(5).items():
        print(f"  - {road}: {count} work zones")


def main():
    print("Loading NY WZDx data...")
    df = load_ny_data()

    print_summary_stats(df)
    create_visualizations(df)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - work_zone_analysis_1.png")
    print("  - work_zone_analysis_2.png")
    print("  - work_zone_timeline.png")
    print("  - top_roads.png")
    print("  - ny_work_zones_analysis.csv")


if __name__ == "__main__":
    main()
