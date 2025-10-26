"""
WZDx Data Analyzer
Utility for parsing and analyzing Work Zone Data Exchange (WZDx) feeds
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import requests


class WZDxAnalyzer:
    """Analyzes WZDx GeoJSON feeds for work zone safety insights"""

    def __init__(self):
        self.feed_data = None
        self.work_zones = []
        self.devices = []

    def load_feed(self, file_path: str) -> Dict:
        """Load a WZDx feed from a GeoJSON file"""
        with open(file_path, 'r') as f:
            self.feed_data = json.load(f)
        return self.feed_data

    def fetch_feed(self, url: str) -> Dict:
        """Fetch a WZDx feed from a URL"""
        response = requests.get(url)
        response.raise_for_status()
        self.feed_data = response.json()
        return self.feed_data

    def get_feed_info(self) -> Dict:
        """Extract feed metadata"""
        if not self.feed_data:
            return {}

        feed_info = self.feed_data.get('feed_info', {})
        return {
            'publisher': feed_info.get('publisher'),
            'version': feed_info.get('version'),
            'update_date': feed_info.get('update_date'),
            'update_frequency': feed_info.get('update_frequency'),
            'contact_email': feed_info.get('contact_email'),
            'num_data_sources': len(feed_info.get('data_sources', []))
        }

    def extract_work_zones(self) -> List[Dict]:
        """Extract work zone information from feed"""
        if not self.feed_data:
            return []

        work_zones = []
        features = self.feed_data.get('features', [])

        for feature in features:
            props = feature.get('properties', {})
            core = props.get('core_details', {})

            # Only process work-zone events (not devices)
            if core.get('event_type') == 'work-zone':
                wz = {
                    'id': feature.get('id'),
                    'event_type': core.get('event_type'),
                    'road_names': ', '.join(core.get('road_names', [])),
                    'direction': core.get('direction'),
                    'description': core.get('description', ''),
                    'start_date': props.get('start_date'),
                    'end_date': props.get('end_date'),
                    'vehicle_impact': props.get('vehicle_impact'),
                    'work_zone_type': props.get('work_zone_type', 'static'),
                    'reduced_speed_limit_kph': props.get('reduced_speed_limit_kph'),
                    'beginning_milepost': props.get('beginning_milepost'),
                    'ending_milepost': props.get('ending_milepost'),
                    'num_lanes': len(props.get('lanes', [])),
                    'lanes_closed': sum(1 for lane in props.get('lanes', []) if lane.get('status') == 'closed'),
                    'has_workers': props.get('worker_presence', {}).get('are_workers_present', False),
                    'geometry_type': feature.get('geometry', {}).get('type'),
                    'num_coordinates': len(feature.get('geometry', {}).get('coordinates', []))
                }
                work_zones.append(wz)

        self.work_zones = work_zones
        return work_zones

    def extract_devices(self) -> List[Dict]:
        """Extract field device information from feed"""
        if not self.feed_data:
            return []

        devices = []
        features = self.feed_data.get('features', [])

        for feature in features:
            props = feature.get('properties', {})
            core = props.get('core_details', {})

            # Check if this is a device (has device_type)
            if 'device_type' in core:
                device = {
                    'id': feature.get('id'),
                    'device_type': core.get('device_type'),
                    'device_status': core.get('device_status'),
                    'road_names': ', '.join(core.get('road_names', [])),
                    'road_direction': core.get('road_direction'),
                    'name': core.get('name', ''),
                    'is_moving': core.get('is_moving', False),
                    'has_automatic_location': core.get('has_automatic_location', False),
                    'update_date': core.get('update_date'),
                    'geometry_type': feature.get('geometry', {}).get('type'),
                    'coordinates': feature.get('geometry', {}).get('coordinates', [])
                }

                # Add device-specific properties
                if core.get('device_type') == 'arrow-board':
                    device['pattern'] = props.get('pattern')
                    device['is_in_transport_position'] = props.get('is_in_transport_position')

                devices.append(device)

        self.devices = devices
        return devices

    def to_dataframe(self, data_type: str = 'work_zones') -> pd.DataFrame:
        """Convert extracted data to pandas DataFrame"""
        if data_type == 'work_zones' and self.work_zones:
            return pd.DataFrame(self.work_zones)
        elif data_type == 'devices' and self.devices:
            return pd.DataFrame(self.devices)
        else:
            return pd.DataFrame()

    def analyze_safety_metrics(self) -> Dict:
        """Analyze key safety metrics from work zones"""
        if not self.work_zones:
            return {}

        df = self.to_dataframe('work_zones')

        metrics = {
            'total_work_zones': len(df),
            'work_zones_with_workers': df['has_workers'].sum() if 'has_workers' in df else 0,
            'work_zones_with_closures': (df['lanes_closed'] > 0).sum() if 'lanes_closed' in df else 0,
            'avg_lanes_closed': df['lanes_closed'].mean() if 'lanes_closed' in df else 0,
            'work_zones_with_speed_reduction': df['reduced_speed_limit_kph'].notna().sum() if 'reduced_speed_limit_kph' in df else 0,
            'vehicle_impact_types': df['vehicle_impact'].value_counts().to_dict() if 'vehicle_impact' in df else {},
            'work_zone_types': df['work_zone_type'].value_counts().to_dict() if 'work_zone_type' in df else {},
            'directions': df['direction'].value_counts().to_dict() if 'direction' in df else {}
        }

        return metrics

    def get_geographic_bounds(self) -> Dict:
        """Calculate geographic bounding box of all work zones"""
        if not self.feed_data:
            return {}

        lats, lons = [], []
        for feature in self.feed_data.get('features', []):
            geom = feature.get('geometry', {})
            coords = geom.get('coordinates', [])

            if geom.get('type') == 'LineString':
                for coord in coords:
                    lons.append(coord[0])
                    lats.append(coord[1])
            elif geom.get('type') == 'Point':
                lons.append(coords[0])
                lats.append(coords[1])

        if lats and lons:
            return {
                'min_lat': min(lats),
                'max_lat': max(lats),
                'min_lon': min(lons),
                'max_lon': max(lons),
                'center_lat': sum(lats) / len(lats),
                'center_lon': sum(lons) / len(lons)
            }
        return {}

    def summarize(self) -> str:
        """Generate a text summary of the feed"""
        if not self.feed_data:
            return "No feed data loaded."

        feed_info = self.get_feed_info()
        work_zones = self.extract_work_zones()
        devices = self.extract_devices()
        metrics = self.analyze_safety_metrics()
        bounds = self.get_geographic_bounds()

        summary = []
        summary.append("=" * 60)
        summary.append("WZDx FEED SUMMARY")
        summary.append("=" * 60)
        summary.append(f"\nFeed Information:")
        summary.append(f"  Publisher: {feed_info.get('publisher')}")
        summary.append(f"  Version: {feed_info.get('version')}")
        summary.append(f"  Last Update: {feed_info.get('update_date')}")
        summary.append(f"  Update Frequency: {feed_info.get('update_frequency')} seconds")

        summary.append(f"\nContent:")
        summary.append(f"  Work Zones: {len(work_zones)}")
        summary.append(f"  Field Devices: {len(devices)}")

        if metrics:
            summary.append(f"\nSafety Metrics:")
            summary.append(f"  Work zones with workers present: {metrics.get('work_zones_with_workers')}")
            summary.append(f"  Work zones with lane closures: {metrics.get('work_zones_with_closures')}")
            summary.append(f"  Average lanes closed: {metrics.get('avg_lanes_closed', 0):.2f}")
            summary.append(f"  Work zones with speed reductions: {metrics.get('work_zones_with_speed_reduction')}")

            if metrics.get('vehicle_impact_types'):
                summary.append(f"\n  Vehicle Impact Types:")
                for impact, count in metrics['vehicle_impact_types'].items():
                    summary.append(f"    - {impact}: {count}")

        if bounds:
            summary.append(f"\nGeographic Coverage:")
            summary.append(f"  Center: ({bounds['center_lat']:.4f}, {bounds['center_lon']:.4f})")
            summary.append(f"  Bounds: ({bounds['min_lat']:.4f}, {bounds['min_lon']:.4f}) to ({bounds['max_lat']:.4f}, {bounds['max_lon']:.4f})")

        summary.append("\n" + "=" * 60)

        return "\n".join(summary)


def main():
    """Example usage"""
    analyzer = WZDxAnalyzer()

    # Example: Load a local file
    print("Example: Loading local WZDx feed...")
    analyzer.load_feed('wzdx/examples/WorkZoneFeed/scenario1_simple_linestring_example.geojson')
    print(analyzer.summarize())

    # Example: Get detailed work zone data
    work_zones_df = analyzer.to_dataframe('work_zones')
    print(f"\nWork Zone Details:")
    print(work_zones_df[['road_names', 'direction', 'vehicle_impact', 'lanes_closed']].head())


if __name__ == "__main__":
    main()
