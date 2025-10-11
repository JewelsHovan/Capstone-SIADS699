"""
Fetch and analyze the New York 511 WZDx feed
"""

from wzdx_analyzer import WZDxAnalyzer
import requests
import json


def main():
    analyzer = WZDxAnalyzer()

    ny_feed_url = "https://511ny.org/api/wzdx"

    print("=" * 70)
    print("NEW YORK DOT WZDX FEED ANALYSIS")
    print("=" * 70)
    print(f"\nFetching feed from: {ny_feed_url}")

    try:
        # Fetch the feed
        print("Downloading feed...")
        response = requests.get(ny_feed_url, timeout=30)
        response.raise_for_status()

        # Save raw feed
        with open('ny_wzdx_feed.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
        print("✓ Feed saved to: ny_wzdx_feed.json")

        # Load into analyzer
        analyzer.feed_data = response.json()

        # Display comprehensive summary
        print("\n" + analyzer.summarize())

        # Extract and display detailed work zone information
        work_zones = analyzer.extract_work_zones()

        if work_zones:
            print("\n" + "=" * 70)
            print("DETAILED WORK ZONE INFORMATION")
            print("=" * 70)

            df = analyzer.to_dataframe('work_zones')

            # Display key columns
            print(f"\nTotal Active Work Zones: {len(df)}\n")

            # Show sample of work zones
            display_cols = ['road_names', 'direction', 'vehicle_impact', 'has_workers', 'lanes_closed']
            available_cols = [col for col in display_cols if col in df.columns]

            print("Sample Work Zones:")
            print("-" * 70)
            for idx, row in df.head(10).iterrows():
                print(f"\n{idx + 1}. {row['road_names']} ({row.get('direction', 'N/A')})")
                print(f"   Impact: {row.get('vehicle_impact', 'N/A')}")
                if row.get('has_workers'):
                    print(f"   ⚠️  Workers Present")
                if row.get('lanes_closed', 0) > 0:
                    print(f"   🚧 {row['lanes_closed']} lane(s) closed")
                if row.get('reduced_speed_limit_kph'):
                    mph = row['reduced_speed_limit_kph'] * 0.621371
                    print(f"   🚗 Speed Limit: {mph:.0f} mph")
                print(f"   Start: {row.get('start_date', 'N/A')}")
                print(f"   End: {row.get('end_date', 'N/A')}")

            # Additional statistics
            print("\n" + "=" * 70)
            print("SAFETY STATISTICS")
            print("=" * 70)

            if 'direction' in df.columns:
                print(f"\nDirection Distribution:")
                for direction, count in df['direction'].value_counts().items():
                    print(f"  - {direction}: {count}")

            if 'work_zone_type' in df.columns:
                print(f"\nWork Zone Types:")
                for wz_type, count in df['work_zone_type'].value_counts().items():
                    print(f"  - {wz_type}: {count}")

            # Export to CSV for further analysis
            csv_file = 'ny_work_zones_analysis.csv'
            df.to_csv(csv_file, index=False)
            print(f"\n✓ Full data exported to: {csv_file}")

        # Also check for devices
        devices = analyzer.extract_devices()
        if devices:
            print(f"\n\nField Devices Found: {len(devices)}")
            device_df = analyzer.to_dataframe('devices')
            if not device_df.empty:
                print("\nDevice Types:")
                for dev_type, count in device_df['device_type'].value_counts().items():
                    print(f"  - {dev_type}: {count}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching feed: {e}")
        print("\nThis could be due to:")
        print("  - Network connectivity issues")
        print("  - The feed URL requiring authentication")
        print("  - The feed being temporarily unavailable")
    except json.JSONDecodeError as e:
        print(f"\n❌ Error parsing JSON: {e}")
        print("The response may not be valid JSON")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
