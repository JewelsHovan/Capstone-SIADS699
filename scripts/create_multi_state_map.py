"""
Create a multi-state comparison map (California + New York)
"""

import folium
from folium import plugins
import json


def load_state_data(state_file, state_name):
    """Load work zone data for a state"""
    with open(state_file, 'r') as f:
        data = json.load(f)

    features = data.get('features', [])
    work_zones = []

    for feature in features:
        try:
            # Get geometry
            geom = feature.get('geometry', {})
            geom_type = geom.get('type')
            coords = geom.get('coordinates', [])

            if not coords:
                continue

            # Get coordinates
            if geom_type == 'Point':
                lat, lon = coords[1], coords[0]
            elif geom_type == 'MultiPoint':
                lat, lon = coords[0][1], coords[0][0]
            elif geom_type == 'LineString':
                mid_idx = len(coords) // 2
                lat, lon = coords[mid_idx][1], coords[mid_idx][0]
            else:
                continue

            # Get properties
            props = feature.get('properties', {})
            core = props.get('core_details', {})

            work_zone = {
                'state': state_name,
                'lat': lat,
                'lon': lon,
                'road_name': ', '.join(core.get('road_names', ['Unknown'])),
                'direction': core.get('direction', 'unknown'),
                'description': core.get('description', '')[:200],
                'vehicle_impact': props.get('vehicle_impact', 'unknown'),
                'workers_present': props.get('worker_presence', {}).get('are_workers_present', False),
                'start_date': props.get('start_date', '')[:10],
                'end_date': props.get('end_date', '')[:10]
            }

            work_zones.append(work_zone)

        except Exception as e:
            continue

    return work_zones


