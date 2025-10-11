"""
Crash + Work Zone Overlay Map
Creates an interactive map showing both crashes and work zones
to identify potential safety correlations
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os
import json

def load_crash_data(csv_path='data/Crashes.csv'):
    """Load crash data with coordinates"""
    if not os.path.isabs(csv_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, csv_path)

    print("Loading crash data...")
    df = pd.read_csv(csv_path, low_memory=False)
    df = df[df[['LATITUDE', 'LONGITUDE']].notna().all(axis=1)]

    # Filter to 2023 crashes only (to match work zone data timeframe)
    df = df[df['ACCIDENT_YEAR'] == 2023]

    print(f"✓ Loaded {len(df):,} crashes from 2023 with coordinates")
    return df

def load_work_zone_data(json_path='data/raw/ca_wzdx_feed.json'):
    """Load California work zone data from JSON feed"""
    if not os.path.isabs(json_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        json_path = os.path.join(project_root, json_path)

    print("Loading work zone data...")

    with open(json_path, 'r') as f:
        data = json.load(f)

    work_zones = []
    for feature in data.get('features', []):
        props = feature.get('properties', {})
        geom = feature.get('geometry', {})

        # Extract center point from geometry
        coords = geom.get('coordinates', [])
        if coords:
            # If LineString, get middle point
            if geom.get('type') == 'LineString':
                mid_idx = len(coords) // 2
                lon, lat = coords[mid_idx]
            # If MultiPoint, get first point
            elif geom.get('type') == 'MultiPoint':
                lon, lat = coords[0]
            else:
                continue

            work_zones.append({
                'road_name': ', '.join(props.get('core_details', {}).get('road_names', [])),
                'direction': props.get('core_details', {}).get('direction', 'unknown'),
                'vehicle_impact': props.get('vehicle_impact', 'unknown'),
                'latitude': lat,
                'longitude': lon
            })

    df = pd.DataFrame(work_zones)
    print(f"✓ Loaded {len(df):,} work zones with coordinates")
    return df

def get_crash_severity_color(severity):
    """Crash severity colors"""
    colors = {
        1: 'darkred',      # Fatal
        2: 'red',          # Severe Injury
        3: 'orange',       # Visible Injury
        4: 'lightblue'     # Complaint of Pain
    }
    return colors.get(severity, 'gray')

def get_workzone_impact_color(impact):
    """Work zone impact colors"""
    if pd.isna(impact):
        return 'blue'
    impact = str(impact).lower()
    if 'all-lanes-closed' in impact:
        return 'purple'
    elif 'some-lanes-closed' in impact:
        return 'darkblue'
    else:
        return 'blue'

def create_crash_popup(crash):
    """Create popup for crash marker"""
    severity_map = {1: 'Fatal', 2: 'Severe Injury', 3: 'Visible Injury', 4: 'Complaint of Pain'}
    severity_name = severity_map.get(crash['COLLISION_SEVERITY'], 'Unknown')

    road = crash.get('PRIMARY_RD', 'Unknown')
    date = crash.get('COLLISION_DATE', 'Unknown')

    html = f"""
    <div style='min-width: 200px;'>
        <h4 style='margin: 0 0 8px 0; color: #d9534f;'>Crash: {severity_name}</h4>
        <b>Location:</b> {road}<br>
        <b>Date:</b> {date}<br>
        <b>Killed:</b> {int(crash.get('NUMBER_KILLED', 0))}<br>
        <b>Injured:</b> {int(crash.get('NUMBER_INJURED', 0))}
    </div>
    """
    return html

def create_workzone_popup(wz):
    """Create popup for work zone marker"""
    road = wz.get('road_name', 'Unknown')
    impact = wz.get('vehicle_impact', 'Unknown')

    html = f"""
    <div style='min-width: 200px;'>
        <h4 style='margin: 0 0 8px 0; color: #5bc0de;'>Work Zone</h4>
        <b>Road:</b> {road}<br>
        <b>Impact:</b> {impact}<br>
        <b>Direction:</b> {wz.get('direction', 'Unknown')}
    </div>
    """
    return html

def create_overlay_map(crashes_df, workzones_df, output_path='outputs/maps/crash_workzone_overlay.html'):
    """Create overlay map with both crashes and work zones"""

    # Handle output path
    if not os.path.isabs(output_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_path = os.path.join(project_root, output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("\nCreating overlay map...")

    # Calculate center (use median of both datasets)
    all_lats = list(crashes_df['LATITUDE']) + list(workzones_df['latitude'])
    all_lons = list(crashes_df['LONGITUDE']) + list(workzones_df['longitude'])
    center_lat = pd.Series(all_lats).median()
    center_lon = pd.Series(all_lons).median()

    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )

    # Create feature groups
    fatal_crashes = folium.FeatureGroup(name='🔴 Fatal Crashes')
    severe_crashes = folium.FeatureGroup(name='🟠 Severe Injury Crashes')
    other_crashes = folium.FeatureGroup(name='🔵 Other Crashes (sample)')
    work_zones = folium.FeatureGroup(name='🟣 Work Zones')

    # Add work zone markers
    print(f"Adding {len(workzones_df):,} work zone markers...")
    for idx, wz in workzones_df.iterrows():
        color = get_workzone_impact_color(wz.get('vehicle_impact'))

        folium.CircleMarker(
            location=[wz['latitude'], wz['longitude']],
            radius=7,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.4,
            weight=2,
            popup=folium.Popup(create_workzone_popup(wz), max_width=250)
        ).add_to(work_zones)

    # Add crash markers (sample other crashes to avoid overload)
    print(f"Adding crash markers...")

    # All fatal crashes
    fatal_df = crashes_df[crashes_df['COLLISION_SEVERITY'] == 1]
    for idx, crash in fatal_df.iterrows():
        folium.CircleMarker(
            location=[crash['LATITUDE'], crash['LONGITUDE']],
            radius=8,
            color='darkred',
            fill=True,
            fillColor='darkred',
            fillOpacity=0.8,
            popup=folium.Popup(create_crash_popup(crash), max_width=250)
        ).add_to(fatal_crashes)

    # All severe injury crashes
    severe_df = crashes_df[crashes_df['COLLISION_SEVERITY'] == 2]
    for idx, crash in severe_df.iterrows():
        folium.CircleMarker(
            location=[crash['LATITUDE'], crash['LONGITUDE']],
            radius=6,
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.7,
            popup=folium.Popup(create_crash_popup(crash), max_width=250)
        ).add_to(severe_crashes)

    # Sample of other crashes (10% to keep map responsive)
    other_df = crashes_df[crashes_df['COLLISION_SEVERITY'].isin([3, 4])].sample(
        n=min(1000, len(crashes_df[crashes_df['COLLISION_SEVERITY'].isin([3, 4])])),
        random_state=42
    )
    for idx, crash in other_df.iterrows():
        color = get_crash_severity_color(crash['COLLISION_SEVERITY'])
        folium.CircleMarker(
            location=[crash['LATITUDE'], crash['LONGITUDE']],
            radius=4,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.5,
            popup=folium.Popup(create_crash_popup(crash), max_width=250)
        ).add_to(other_crashes)

    # Add all groups to map
    work_zones.add_to(m)
    fatal_crashes.add_to(m)
    severe_crashes.add_to(m)
    other_crashes.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Add legend
    legend_html = f'''
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 250px; height: auto;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:13px; padding: 12px">
        <h4 style="margin-top:0;">Crash + Work Zone Overlay</h4>

        <p style="margin: 8px 0; font-weight: bold;">Work Zones</p>
        <p style="margin: 3px 0;"><span style="background-color: purple; width: 18px; height: 18px; display: inline-block; border-radius: 50%; opacity: 0.6;"></span> All Lanes Closed</p>
        <p style="margin: 3px 0;"><span style="background-color: darkblue; width: 18px; height: 18px; display: inline-block; border-radius: 50%; opacity: 0.6;"></span> Some Lanes Closed</p>
        <p style="margin: 3px 0;"><span style="background-color: blue; width: 18px; height: 18px; display: inline-block; border-radius: 50%; opacity: 0.6;"></span> Other Impact</p>

        <hr style="margin: 10px 0;">

        <p style="margin: 8px 0; font-weight: bold;">Crashes (2023)</p>
        <p style="margin: 3px 0;"><span style="background-color: darkred; width: 18px; height: 18px; display: inline-block; border-radius: 50%;"></span> Fatal</p>
        <p style="margin: 3px 0;"><span style="background-color: red; width: 18px; height: 18px; display: inline-block; border-radius: 50%;"></span> Severe Injury</p>
        <p style="margin: 3px 0;"><span style="background-color: orange; width: 18px; height: 18px; display: inline-block; border-radius: 50%;"></span> Visible Injury</p>

        <hr style="margin: 10px 0;">

        <p style="margin: 3px 0; font-size: 12px;"><b>Work Zones:</b> {len(workzones_df):,}</p>
        <p style="margin: 3px 0; font-size: 12px;"><b>Fatal Crashes:</b> {len(fatal_df):,}</p>
        <p style="margin: 3px 0; font-size: 12px;"><b>Severe Crashes:</b> {len(severe_df):,}</p>
        <p style="margin: 3px 0; font-size: 12px;"><b>Total Crashes:</b> {len(crashes_df):,}</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save map
    m.save(output_path)
    print(f"✓ Saved overlay map to: {output_path}")

    return m

def generate_overlap_analysis(crashes_df, workzones_df):
    """Analyze crashes near work zones"""
    print("\n" + "="*60)
    print("CRASH-WORKZONE PROXIMITY ANALYSIS")
    print("="*60)

    # Simple distance calculation (approximate - for detailed analysis use geopy)
    print("\nNote: This is a basic proximity analysis.")
    print("For detailed spatial analysis, use GIS tools or geopy library.")

    # Count crashes by severity
    print(f"\nCrashes in dataset (2023):")
    print(f"  Fatal: {len(crashes_df[crashes_df['COLLISION_SEVERITY'] == 1]):,}")
    print(f"  Severe Injury: {len(crashes_df[crashes_df['COLLISION_SEVERITY'] == 2]):,}")
    print(f"  Visible Injury: {len(crashes_df[crashes_df['COLLISION_SEVERITY'] == 3]):,}")
    print(f"  Other: {len(crashes_df[crashes_df['COLLISION_SEVERITY'] == 4]):,}")

    print(f"\nWork Zones in dataset:")
    print(f"  Total: {len(workzones_df):,}")

    # Top crash roads vs top work zone roads
    print(f"\nTop 5 Crash Roads:")
    crash_roads = crashes_df['PRIMARY_RD'].value_counts().head(5)
    for road, count in crash_roads.items():
        print(f"  {road}: {count:,} crashes")

    print(f"\nTop 5 Work Zone Roads:")
    wz_roads = workzones_df['road_name'].value_counts().head(5)
    for road, count in wz_roads.items():
        print(f"  {road}: {count:,} work zones")

def main():
    """Main workflow"""
    print("\n" + "="*60)
    print("CRASH + WORK ZONE OVERLAY MAP GENERATOR")
    print("="*60)

    # Load data
    crashes = load_crash_data()
    workzones = load_work_zone_data()

    # Create overlay map
    create_overlay_map(crashes, workzones)

    # Generate analysis
    generate_overlap_analysis(crashes, workzones)

    print("\n" + "="*60)
    print("OVERLAY MAP GENERATION COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  - outputs/maps/crash_workzone_overlay.html")
    print("\nUse this map to:")
    print("  • Identify crashes near work zones")
    print("  • Compare crash patterns in work zone areas")
    print("  • Explore potential safety correlations")
    print("\nOpen in browser to explore!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
