"""
Create an interactive map of California work zones
"""

import folium
from folium import plugins
import json
from datetime import datetime


def create_california_map():
    """Create interactive map of California work zones"""

    print("=" * 70)
    print("CREATING CALIFORNIA WORK ZONE MAP")
    print("=" * 70)

    # Load the California feed
    print("\nLoading California WZDx data...")
    with open('ca_wzdx_feed.json', 'r') as f:
        data = json.load(f)

    features = data.get('features', [])
    print(f"Found {len(features)} work zones")

    # Create base map centered on California
    # Using the center from our analysis: (37.4290, -121.9717)
    m = folium.Map(
        location=[37.5, -122.0],
        zoom_start=9,
        tiles='OpenStreetMap'
    )

    # Color scheme based on vehicle impact
    impact_colors = {
        'all-lanes-closed': 'red',
        'some-lanes-closed': 'orange',
        'some-lanes-closed-merge-right': 'orange',
        'some-lanes-closed-merge-left': 'orange',
        'some-lanes-closed-split': 'orange',
        'all-lanes-open-shift-right': 'blue',
        'all-lanes-open-shift-left': 'blue',
        'all-lanes-open': 'green',
        'unknown': 'gray'
    }

    # Icons based on vehicle impact
    impact_icons = {
        'all-lanes-closed': 'road',
        'some-lanes-closed': 'exclamation-triangle',
        'all-lanes-open': 'info-sign',
        'unknown': 'question-sign'
    }

    # Create feature groups for different layers
    all_closures = folium.FeatureGroup(name='All Lane Closures', show=True)
    some_closures = folium.FeatureGroup(name='Some Lane Closures', show=True)
    lane_shifts = folium.FeatureGroup(name='Lane Shifts', show=True)
    open_roads = folium.FeatureGroup(name='All Lanes Open', show=False)
    unknown = folium.FeatureGroup(name='Unknown Impact', show=False)

    # Track statistics
    stats = {
        'total': 0,
        'all_closed': 0,
        'some_closed': 0,
        'shifts': 0,
        'open': 0,
        'workers_present': 0
    }

    print("\nProcessing work zones...")

    for feature in features:
        try:
            # Get geometry
            geom = feature.get('geometry', {})
            geom_type = geom.get('type')
            coords = geom.get('coordinates', [])

            if not coords:
                continue

            # Get coordinates (handle both Point and LineString)
            if geom_type == 'Point':
                lat, lon = coords[1], coords[0]
            elif geom_type == 'MultiPoint':
                lat, lon = coords[0][1], coords[0][0]
            elif geom_type == 'LineString':
                # Use middle point of line
                mid_idx = len(coords) // 2
                lat, lon = coords[mid_idx][1], coords[mid_idx][0]
            else:
                continue

            # Get properties
            props = feature.get('properties', {})
            core = props.get('core_details', {})

            road_names = core.get('road_names', ['Unknown Road'])
            road_name = ', '.join(road_names) if road_names else 'Unknown Road'
            direction = core.get('direction', 'unknown')
            description = core.get('description', 'No description available')
            vehicle_impact = props.get('vehicle_impact', 'unknown')

            # Worker presence
            worker_presence = props.get('worker_presence', {})
            workers_present = worker_presence.get('are_workers_present', False)

            # Dates
            start_date = props.get('start_date', 'Unknown')
            end_date = props.get('end_date', 'Unknown')

            # Update stats
            stats['total'] += 1
            if 'all-lanes-closed' in vehicle_impact:
                stats['all_closed'] += 1
            elif 'some-lanes-closed' in vehicle_impact:
                stats['some_closed'] += 1
            elif 'shift' in vehicle_impact:
                stats['shifts'] += 1
            elif 'all-lanes-open' in vehicle_impact:
                stats['open'] += 1

            if workers_present:
                stats['workers_present'] += 1

            # Get color and icon
            color = impact_colors.get(vehicle_impact, 'gray')
            icon_name = impact_icons.get(
                vehicle_impact,
                impact_icons.get(vehicle_impact.split('-')[0], 'question-sign')
            )

            # Create popup content
            popup_html = f"""
            <div style="width: 300px">
                <h4 style="margin: 0 0 10px 0; color: {color}">
                    <b>{road_name}</b>
                </h4>
                <hr style="margin: 5px 0">
                <p style="margin: 5px 0">
                    <b>Direction:</b> {direction}<br>
                    <b>Impact:</b> {vehicle_impact.replace('-', ' ').title()}<br>
                    {'<b style="color: red">⚠️ Workers Present</b><br>' if workers_present else ''}
                    <b>Start:</b> {start_date[:10] if len(start_date) > 10 else start_date}<br>
                    <b>End:</b> {end_date[:10] if len(end_date) > 10 else end_date}
                </p>
                <hr style="margin: 5px 0">
                <p style="margin: 5px 0; font-size: 11px">
                    {description[:200]}{'...' if len(description) > 200 else ''}
                </p>
            </div>
            """

            # Create marker
            marker = folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{road_name} - {vehicle_impact.replace('-', ' ').title()}",
                icon=folium.Icon(color=color, icon=icon_name, prefix='glyphicon')
            )

            # Add to appropriate layer
            if 'all-lanes-closed' in vehicle_impact:
                marker.add_to(all_closures)
            elif 'some-lanes-closed' in vehicle_impact:
                marker.add_to(some_closures)
            elif 'shift' in vehicle_impact:
                marker.add_to(lane_shifts)
            elif 'all-lanes-open' in vehicle_impact:
                marker.add_to(open_roads)
            else:
                marker.add_to(unknown)

        except Exception as e:
            print(f"Warning: Error processing feature: {e}")
            continue

    # Add all feature groups to map
    all_closures.add_to(m)
    some_closures.add_to(m)
    lane_shifts.add_to(m)
    open_roads.add_to(m)
    unknown.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Add a custom legend
    legend_html = f"""
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 250px; height: auto;
                background-color: white; z-index: 9999; font-size: 14px;
                border: 2px solid grey; border-radius: 5px; padding: 10px">
        <h4 style="margin: 0 0 10px 0">California Work Zones</h4>
        <hr style="margin: 5px 0">
        <p style="margin: 5px 0"><b>Total:</b> {stats['total']} work zones</p>
        <p style="margin: 5px 0">
            <i class="glyphicon glyphicon-road" style="color: red"></i>
            All lanes closed: {stats['all_closed']}
        </p>
        <p style="margin: 5px 0">
            <i class="glyphicon glyphicon-exclamation-triangle" style="color: orange"></i>
            Some lanes closed: {stats['some_closed']}
        </p>
        <p style="margin: 5px 0">
            <i class="glyphicon glyphicon-info-sign" style="color: blue"></i>
            Lane shifts: {stats['shifts']}
        </p>
        <p style="margin: 5px 0">
            <i class="glyphicon glyphicon-info-sign" style="color: green"></i>
            All lanes open: {stats['open']}
        </p>
        <hr style="margin: 5px 0">
        <p style="margin: 5px 0; color: red">
            <b>⚠️ Workers present: {stats['workers_present']}</b>
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add marker cluster for better performance with many points
    # Optionally uncomment this if you want clustering
    # marker_cluster = plugins.MarkerCluster().add_to(m)

    # Save the map
    output_file = 'california_work_zones_map.html'
    m.save(output_file)

    print("\n" + "=" * 70)
    print("MAP CREATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nMap saved to: {output_file}")
    print("\nMap Statistics:")
    print(f"  Total work zones: {stats['total']}")
    print(f"  All lanes closed: {stats['all_closed']}")
    print(f"  Some lanes closed: {stats['some_closed']}")
    print(f"  Lane shifts: {stats['shifts']}")
    print(f"  All lanes open: {stats['open']}")
    print(f"  Workers present: {stats['workers_present']}")

    print(f"\nOpen '{output_file}' in your browser to view the interactive map!")
    print("\nFeatures:")
    print("  ✓ Click markers for detailed information")
    print("  ✓ Hover over markers for quick info")
    print("  ✓ Toggle layers on/off using the layer control")
    print("  ✓ Color-coded by impact severity (red=closed, orange=some closed, blue=shift)")
    print("  ✓ Legend shows current statistics")


if __name__ == "__main__":
    create_california_map()
