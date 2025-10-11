"""
Texas Work Zone Interactive Map
Creates Folium map showing TxDOT work zones
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

def load_texas_data(csv_path='data/processed/texas_work_zones_analysis.csv'):
    """Load processed Texas work zone data"""
    if not os.path.isabs(csv_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, csv_path)

    print("Loading Texas work zone data...")
    df = pd.read_csv(csv_path, low_memory=False)

    # Filter to records with coordinates
    df = df[df[['latitude', 'longitude']].notna().all(axis=1)]

    print(f"✓ Loaded {len(df):,} work zones with coordinates")
    return df

def get_impact_color(impact):
    """Map vehicle impact to marker color"""
    if pd.isna(impact):
        return 'gray'

    impact = str(impact).lower()
    if 'all-lanes-closed' in impact:
        return 'red'
    elif 'some-lanes-closed' in impact:
        return 'orange'
    elif 'all-lanes-open' in impact:
        return 'blue'
    else:
        return 'gray'

def create_popup_html(wz):
    """Create HTML popup for work zone marker"""
    road = wz.get('road_name', 'Unknown')
    direction = wz.get('direction', 'Unknown')
    impact = wz.get('vehicle_impact', 'Unknown')
    description = wz.get('description', '')

    # Truncate long descriptions
    if len(str(description)) > 200:
        description = str(description)[:200] + '...'

    # Region
    region = wz.get('subidentifier', 'Unknown')

    # Dates
    start = wz.get('start_date', 'Unknown')
    end = wz.get('end_date', 'Unknown')

    html = f"""
    <div style='min-width: 250px; font-family: Arial, sans-serif;'>
        <h4 style='margin: 0 0 10px 0; color: #333;'>TxDOT Work Zone</h4>
        <b>Road:</b> {road}<br>
        <b>Direction:</b> {direction}<br>
        <b>Region:</b> {region}<br>
        <hr style='margin: 8px 0;'>
        <b>Impact:</b> {impact}<br>
        <b>Start:</b> {start}<br>
        <b>End:</b> {end}<br>
    """

    if description and description != 'nan':
        html += f"<hr style='margin: 8px 0;'><b>Details:</b><br>{description}<br>"

    html += "</div>"
    return html

def create_texas_map(df, output_path='outputs/maps/texas_workzones_map.html'):
    """Create interactive map of Texas work zones"""

    # Handle output path
    if not os.path.isabs(output_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_path = os.path.join(project_root, output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("\nCreating Texas work zone map...")

    # Calculate center (median lat/lon)
    center_lat = df['latitude'].median()
    center_lon = df['longitude'].median()

    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles='OpenStreetMap'
    )

    # Create feature groups for each impact type
    all_lanes_closed = folium.FeatureGroup(name='🔴 All Lanes Closed')
    some_lanes_closed = folium.FeatureGroup(name='🟠 Some Lanes Closed')
    all_lanes_open = folium.FeatureGroup(name='🔵 All Lanes Open')
    unknown_impact = folium.FeatureGroup(name='⚪ Unknown Impact')

    # Add markers
    print(f"Adding {len(df):,} work zone markers...")

    for idx, wz in df.iterrows():
        impact = str(wz.get('vehicle_impact', '')).lower()
        color = get_impact_color(wz.get('vehicle_impact'))

        marker = folium.CircleMarker(
            location=[wz['latitude'], wz['longitude']],
            radius=6,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6,
            popup=folium.Popup(create_popup_html(wz), max_width=300)
        )

        # Add to appropriate group
        if 'all-lanes-closed' in impact:
            marker.add_to(all_lanes_closed)
        elif 'some-lanes-closed' in impact:
            marker.add_to(some_lanes_closed)
        elif 'all-lanes-open' in impact:
            marker.add_to(all_lanes_open)
        else:
            marker.add_to(unknown_impact)

    # Add all groups to map
    all_lanes_closed.add_to(m)
    some_lanes_closed.add_to(m)
    all_lanes_open.add_to(m)
    unknown_impact.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Count by impact
    impact_counts = df['vehicle_impact'].value_counts()

    # Add legend
    legend_html = f'''
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 240px; height: auto;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:13px; padding: 12px">
        <h4 style="margin-top:0;">Texas Work Zones</h4>
        <p style="margin: 5px 0;"><span style="background-color: red; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> All Lanes Closed</p>
        <p style="margin: 5px 0;"><span style="background-color: orange; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Some Lanes Closed</p>
        <p style="margin: 5px 0;"><span style="background-color: blue; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> All Lanes Open</p>
        <p style="margin: 5px 0;"><span style="background-color: gray; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> Unknown</p>
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0; font-size: 12px;"><b>Total Zones:</b> {len(df):,}</p>
        <p style="margin: 5px 0; font-size: 12px;"><b>All Closed:</b> {impact_counts.get('all-lanes-closed', 0):,}</p>
        <p style="margin: 5px 0; font-size: 12px;"><b>Some Closed:</b> {impact_counts.get('some-lanes-closed', 0):,}</p>
        <p style="margin: 5px 0; font-size: 12px;"><b>All Open:</b> {impact_counts.get('all-lanes-open', 0):,}</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save map
    m.save(output_path)
    print(f"✓ Saved map to: {output_path}")

    return m

def main():
    """Main workflow"""
    print("\n" + "="*60)
    print("TEXAS WORK ZONE MAP GENERATOR")
    print("="*60)

    # Load data
    df = load_texas_data()

    # Create map
    create_texas_map(df)

    print("\n" + "="*60)
    print("MAP GENERATION COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  - outputs/maps/texas_workzones_map.html")
    print("\nOpen in browser to explore Texas work zones!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
