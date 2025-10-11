"""
Texas DOT Work Zone Data Analysis
Explores TxDOT Work Zone Data Schema Version 2.0
"""

import pandas as pd
import json
import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def load_texas_data(csv_path='data/Texas_DOT__TxDOT__Work_Zone_Data_Schema_Version_2.0.csv'):
    """Load Texas DOT work zone data"""
    if not os.path.isabs(csv_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, csv_path)

    print("Loading Texas DOT work zone data...")
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"✓ Loaded {len(df):,} work zone records")
    print(f"✓ Found {len(df.columns)} columns")
    return df

def extract_coordinates(df):
    """Extract coordinates from geometry fields"""
    print("\nExtracting coordinates from geometry fields...")

    coords = []
    for idx, row in df.iterrows():
        lat, lon = None, None

        # Try geometry_multipoint first
        multipoint = row.get('geometry_multipoint', '')
        if pd.notna(multipoint) and multipoint != '':
            # Parse MULTIPOINT ((-106.323587 31.676631))
            match = re.search(r'\(\(([^)]+)\)\)', str(multipoint))
            if match:
                coord_str = match.group(1)
                parts = coord_str.split()
                if len(parts) >= 2:
                    lon = float(parts[0])
                    lat = float(parts[1])

        # Try geometry_linestring if multipoint failed
        if lat is None and lon is None:
            linestring = row.get('geometry_linestring', '')
            if pd.notna(linestring) and linestring != '':
                # Parse LINESTRING ((-106.323587 31.676631, ...))
                match = re.search(r'\(\(([^,]+)', str(linestring))
                if match:
                    coord_str = match.group(1).strip()
                    parts = coord_str.split()
                    if len(parts) >= 2:
                        lon = float(parts[0])
                        lat = float(parts[1])

        coords.append({'latitude': lat, 'longitude': lon})

    coord_df = pd.DataFrame(coords)
    df['latitude'] = coord_df['latitude']
    df['longitude'] = coord_df['longitude']

    valid_coords = df[['latitude', 'longitude']].notna().all(axis=1).sum()
    print(f"✓ Extracted coordinates for {valid_coords:,} records ({valid_coords/len(df)*100:.1f}%)")

    return df

