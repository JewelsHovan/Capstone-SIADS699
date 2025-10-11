"""
Interactive Crash Map Generator
Creates an interactive Folium map showing crash locations from TIMS data
Color-coded by severity with detailed popup information
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

def load_crash_data(csv_path='data/Crashes.csv'):
    """Load crash data and filter to records with coordinates"""
    # Handle relative paths
    if not os.path.isabs(csv_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, csv_path)

    print("Loading crash data...")
    df = pd.read_csv(csv_path, low_memory=False)

    # Filter to records with valid coordinates
    df = df[df[['LATITUDE', 'LONGITUDE']].notna().all(axis=1)]

    print(f"✓ Loaded {len(df):,} crashes with coordinates")
    return df

def get_severity_color(severity):
    """Map severity level to marker color"""
    severity_colors = {
        1: 'darkred',      # Fatal
        2: 'red',          # Severe Injury
        3: 'orange',       # Other Visible Injury
        4: 'lightblue',    # Complaint of Pain
        0: 'lightgray'     # Property Damage Only
    }
    return severity_colors.get(severity, 'gray')

def get_severity_name(severity):
    """Map severity level to human-readable name"""
    severity_names = {
        1: 'Fatal',
        2: 'Severe Injury',
        3: 'Visible Injury',
        4: 'Complaint of Pain',
        0: 'Property Damage Only'
    }
    return severity_names.get(severity, f'Unknown ({severity})')

def create_popup_html(crash):
    """Create HTML popup content for crash marker"""
    severity_name = get_severity_name(crash['COLLISION_SEVERITY'])

    # Format date
    date = crash.get('COLLISION_DATE', 'Unknown')
    time = str(crash.get('COLLISION_TIME', '')).strip() if pd.notna(crash.get('COLLISION_TIME')) else 'Unknown'

    # Location info
    road = crash.get('PRIMARY_RD', 'Unknown')
    secondary = crash.get('SECONDARY_RD', '')
    location = road
    if pd.notna(secondary) and secondary not in ['', '-', 'nan']:
        location = f"{road} & {secondary}"

    city = crash.get('CITY', 'Unknown')

    # Casualties
    killed = int(crash.get('NUMBER_KILLED', 0)) if pd.notna(crash.get('NUMBER_KILLED')) else 0
    injured = int(crash.get('NUMBER_INJURED', 0)) if pd.notna(crash.get('NUMBER_INJURED')) else 0

    # Special flags
    flags = []
    if crash.get('ALCOHOL_INVOLVED') == 'Y':
        flags.append('🍺 Alcohol')
    if crash.get('HIT_AND_RUN') in ['F', 'M']:
        flags.append('🚨 Hit-and-Run')
    if pd.notna(crash.get('PEDESTRIAN_ACCIDENT')) and crash.get('PEDESTRIAN_ACCIDENT') != 0:
        flags.append('🚶 Pedestrian')
    if pd.notna(crash.get('BICYCLE_ACCIDENT')) and crash.get('BICYCLE_ACCIDENT') != 0:
        flags.append('🚲 Bicycle')

    # Build HTML
    html = f"""
    <div style='min-width: 250px; font-family: Arial, sans-serif;'>
        <h4 style='margin: 0 0 10px 0; color: #333;'>{severity_name} Crash</h4>
        <b>Location:</b> {location}<br>
        <b>City:</b> {city}<br>
        <b>Date:</b> {date} at {time}<br>
        <hr style='margin: 8px 0;'>
        <b>Casualties:</b><br>
        • Killed: {killed}<br>
        • Injured: {injured}<br>
    """

    if flags:
        html += f"<hr style='margin: 8px 0;'><b>Special Factors:</b><br>{'<br>'.join(flags)}<br>"

    html += "</div>"

    return html

def create_crash_map(df, use_clustering=True, output_path='outputs/maps/crash_map.html'):
    """Create interactive Folium map of crashes"""

    # Handle output path
    if not os.path.isabs(output_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_path = os.path.join(project_root, output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("\nCreating interactive crash map...")

    # Calculate center point (median lat/lon)
    center_lat = df['LATITUDE'].median()
    center_lon = df['LONGITUDE'].median()

    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )

    # Create feature groups for each severity level
    severity_groups = {}
    for severity in sorted(df['COLLISION_SEVERITY'].unique()):
        severity_name = get_severity_name(severity)
        severity_groups[severity] = folium.FeatureGroup(name=severity_name)

    # Add markers to appropriate groups
    print(f"Adding {len(df):,} crash markers...")

    for idx, crash in df.iterrows():
        severity = crash['COLLISION_SEVERITY']
        color = get_severity_color(severity)

        # Create marker
        marker = folium.CircleMarker(
            location=[crash['LATITUDE'], crash['LONGITUDE']],
            radius=6,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            popup=folium.Popup(create_popup_html(crash), max_width=300)
        )

        # Add to appropriate severity group
        if severity in severity_groups:
            marker.add_to(severity_groups[severity])

    # Add all groups to map
    for group in severity_groups.values():
        group.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Add legend
    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 220px; height: auto;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px">
        <h4 style="margin-top:0;">Crash Severity Legend</h4>
        <p style="margin: 5px 0;"><span style="background-color: darkred; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Fatal</p>
        <p style="margin: 5px 0;"><span style="background-color: red; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Severe Injury</p>
        <p style="margin: 5px 0;"><span style="background-color: orange; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Visible Injury</p>
        <p style="margin: 5px 0;"><span style="background-color: lightblue; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Complaint of Pain</p>
        <p style="margin: 5px 0;"><span style="background-color: lightgray; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Property Only</p>
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0; font-size: 12px;"><b>Total Crashes:</b> ''' + f'{len(df):,}' + '''</p>
        <p style="margin: 5px 0; font-size: 12px;"><b>Fatalities:</b> ''' + f'{int(df["NUMBER_KILLED"].sum())}' + '''</p>
        <p style="margin: 5px 0; font-size: 12px;"><b>Injuries:</b> ''' + f'{int(df["NUMBER_INJURED"].sum()):,}' + '''</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save map
    m.save(output_path)
    print(f"✓ Saved map to: {output_path}")

    return m

def create_severity_comparison_maps(df, output_dir='outputs/maps'):
    """Create separate maps for fatal vs injury crashes"""

    # Handle output path
    if not os.path.isabs(output_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    print("\nCreating fatal crashes map...")

    # Fatal crashes only
    fatal = df[df['COLLISION_SEVERITY'] == 1]

    if len(fatal) > 0:
        center_lat = df['LATITUDE'].median()
        center_lon = df['LONGITUDE'].median()

        m_fatal = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )

        for idx, crash in fatal.iterrows():
            folium.CircleMarker(
                location=[crash['LATITUDE'], crash['LONGITUDE']],
                radius=8,
                color='darkred',
                fill=True,
                fillColor='darkred',
                fillOpacity=0.8,
                popup=folium.Popup(create_popup_html(crash), max_width=300)
            ).add_to(m_fatal)

        fatal_path = os.path.join(output_dir, 'fatal_crashes_map.html')
        m_fatal.save(fatal_path)
        print(f"✓ Saved fatal crashes map ({len(fatal)} crashes): {fatal_path}")

def main():
    """Main workflow"""
    print("\n" + "="*60)
    print("INTERACTIVE CRASH MAP GENERATOR")
    print("="*60)

    # Load data
    df = load_crash_data()

    # Create main map
    create_crash_map(df)

    # Create fatal crashes map
    create_severity_comparison_maps(df)

    print("\n" + "="*60)
    print("MAP GENERATION COMPLETE!")
    print("="*60)
    print("\nGenerated maps:")
    print("  - outputs/maps/crash_map.html (all crashes)")
    print("  - outputs/maps/fatal_crashes_map.html (fatal only)")
    print("\nOpen in browser to explore crash locations!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
