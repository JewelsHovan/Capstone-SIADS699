"""
WZDx Mapping Module
Core functionality for creating interactive work zone maps with Folium
"""

import folium
from folium import plugins
import pandas as pd
from typing import List, Dict, Optional, Tuple


class WorkZoneMapper:
    """Create interactive maps from WZDx work zone data"""

    # Color scheme based on vehicle impact severity
    IMPACT_COLORS = {
        'all-lanes-closed': 'red',
        'some-lanes-closed': 'orange',
        'some-lanes-closed-merge-right': 'orange',
        'some-lanes-closed-merge-left': 'orange',
        'some-lanes-closed-split': 'orange',
        'all-lanes-open-shift-right': 'blue',
        'all-lanes-open-shift-left': 'blue',
        'all-lanes-open': 'green',
        'unknown': 'gray',
        'alternating-one-way': 'purple'
    }

    # Icon mapping for different impact types
    IMPACT_ICONS = {
        'all-lanes-closed': 'road',
        'some-lanes-closed': 'exclamation-triangle',
        'all-lanes-open': 'info-sign',
        'unknown': 'question-sign'
    }

    def __init__(self, work_zones: List[Dict]):
        """
        Initialize mapper with work zone data

        Args:
            work_zones: List of work zone dictionaries with keys:
                - latitude, longitude (required)
                - road_name, direction, vehicle_impact
                - workers_present, description
                - start_date, end_date
        """
        self.work_zones = work_zones
        self.df = pd.DataFrame(work_zones)
        self.map = None
        self.stats = {}

    def get_color(self, impact: str) -> str:
        """Get marker color for vehicle impact type"""
        return self.IMPACT_COLORS.get(impact, 'gray')

    def get_icon(self, impact: str) -> str:
        """Get marker icon for vehicle impact type"""
        # Check for exact match first
        if impact in self.IMPACT_ICONS:
            return self.IMPACT_ICONS[impact]
        # Then check for partial match
        for key in self.IMPACT_ICONS:
            if key in impact:
                return self.IMPACT_ICONS[key]
        return 'question-sign'

    def get_center(self) -> Tuple[float, float]:
        """Calculate center point of all work zones"""
        center_lat = self.df['latitude'].mean()
        center_lon = self.df['longitude'].mean()
        return (center_lat, center_lon)

    def calculate_stats(self) -> Dict:
        """Calculate statistics for legend"""
        stats = {
            'total': len(self.df),
            'all_closed': 0,
            'some_closed': 0,
            'shifts': 0,
            'open': 0,
            'workers': 0
        }

        for _, row in self.df.iterrows():
            impact = row.get('vehicle_impact', 'unknown')

            if 'all-lanes-closed' in impact:
                stats['all_closed'] += 1
            elif 'some-lanes-closed' in impact:
                stats['some_closed'] += 1
            elif 'shift' in impact:
                stats['shifts'] += 1
            elif 'all-lanes-open' in impact:
                stats['open'] += 1

            if row.get('workers_present', False):
                stats['workers'] += 1

        self.stats = stats
        return stats

    def create_popup_html(self, row: pd.Series) -> str:
        """
        Create HTML for marker popup

        Args:
            row: DataFrame row with work zone data

        Returns:
            HTML string for popup
        """
        color = self.get_color(row.get('vehicle_impact', 'unknown'))
        road_name = row.get('road_name', 'Unknown Road')
        direction = row.get('direction', 'unknown')
        vehicle_impact = row.get('vehicle_impact', 'unknown')
        workers_present = row.get('workers_present', False)
        description = str(row.get('description', 'No description available'))
        start_date = str(row.get('start_date', 'Unknown'))
        end_date = str(row.get('end_date', 'Unknown'))

        # Format dates (take first 10 chars if longer)
        if pd.notna(start_date) and len(start_date) > 10:
            start_date = start_date[:10]
        if pd.notna(end_date) and len(end_date) > 10:
            end_date = end_date[:10]

        # Truncate description
        if len(description) > 200:
            description = description[:200] + '...'

        popup_html = f"""
        <div style="width: 300px; font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0; color: {color};">
                <b>{road_name}</b>
            </h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;">
                <b>Direction:</b> {direction}<br>
                <b>Impact:</b> {vehicle_impact.replace('-', ' ').title()}<br>
                {'<b style="color: red;">⚠️ Workers Present</b><br>' if workers_present else ''}
                <b>Start:</b> {start_date}<br>
                <b>End:</b> {end_date}
            </p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; font-size: 11px; color: #666;">
                {description}
            </p>
        </div>
        """
        return popup_html

    def create_base_map(self, center: Optional[Tuple[float, float]] = None,
                       zoom_start: int = 9, tiles: str = 'OpenStreetMap') -> folium.Map:
        """
        Create base Folium map

        Args:
            center: (lat, lon) tuple, or None to auto-calculate
            zoom_start: Initial zoom level
            tiles: Map tile style

        Returns:
            Folium Map object
        """
        if center is None:
            center = self.get_center()

        self.map = folium.Map(
            location=center,
            zoom_start=zoom_start,
            tiles=tiles
        )
        return self.map

    def add_markers(self, use_layers: bool = True,
                   use_clustering: bool = False) -> folium.Map:
        """
        Add work zone markers to map

        Args:
            use_layers: If True, create separate layers for different impact types
            use_clustering: If True, use marker clustering

        Returns:
            Updated Folium Map object
        """
        if self.map is None:
            self.create_base_map()

        # Calculate statistics
        self.calculate_stats()

        if use_layers:
            # Create feature groups for different impact types
            layers = {
                'all_closed': folium.FeatureGroup(name='All Lanes Closed', show=True),
                'some_closed': folium.FeatureGroup(name='Some Lanes Closed', show=True),
                'shifts': folium.FeatureGroup(name='Lane Shifts', show=True),
                'open': folium.FeatureGroup(name='All Lanes Open', show=False),
                'unknown': folium.FeatureGroup(name='Unknown Impact', show=False)
            }
        elif use_clustering:
            marker_cluster = plugins.MarkerCluster()
        else:
            layers = None

        # Add markers
        for idx, row in self.df.iterrows():
            try:
                lat = row['latitude']
                lon = row['longitude']
                vehicle_impact = row.get('vehicle_impact', 'unknown')

                # Get marker properties
                color = self.get_color(vehicle_impact)
                icon = self.get_icon(vehicle_impact)

                # Create popup
                popup_html = self.create_popup_html(row)

                # Create tooltip
                tooltip = f"{row.get('road_name', 'Unknown')} - {vehicle_impact.replace('-', ' ').title()}"

                # Create marker
                marker = folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=tooltip,
                    icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
                )

                # Add to appropriate container
                if use_clustering:
                    marker.add_to(marker_cluster)
                elif use_layers:
                    # Determine which layer
                    if 'all-lanes-closed' in vehicle_impact:
                        marker.add_to(layers['all_closed'])
                    elif 'some-lanes-closed' in vehicle_impact:
                        marker.add_to(layers['some_closed'])
                    elif 'shift' in vehicle_impact:
                        marker.add_to(layers['shifts'])
                    elif 'all-lanes-open' in vehicle_impact:
                        marker.add_to(layers['open'])
                    else:
                        marker.add_to(layers['unknown'])
                else:
                    marker.add_to(self.map)

            except Exception as e:
                print(f"Warning: Error adding marker for row {idx}: {e}")
                continue

        # Add layers or cluster to map
        if use_clustering:
            marker_cluster.add_to(self.map)
        elif use_layers:
            for layer in layers.values():
                layer.add_to(self.map)

        return self.map

    def add_layer_control(self) -> folium.Map:
        """Add layer control to map"""
        if self.map is not None:
            folium.LayerControl(collapsed=False).add_to(self.map)
        return self.map

    def add_legend(self, state_name: str = "Work Zones") -> folium.Map:
        """
        Add custom legend to map

        Args:
            state_name: Name to display in legend title

        Returns:
            Updated Folium Map object
        """
        if self.map is None or not self.stats:
            return self.map

        legend_html = f"""
        <div style="position: fixed;
                    bottom: 50px; right: 50px; width: 280px; height: auto;
                    background-color: white; z-index: 9999; font-size: 14px;
                    border: 2px solid grey; border-radius: 5px; padding: 10px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <h4 style="margin: 0 0 10px 0; text-align: center;">
                {state_name}
            </h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">
                Total: {self.stats['total']} work zones
            </p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;">
                <i class="glyphicon glyphicon-road" style="color: red;"></i>
                All lanes closed: <b>{self.stats['all_closed']}</b>
            </p>
            <p style="margin: 5px 0;">
                <i class="glyphicon glyphicon-exclamation-triangle" style="color: orange;"></i>
                Some lanes closed: <b>{self.stats['some_closed']}</b>
            </p>
            <p style="margin: 5px 0;">
                <i class="glyphicon glyphicon-info-sign" style="color: blue;"></i>
                Lane shifts: <b>{self.stats['shifts']}</b>
            </p>
            <p style="margin: 5px 0;">
                <i class="glyphicon glyphicon-info-sign" style="color: green;"></i>
                All lanes open: <b>{self.stats['open']}</b>
            </p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; color: red; font-weight: bold;">
                ⚠️ Workers present: {self.stats['workers']}
            </p>
        </div>
        """

        self.map.get_root().html.add_child(folium.Element(legend_html))
        return self.map

    def create_map(self, center: Optional[Tuple[float, float]] = None,
                   zoom_start: int = 9,
                   use_layers: bool = True,
                   use_clustering: bool = False,
                   add_legend: bool = True,
                   state_name: str = "Work Zones") -> folium.Map:
        """
        Create complete map with all features

        Args:
            center: (lat, lon) tuple for map center, or None to auto-calculate
            zoom_start: Initial zoom level
            use_layers: Create separate layers for different impact types
            use_clustering: Use marker clustering (overrides use_layers)
            add_legend: Add legend with statistics
            state_name: Name to display in legend

        Returns:
            Complete Folium Map object
        """
        # Create base map
        self.create_base_map(center=center, zoom_start=zoom_start)

        # Add markers
        self.add_markers(use_layers=use_layers, use_clustering=use_clustering)

        # Add layer control (if using layers)
        if use_layers and not use_clustering:
            self.add_layer_control()

        # Add legend
        if add_legend:
            self.add_legend(state_name=state_name)

        return self.map

    def save_map(self, filename: str = 'work_zones_map.html') -> str:
        """
        Save map to HTML file

        Args:
            filename: Output filename

        Returns:
            Filename of saved map
        """
        if self.map is not None:
            self.map.save(filename)
            return filename
        else:
            raise ValueError("No map created. Call create_map() first.")

    def get_statistics(self) -> Dict:
        """Get current statistics"""
        if not self.stats:
            self.calculate_stats()
        return self.stats


