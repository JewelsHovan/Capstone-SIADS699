"""
Crash Data Analysis Script
Explores crash data from TIMS (UC Berkeley) and generates summary statistics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def load_crash_data(csv_path='data/Crashes.csv'):
    """Load crash data from CSV"""
    print("Loading crash data...")
    # Handle both absolute and relative paths
    if not os.path.isabs(csv_path):
        # Get the script's directory and go up one level to project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, csv_path)
    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df):,} crash records")
    print(f"✓ Found {len(df.columns)} columns")
    return df

def basic_info(df):
    """Display basic dataset information"""
    print("\n" + "="*60)
    print("CRASH DATA OVERVIEW")
    print("="*60)

    print(f"\nTotal Crashes: {len(df):,}")
    print(f"Date Range: {df['COLLISION_DATE'].min()} to {df['COLLISION_DATE'].max()}")

    # Geographic coverage
    print(f"\nGeographic Coverage:")
    print(f"  County: {df['COUNTY'].unique()}")
    cities = df['CITY'].value_counts()
    print(f"  Cities: {len(cities)} unique cities")
    print(f"  Top 5 cities:")
    for city, count in cities.head(5).items():
        print(f"    - {city}: {count:,} crashes")

    # Data completeness
    print(f"\nData Completeness:")
    print(f"  Records with coordinates: {df[['LATITUDE', 'LONGITUDE']].notna().all(axis=1).sum():,}")
    print(f"  Missing coordinates: {df[['LATITUDE', 'LONGITUDE']].isna().any(axis=1).sum():,}")

def severity_analysis(df):
    """Analyze crash severity"""
    print("\n" + "="*60)
    print("SEVERITY ANALYSIS")
    print("="*60)

    severity_map = {
        1: 'Fatal',
        2: 'Severe Injury',
        3: 'Other Visible Injury',
        4: 'Complaint of Pain',
        0: 'Property Damage Only'
    }

    severity_counts = df['COLLISION_SEVERITY'].value_counts().sort_index()
    print("\nCrash Severity Distribution:")
    for sev, count in severity_counts.items():
        sev_name = severity_map.get(sev, f'Unknown ({sev})')
        pct = (count / len(df)) * 100
        print(f"  {sev_name}: {count:,} ({pct:.1f}%)")

    # Fatalities and injuries
    print(f"\nCasualties:")
    print(f"  Total Killed: {df['NUMBER_KILLED'].sum():,.0f}")
    print(f"  Total Injured: {df['NUMBER_INJURED'].sum():,.0f}")
    print(f"  Crashes with Fatalities: {(df['NUMBER_KILLED'] > 0).sum():,}")
    print(f"  Crashes with Injuries: {(df['NUMBER_INJURED'] > 0).sum():,}")

def crash_type_analysis(df):
    """Analyze crash types and factors"""
    print("\n" + "="*60)
    print("CRASH TYPE ANALYSIS")
    print("="*60)

    # Special crash types (handle string/numeric mix)
    print("\nSpecial Crash Types:")

    # Convert to numeric, handling errors
    ped = pd.to_numeric(df['PEDESTRIAN_ACCIDENT'], errors='coerce').sum()
    bike = pd.to_numeric(df['BICYCLE_ACCIDENT'], errors='coerce').sum()
    mc = pd.to_numeric(df['MOTORCYCLE_ACCIDENT'], errors='coerce').sum()
    truck = pd.to_numeric(df['TRUCK_ACCIDENT'], errors='coerce').sum()

    print(f"  Pedestrian: {int(ped):,}")
    print(f"  Bicycle: {int(bike):,}")
    print(f"  Motorcycle: {int(mc):,}")
    print(f"  Truck: {int(truck):,}")
    print(f"  Hit-and-Run: {df['HIT_AND_RUN'].notna().sum():,}")

    # Alcohol involvement
    alcohol_yes = (df['ALCOHOL_INVOLVED'] == 'Y').sum()
    print(f"\nAlcohol-Involved: {alcohol_yes:,} ({(alcohol_yes/len(df)*100):.1f}%)")

def environmental_conditions(df):
    """Analyze environmental conditions"""
    print("\n" + "="*60)
    print("ENVIRONMENTAL CONDITIONS")
    print("="*60)

    # Weather
    print("\nWeather Conditions:")
    weather_counts = df['WEATHER_1'].value_counts().head(5)
    for weather, count in weather_counts.items():
        print(f"  {weather}: {count:,}")

    # Road surface
    print("\nRoad Surface:")
    surface_counts = df['ROAD_SURFACE'].value_counts().head(5)
    for surface, count in surface_counts.items():
        print(f"  {surface}: {count:,}")

    # Lighting
    print("\nLighting Conditions:")
    lighting_counts = df['LIGHTING'].value_counts().head(5)
    for lighting, count in lighting_counts.items():
        print(f"  {lighting}: {count:,}")

def temporal_analysis(df):
    """Analyze temporal patterns"""
    print("\n" + "="*60)
    print("TEMPORAL PATTERNS")
    print("="*60)

    # Day of week
    dow_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
               5: 'Thursday', 6: 'Friday', 7: 'Saturday'}

    print("\nCrashes by Day of Week:")
    dow_counts = df['DAY_OF_WEEK'].value_counts().sort_index()
    for dow, count in dow_counts.items():
        dow_name = dow_map.get(dow, f'Unknown ({dow})')
        print(f"  {dow_name}: {count:,}")

    # Time of day (if available and parseable)
    print("\nTop Crash Hours (sample):")
    # Extract hour from COLLISION_TIME (format varies, so this is approximate)
    try:
        df['hour'] = pd.to_numeric(df['COLLISION_TIME'].astype(str).str.strip().str[:2], errors='coerce')
        hour_counts = df['hour'].value_counts().sort_index().head(10)
        for hour, count in hour_counts.items():
            if pd.notna(hour):
                print(f"  {int(hour):02d}:00 hour: {count:,}")
    except:
        print("  (Time parsing not available)")

def location_analysis(df):
    """Analyze crash locations"""
    print("\n" + "="*60)
    print("LOCATION ANALYSIS")
    print("="*60)

    # Top roads
    print("\nTop 10 Roads by Crash Count:")
    road_counts = df['PRIMARY_RD'].value_counts().head(10)
    for road, count in road_counts.items():
        print(f"  {road}: {count:,}")

    # Intersection vs non-intersection
    intersections = (df['INTERSECTION'] == 'Y').sum()
    print(f"\nIntersection Crashes: {intersections:,} ({(intersections/len(df)*100):.1f}%)")

def create_visualizations(df, output_dir='outputs/visualizations'):
    """Create visualization charts"""
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)

    # Handle relative paths
    if not os.path.isabs(output_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 10)

    # Create 2x2 subplot
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Severity distribution
    severity_map = {
        1: 'Fatal',
        2: 'Severe Injury',
        3: 'Visible Injury',
        4: 'Pain',
        0: 'Property Only'
    }
    severity_data = df['COLLISION_SEVERITY'].value_counts().sort_index()
    severity_labels = [severity_map.get(k, f'Code {k}') for k in severity_data.index]
    axes[0, 0].bar(range(len(severity_data)), severity_data.values, color='steelblue')
    axes[0, 0].set_xticks(range(len(severity_data)))
    axes[0, 0].set_xticklabels(severity_labels, rotation=45, ha='right')
    axes[0, 0].set_title('Crash Severity Distribution', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Number of Crashes')
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Day of week
    dow_map = {1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat'}
    dow_data = df['DAY_OF_WEEK'].value_counts().sort_index()
    dow_labels = [dow_map.get(k, str(k)) for k in dow_data.index]
    axes[0, 1].bar(range(len(dow_data)), dow_data.values, color='coral')
    axes[0, 1].set_xticks(range(len(dow_data)))
    axes[0, 1].set_xticklabels(dow_labels)
    axes[0, 1].set_title('Crashes by Day of Week', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Number of Crashes')
    axes[0, 1].grid(axis='y', alpha=0.3)

    # 3. Special crash types (handle type issues)
    crash_types = {
        'Pedestrian': int(pd.to_numeric(df['PEDESTRIAN_ACCIDENT'], errors='coerce').sum()),
        'Bicycle': int(pd.to_numeric(df['BICYCLE_ACCIDENT'], errors='coerce').sum()),
        'Motorcycle': int(pd.to_numeric(df['MOTORCYCLE_ACCIDENT'], errors='coerce').sum()),
        'Truck': int(pd.to_numeric(df['TRUCK_ACCIDENT'], errors='coerce').sum()),
        'Hit-and-Run': df['HIT_AND_RUN'].notna().sum(),
        'Alcohol': (df['ALCOHOL_INVOLVED'] == 'Y').sum()
    }
    axes[1, 0].barh(list(crash_types.keys()), list(crash_types.values()), color='mediumseagreen')
    axes[1, 0].set_title('Special Crash Types', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Number of Crashes')
    axes[1, 0].grid(axis='x', alpha=0.3)

    # 4. Top 10 roads
    top_roads = df['PRIMARY_RD'].value_counts().head(10)
    axes[1, 1].barh(range(len(top_roads)), top_roads.values, color='purple')
    axes[1, 1].set_yticks(range(len(top_roads)))
    axes[1, 1].set_yticklabels(top_roads.index, fontsize=9)
    axes[1, 1].set_title('Top 10 Roads by Crash Count', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Number of Crashes')
    axes[1, 1].grid(axis='x', alpha=0.3)
    axes[1, 1].invert_yaxis()

    plt.tight_layout()
    output_path = os.path.join(output_dir, 'crash_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved visualization: {output_path}")
    plt.close()

def export_summary(df, output_dir='docs'):
    """Export summary statistics to markdown"""
    print("\n" + "="*60)
    print("EXPORTING SUMMARY REPORT")
    print("="*60)

    # Handle relative paths
    if not os.path.isabs(output_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'CRASH_DATA_SUMMARY.md')

    with open(output_path, 'w') as f:
        f.write("# Crash Data Analysis Summary\n\n")
        f.write(f"**Data Source**: TIMS (Transportation Injury Mapping System - UC Berkeley)\n")
        f.write(f"**Date Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Dataset Overview\n\n")
        f.write(f"- **Total Crashes**: {len(df):,}\n")
        f.write(f"- **Date Range**: {df['COLLISION_DATE'].min()} to {df['COLLISION_DATE'].max()}\n")
        f.write(f"- **County**: {df['COUNTY'].unique()[0]}\n")
        f.write(f"- **Cities Covered**: {df['CITY'].nunique()}\n")
        f.write(f"- **Records with Coordinates**: {df[['LATITUDE', 'LONGITUDE']].notna().all(axis=1).sum():,}\n\n")

        f.write("## Key Statistics\n\n")
        f.write(f"- **Total Fatalities**: {df['NUMBER_KILLED'].sum():,.0f}\n")
        f.write(f"- **Total Injuries**: {df['NUMBER_INJURED'].sum():,.0f}\n")
        f.write(f"- **Pedestrian Crashes**: {int(pd.to_numeric(df['PEDESTRIAN_ACCIDENT'], errors='coerce').sum()):,}\n")
        f.write(f"- **Bicycle Crashes**: {int(pd.to_numeric(df['BICYCLE_ACCIDENT'], errors='coerce').sum()):,}\n")
        f.write(f"- **Motorcycle Crashes**: {int(pd.to_numeric(df['MOTORCYCLE_ACCIDENT'], errors='coerce').sum()):,}\n")
        f.write(f"- **Alcohol-Involved**: {(df['ALCOHOL_INVOLVED'] == 'Y').sum():,}\n\n")

        f.write("## Severity Breakdown\n\n")
        severity_map = {1: 'Fatal', 2: 'Severe Injury', 3: 'Other Visible Injury',
                       4: 'Complaint of Pain', 0: 'Property Damage Only'}
        severity_counts = df['COLLISION_SEVERITY'].value_counts().sort_index()
        for sev, count in severity_counts.items():
            sev_name = severity_map.get(sev, f'Unknown ({sev})')
            pct = (count / len(df)) * 100
            f.write(f"- **{sev_name}**: {count:,} ({pct:.1f}%)\n")

        f.write("\n## Top 10 Crash Locations\n\n")
        top_roads = df['PRIMARY_RD'].value_counts().head(10)
        for i, (road, count) in enumerate(top_roads.items(), 1):
            f.write(f"{i}. **{road}**: {count:,} crashes\n")

        f.write("\n---\n\n")
        f.write("*See outputs/visualizations/crash_analysis.png for visual analysis*\n")

    print(f"✓ Saved summary report: {output_path}")

def main():
    """Main analysis workflow"""
    print("\n" + "="*60)
    print("CRASH DATA ANALYSIS - TIMS (UC Berkeley)")
    print("="*60)

    # Load data
    df = load_crash_data()

    # Run analyses
    basic_info(df)
    severity_analysis(df)
    crash_type_analysis(df)
    environmental_conditions(df)
    temporal_analysis(df)
    location_analysis(df)

    # Create visualizations
    create_visualizations(df)

    # Export summary
    export_summary(df)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  - outputs/visualizations/crash_analysis.png")
    print("  - docs/CRASH_DATA_SUMMARY.md")
    print("\nNext step: Create interactive crash map")
    print("  Run: python scripts/create_crash_map.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