def basic_info(df):
    """Display basic dataset information"""
    print("\n" + "="*60)
    print("TEXAS DOT WORK ZONE OVERVIEW")
    print("="*60)

    print(f"\nTotal Work Zone Records: {len(df):,}")

    # Date range
    df['start_date_parsed'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date_parsed'] = pd.to_datetime(df['end_date'], errors='coerce')

    print(f"\nDate Range:")
    print(f"  Start Dates: {df['start_date_parsed'].min()} to {df['start_date_parsed'].max()}")
    print(f"  End Dates: {df['end_date_parsed'].min()} to {df['end_date_parsed'].max()}")

    # Feed update
    print(f"\nFeed Information:")
    if 'road_event_feed_info_feed_update_date' in df.columns:
        feed_dates = df['road_event_feed_info_feed_update_date'].value_counts()
        if len(feed_dates) > 0:
            print(f"  Last Update: {feed_dates.index[0]}")
        print(f"  Schema Version: {df['road_event_feed_info_version'].iloc[0] if 'road_event_feed_info_version' in df.columns else 'Unknown'}")

    # Issuing organization
    print(f"\nIssuing Organizations:")
    orgs = df['issuing_organization'].value_counts() if 'issuing_organization' in df.columns else {}
    for org, count in list(orgs.items())[:5]:
        print(f"  {org}: {count:,} records")

    # Coordinates
    valid_coords = df[['latitude', 'longitude']].notna().all(axis=1).sum()
    print(f"\nGeographic Coverage:")
    print(f"  Records with Coordinates: {valid_coords:,} ({valid_coords/len(df)*100:.1f}%)")

def unique_work_zones(df):
    """Analyze unique work zones (multiple records may be same zone on different dates)"""
    print("\n" + "="*60)
    print("UNIQUE WORK ZONE ANALYSIS")
    print("="*60)

    # Extract base road_event_id (before the date suffix)
    df['base_event_id'] = df['road_event_id'].apply(
        lambda x: x.split('+')[0] if pd.notna(x) else None
    )

    unique_zones = df['base_event_id'].nunique()
    total_records = len(df)

    print(f"\nTotal Records: {total_records:,}")
    print(f"Unique Work Zones: {unique_zones:,}")
    print(f"Average Records per Work Zone: {total_records/unique_zones:.1f}")
    print("\n(Note: Same work zone may have multiple records for different dates)")

def vehicle_impact_analysis(df):
    """Analyze vehicle impact levels"""
    print("\n" + "="*60)
    print("VEHICLE IMPACT ANALYSIS")
    print("="*60)

    if 'vehicle_impact' in df.columns:
        impact_counts = df['vehicle_impact'].value_counts()
        print("\nVehicle Impact Distribution:")
        for impact, count in impact_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {impact}: {count:,} ({pct:.1f}%)")
    else:
        print("Vehicle impact data not available")

def worker_presence_analysis(df):
    """Analyze worker presence"""
    print("\n" + "="*60)
    print("WORKER PRESENCE ANALYSIS")
    print("="*60)

    if 'workers_present' in df.columns:
        workers = df['workers_present'].value_counts()
        print("\nWorker Presence:")
        for status, count in workers.items():
            print(f"  {status}: {count:,}")
    else:
        print("Worker presence data not available")

def location_analysis(df):
    """Analyze work zone locations"""
    print("\n" + "="*60)
    print("LOCATION ANALYSIS")
    print("="*60)

    # Top roads
    print("\nTop 10 Roads by Work Zone Count:")
    if 'road_name' in df.columns:
        road_counts = df['road_name'].value_counts().head(10)
        for road, count in road_counts.items():
            print(f"  {road}: {count:,}")

    # Directions
    if 'direction' in df.columns:
        print("\nDirections:")
        dir_counts = df['direction'].value_counts()
        for direction, count in dir_counts.items():
            if pd.notna(direction) and direction != '':
                print(f"  {direction}: {count:,}")

    # Regions (from subidentifier)
    if 'subidentifier' in df.columns:
        print("\nTop 10 Regions/Districts:")
        region_counts = df['subidentifier'].value_counts().head(10)
        for region, count in region_counts.items():
            print(f"  {region}: {count:,}")

def temporal_analysis(df):
    """Analyze temporal patterns"""
    print("\n" + "="*60)
    print("TEMPORAL PATTERNS")
    print("="*60)

    if 'start_date_parsed' in df.columns and 'end_date_parsed' in df.columns:
        # Active work zones
        now = pd.Timestamp.now()
        active = df[(df['start_date_parsed'] <= now) & (df['end_date_parsed'] >= now)]
        print(f"\nCurrently Active Work Zones: {len(active):,}")

        # Duration analysis
        df['duration_days'] = (df['end_date_parsed'] - df['start_date_parsed']).dt.days
        valid_duration = df[df['duration_days'].notna()]

        if len(valid_duration) > 0:
            print(f"\nDuration Statistics:")
            print(f"  Mean: {valid_duration['duration_days'].mean():.1f} days")
            print(f"  Median: {valid_duration['duration_days'].median():.1f} days")
            print(f"  Min: {valid_duration['duration_days'].min():.0f} days")
            print(f"  Max: {valid_duration['duration_days'].max():.0f} days")

            # Duration categories
            short = (valid_duration['duration_days'] <= 7).sum()
            medium = ((valid_duration['duration_days'] > 7) & (valid_duration['duration_days'] <= 30)).sum()
            long = (valid_duration['duration_days'] > 30).sum()

            print(f"\nDuration Categories:")
            print(f"  Short-term (≤7 days): {short:,}")
            print(f"  Medium-term (8-30 days): {medium:,}")
            print(f"  Long-term (>30 days): {long:,}")

def data_quality_comparison(df):
    """Compare with California WZDx data quality"""
    print("\n" + "="*60)
    print("DATA QUALITY ASSESSMENT")
    print("="*60)

    print("\nField Completeness:")

    fields = {
        'road_name': 'Road Name',
        'direction': 'Direction',
        'vehicle_impact': 'Vehicle Impact',
        'workers_present': 'Workers Present',
        'reduced_speed_limit': 'Speed Limit',
        'description': 'Description',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'latitude': 'Coordinates',
    }

    for field, label in fields.items():
        if field in df.columns:
            if field == 'latitude':
                complete = df[['latitude', 'longitude']].notna().all(axis=1).sum()
            else:
                complete = df[field].notna().sum()
            pct = (complete / len(df)) * 100
            print(f"  {label}: {complete:,} ({pct:.1f}%)")

def create_visualizations(df, output_dir='outputs/visualizations'):
    """Create visualization charts"""
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)

    if not os.path.isabs(output_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    # Set style
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Vehicle Impact
    if 'vehicle_impact' in df.columns:
        impact_data = df['vehicle_impact'].value_counts()
        axes[0, 0].bar(range(len(impact_data)), impact_data.values, color='steelblue')
        axes[0, 0].set_xticks(range(len(impact_data)))
        axes[0, 0].set_xticklabels([str(x)[:20] for x in impact_data.index], rotation=45, ha='right', fontsize=9)
        axes[0, 0].set_title('Vehicle Impact Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('Number of Work Zones')
        axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Top regions
    if 'subidentifier' in df.columns:
        region_data = df['subidentifier'].value_counts().head(10)
        axes[0, 1].barh(range(len(region_data)), region_data.values, color='coral')
        axes[0, 1].set_yticks(range(len(region_data)))
        axes[0, 1].set_yticklabels(region_data.index, fontsize=9)
        axes[0, 1].set_title('Top 10 Regions/Districts', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Number of Work Zones')
        axes[0, 1].grid(axis='x', alpha=0.3)
        axes[0, 1].invert_yaxis()

    # 3. Duration distribution
    if 'duration_days' in df.columns:
        duration_valid = df[df['duration_days'].notna() & (df['duration_days'] > 0) & (df['duration_days'] < 365)]
        if len(duration_valid) > 0:
            axes[1, 0].hist(duration_valid['duration_days'], bins=50, color='mediumseagreen', edgecolor='black')
            axes[1, 0].set_title('Work Zone Duration Distribution', fontsize=14, fontweight='bold')
            axes[1, 0].set_xlabel('Duration (days)')
            axes[1, 0].set_ylabel('Number of Work Zones')
            axes[1, 0].grid(axis='y', alpha=0.3)

    # 4. Top roads
    if 'road_name' in df.columns:
        road_data = df['road_name'].value_counts().head(10)
        axes[1, 1].barh(range(len(road_data)), road_data.values, color='purple')
        axes[1, 1].set_yticks(range(len(road_data)))
        axes[1, 1].set_yticklabels([str(x)[:30] for x in road_data.index], fontsize=9)
        axes[1, 1].set_title('Top 10 Roads by Work Zone Count', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Number of Work Zones')
        axes[1, 1].grid(axis='x', alpha=0.3)
        axes[1, 1].invert_yaxis()

    plt.tight_layout()
    output_path = os.path.join(output_dir, 'texas_workzone_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved visualization: {output_path}")
    plt.close()

def export_summary(df, output_dir='docs'):
    """Export summary report"""
    print("\n" + "="*60)
    print("EXPORTING SUMMARY REPORT")
    print("="*60)

    if not os.path.isabs(output_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'TEXAS_WORKZONE_SUMMARY.md')

    with open(output_path, 'w') as f:
        f.write("# Texas DOT Work Zone Data Summary\n\n")
        f.write(f"**Data Source**: TxDOT Work Zone Data Schema Version 2.0\n")
        f.write(f"**Date Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Dataset Overview\n\n")
        f.write(f"- **Total Records**: {len(df):,}\n")

        # Unique zones
        unique_zones = df['base_event_id'].nunique() if 'base_event_id' in df.columns else len(df)
        f.write(f"- **Unique Work Zones**: {unique_zones:,}\n")

        # Date range
        if 'start_date_parsed' in df.columns:
            f.write(f"- **Date Range**: {df['start_date_parsed'].min()} to {df['end_date_parsed'].max()}\n")

        # Coordinates
        valid_coords = df[['latitude', 'longitude']].notna().all(axis=1).sum()
        f.write(f"- **Records with Coordinates**: {valid_coords:,} ({valid_coords/len(df)*100:.1f}%)\n\n")

        f.write("## Vehicle Impact Distribution\n\n")
        if 'vehicle_impact' in df.columns:
            impact_counts = df['vehicle_impact'].value_counts()
            for impact, count in impact_counts.items():
                pct = (count / len(df)) * 100
                f.write(f"- **{impact}**: {count:,} ({pct:.1f}%)\n")

        f.write("\n## Top 10 Regions/Districts\n\n")
        if 'subidentifier' in df.columns:
            regions = df['subidentifier'].value_counts().head(10)
            for i, (region, count) in enumerate(regions.items(), 1):
                f.write(f"{i}. **{region}**: {count:,} work zones\n")

        f.write("\n## Top 10 Roads\n\n")
        if 'road_name' in df.columns:
            roads = df['road_name'].value_counts().head(10)
            for i, (road, count) in enumerate(roads.items(), 1):
                f.write(f"{i}. **{road}**: {count:,} work zones\n")

        f.write("\n---\n\n")
        f.write("*See outputs/visualizations/texas_workzone_analysis.png for visual analysis*\n")

    print(f"✓ Saved summary report: {output_path}")

def main():
    """Main analysis workflow"""
    print("\n" + "="*60)
    print("TEXAS DOT WORK ZONE DATA ANALYSIS")
    print("="*60)

    # Load data
    df = load_texas_data()

    # Extract coordinates
    df = extract_coordinates(df)

    # Run analyses
    basic_info(df)
    unique_work_zones(df)
    vehicle_impact_analysis(df)
    worker_presence_analysis(df)
    location_analysis(df)
    temporal_analysis(df)
    data_quality_comparison(df)

    # Create visualizations
    create_visualizations(df)

    # Export summary
    export_summary(df)

    # Save processed data with coordinates
    output_path = 'data/processed/texas_work_zones_analysis.csv'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, output_path)

    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved processed data: {output_path}")

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  - outputs/visualizations/texas_workzone_analysis.png")
    print("  - docs/TEXAS_WORKZONE_SUMMARY.md")
    print("  - data/processed/texas_work_zones_analysis.csv")
    print("\nNext step: Create Texas work zone map")
    print("  Run: python scripts/create_texas_map.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