class MultiStateMapper:
    """Create comparison maps for multiple states"""

    STATE_COLORS = {
        'California': 'blue',
        'New York': 'red',
        'Colorado': 'green',
        'Iowa': 'purple',
        'Massachusetts': 'orange',
        'Texas': 'darkred',
        'Florida': 'lightblue',
        'Utah': 'darkgreen'
    }

    def __init__(self, work_zones_by_state: Dict[str, List[Dict]]):
        """
        Initialize multi-state mapper

        Args:
            work_zones_by_state: Dict with state names as keys and
                                 lists of work zone dicts as values
        """
        self.work_zones_by_state = work_zones_by_state
        self.map = None
        self.stats_by_state = {}

    def create_comparison_map(self, center: Tuple[float, float] = (39.8, -98.6),
                             zoom_start: int = 4,
                             max_markers_per_state: Optional[int] = 500) -> folium.Map:
        """
        Create map comparing multiple states

        Args:
            center: Map center (default: center of USA)
            zoom_start: Initial zoom level
            max_markers_per_state: Limit markers per state for performance

        Returns:
            Folium Map object
        """
        # Create base map
        self.map = folium.Map(
            location=center,
            zoom_start=zoom_start,
            tiles='OpenStreetMap'
        )

        # Create layer for each state
        for state_name, work_zones in self.work_zones_by_state.items():
            color = self.STATE_COLORS.get(state_name, 'gray')

            # Limit markers if specified
            if max_markers_per_state:
                work_zones_subset = work_zones[:max_markers_per_state]
            else:
                work_zones_subset = work_zones

            # Create feature group for state
            state_layer = folium.FeatureGroup(
                name=f'{state_name} ({color.title()})',
                show=True
            )

            # Calculate stats
            stats = {
                'total': len(work_zones),
                'workers': sum(1 for wz in work_zones if wz.get('workers_present', False)),
                'closed': sum(1 for wz in work_zones if 'closed' in wz.get('vehicle_impact', ''))
            }
            self.stats_by_state[state_name] = stats

            # Add markers
            for zone in work_zones_subset:
                try:
                    lat = zone['latitude']
                    lon = zone['longitude']
                    road_name = zone.get('road_name', 'Unknown')
                    vehicle_impact = zone.get('vehicle_impact', 'unknown')
                    workers_present = zone.get('workers_present', False)

                    # Determine icon
                    if workers_present:
                        icon = folium.Icon(color=color, icon='user', prefix='glyphicon')
                    elif 'all-lanes-closed' in vehicle_impact:
                        icon = folium.Icon(color=color, icon='road', prefix='glyphicon')
                    else:
                        icon = folium.Icon(color=color, icon='info-sign', prefix='glyphicon')

                    # Create popup
                    popup_html = f"""
                    <div style="width: 300px;">
                        <h4 style="margin: 0; color: {color};">
                            <b>{state_name}: {road_name}</b>
                        </h4>
                        <hr style="margin: 5px 0;">
                        <p style="margin: 5px 0;">
                            <b>Direction:</b> {zone.get('direction', 'unknown')}<br>
                            <b>Impact:</b> {vehicle_impact.replace('-', ' ').title()}<br>
                            {'<b style="color: red;">⚠️ Workers Present</b><br>' if workers_present else ''}
                            <b>Start:</b> {str(zone.get('start_date', ''))[:10]}<br>
                            <b>End:</b> {str(zone.get('end_date', ''))[:10]}
                        </p>
                    </div>
                    """

                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=300),
                        tooltip=f"{state_name}: {road_name} - {vehicle_impact}",
                        icon=icon
                    ).add_to(state_layer)

                except Exception as e:
                    continue

            state_layer.add_to(self.map)

        # Add layer control
        folium.LayerControl(collapsed=False).add_to(self.map)

        # Add comparison legend
        self.add_comparison_legend()

        return self.map

    def add_comparison_legend(self):
        """Add legend comparing states"""
        legend_items = []
        total_all_states = 0

        for state_name, stats in self.stats_by_state.items():
            color = self.STATE_COLORS.get(state_name, 'gray')
            total_all_states += stats['total']

            legend_items.append(f"""
            <p style="margin: 5px 0; color: {color}; font-weight: bold;">
                <i class="glyphicon glyphicon-map-marker"></i> {state_name}
            </p>
            <p style="margin: 5px 0; padding-left: 20px;">
                Total: {stats['total']}<br>
                Lane closures: {stats['closed']}<br>
                Workers present: {stats['workers']}
            </p>
            <hr style="margin: 5px 0;">
            """)

        legend_html = f"""
        <div style="position: fixed;
                    bottom: 50px; right: 50px; width: 280px; height: auto;
                    background-color: white; z-index: 9999; font-size: 14px;
                    border: 2px solid grey; border-radius: 5px; padding: 10px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                    max-height: 80vh; overflow-y: auto;">
            <h4 style="margin: 0 0 10px 0;">Multi-State Comparison</h4>
            <hr style="margin: 5px 0;">
            {''.join(legend_items)}
            <p style="margin: 5px 0; font-size: 12px; font-weight: bold;">
                Combined Total: {total_all_states} work zones
            </p>
        </div>
        """

        self.map.get_root().html.add_child(folium.Element(legend_html))

    def save_map(self, filename: str = 'multi_state_map.html') -> str:
        """Save comparison map"""
        if self.map is not None:
            self.map.save(filename)
            return filename
        else:
            raise ValueError("No map created. Call create_comparison_map() first.")