def create_multi_state_map():
    """Create map comparing California and New York work zones"""

    print("=" * 70)
    print("CREATING MULTI-STATE WORK ZONE COMPARISON MAP")
    print("=" * 70)

    # Load data for both states
    print("\nLoading California data...")
    ca_zones = load_state_data('ca_wzdx_feed.json', 'California')
    print(f"  Loaded {len(ca_zones)} California work zones")

    print("Loading New York data...")
    ny_zones = load_state_data('ny_wzdx_feed.json', 'New York')
    print(f"  Loaded {len(ny_zones)} New York work zones")

    # Create base map - centered on USA
    m = folium.Map(
        location=[39.8, -98.6],
        zoom_start=4,
        tiles='OpenStreetMap'
    )

    # Color scheme by state
    state_colors = {
        'California': 'blue',
        'New York': 'red'
    }

    # Create feature groups for each state
    ca_group = folium.FeatureGroup(name='California Work Zones', show=True)
    ny_group = folium.FeatureGroup(name='New York Work Zones', show=True)

    # Statistics
    stats = {
        'California': {'total': len(ca_zones), 'workers': 0, 'closed': 0},
        'New York': {'total': len(ny_zones), 'workers': 0, 'closed': 0}
    }

    print("\nCreating California markers...")
    for wz in ca_zones:
        if wz['workers_present']:
            stats['California']['workers'] += 1
        if 'closed' in wz['vehicle_impact']:
            stats['California']['closed'] += 1

        # Determine icon based on severity
        if wz['workers_present']:
            icon = folium.Icon(color='blue', icon='user', prefix='glyphicon')
        elif 'all-lanes-closed' in wz['vehicle_impact']:
            icon = folium.Icon(color='blue', icon='road', prefix='glyphicon')
        else:
            icon = folium.Icon(color='blue', icon='info-sign', prefix='glyphicon')

        popup_html = f"""
        <div style="width: 300px">
            <h4 style="margin: 0; color: blue">
                <b>California: {wz['road_name']}</b>
            </h4>
            <hr style="margin: 5px 0">
            <p style="margin: 5px 0">
                <b>Direction:</b> {wz['direction']}<br>
                <b>Impact:</b> {wz['vehicle_impact'].replace('-', ' ').title()}<br>
                {'<b style="color: red">⚠️ Workers Present</b><br>' if wz['workers_present'] else ''}
                <b>Start:</b> {wz['start_date']}<br>
                <b>End:</b> {wz['end_date']}
            </p>
            <p style="margin: 5px 0; font-size: 11px">
                {wz['description']}...
            </p>
        </div>
        """

        folium.Marker(
            location=[wz['lat'], wz['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"CA: {wz['road_name']} - {wz['vehicle_impact']}",
            icon=icon
        ).add_to(ca_group)

    print("Creating New York markers...")
    for wz in ny_zones:
        if wz['workers_present']:
            stats['New York']['workers'] += 1
        if 'closed' in wz['vehicle_impact']:
            stats['New York']['closed'] += 1

        # Determine icon based on severity
        if wz['workers_present']:
            icon = folium.Icon(color='red', icon='user', prefix='glyphicon')
        elif 'all-lanes-closed' in wz['vehicle_impact']:
            icon = folium.Icon(color='red', icon='road', prefix='glyphicon')
        else:
            icon = folium.Icon(color='red', icon='info-sign', prefix='glyphicon')

        popup_html = f"""
        <div style="width: 300px">
            <h4 style="margin: 0; color: red">
                <b>New York: {wz['road_name']}</b>
            </h4>
            <hr style="margin: 5px 0">
            <p style="margin: 5px 0">
                <b>Direction:</b> {wz['direction']}<br>
                <b>Impact:</b> {wz['vehicle_impact'].replace('-', ' ').title()}<br>
                {'<b style="color: red">⚠️ Workers Present</b><br>' if wz['workers_present'] else ''}
                <b>Start:</b> {wz['start_date']}<br>
                <b>End:</b> {wz['end_date']}
            </p>
            <p style="margin: 5px 0; font-size: 11px">
                {wz['description']}...
            </p>
        </div>
        """

        folium.Marker(
            location=[wz['lat'], wz['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"NY: {wz['road_name']} - {wz['vehicle_impact']}",
            icon=icon
        ).add_to(ny_group)

    # Add feature groups to map
    ca_group.add_to(m)
    ny_group.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Add legend
    legend_html = f"""
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 280px; height: auto;
                background-color: white; z-index: 9999; font-size: 14px;
                border: 2px solid grey; border-radius: 5px; padding: 10px">
        <h4 style="margin: 0 0 10px 0">Multi-State Comparison</h4>
        <hr style="margin: 5px 0">

        <p style="margin: 5px 0; color: blue; font-weight: bold">
            <i class="glyphicon glyphicon-map-marker"></i> California
        </p>
        <p style="margin: 5px 0; padding-left: 20px">
            Total: {stats['California']['total']}<br>
            Lane closures: {stats['California']['closed']}<br>
            Workers present: {stats['California']['workers']}
        </p>

        <hr style="margin: 5px 0">

        <p style="margin: 5px 0; color: red; font-weight: bold">
            <i class="glyphicon glyphicon-map-marker"></i> New York
        </p>
        <p style="margin: 5px 0; padding-left: 20px">
            Total: {stats['New York']['total']}<br>
            Lane closures: {stats['New York']['closed']}<br>
            Workers present: {stats['New York']['workers']}
        </p>

        <hr style="margin: 5px 0">
        <p style="margin: 5px 0; font-size: 12px">
            <b>Combined Total: {stats['California']['total'] + stats['New York']['total']} work zones</b>
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save the map
    output_file = 'multi_state_comparison_map.html'
    m.save(output_file)

    print("\n" + "=" * 70)
    print("MULTI-STATE MAP CREATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nMap saved to: {output_file}")
    print("\nComparison Statistics:")
    print("\nCalifornia:")
    print(f"  Total work zones: {stats['California']['total']}")
    print(f"  Lane closures: {stats['California']['closed']}")
    print(f"  Workers present: {stats['California']['workers']}")
    print("\nNew York:")
    print(f"  Total work zones: {stats['New York']['total']}")
    print(f"  Lane closures: {stats['New York']['closed']}")
    print(f"  Workers present: {stats['New York']['workers']}")
    print(f"\nCombined Total: {stats['California']['total'] + stats['New York']['total']} work zones")

    print(f"\nOpen '{output_file}' in your browser to view the comparison map!")
    print("\nFeatures:")
    print("  ✓ Blue markers = California")
    print("  ✓ Red markers = New York")
    print("  ✓ Toggle states on/off with layer control")
    print("  ✓ Compare geographic distribution")
    print("  ✓ Click markers for details")


if __name__ == "__main__":
    create_multi_state_map()
