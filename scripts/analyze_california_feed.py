"""
Fetch and analyze California 511 WZDx feed
"""

from wzdx_analyzer import WZDxAnalyzer
import requests
import json


def main():
    analyzer = WZDxAnalyzer()

    ca_feed_url = "https://api.511.org/traffic/wzdx?api_key=e6f51f24-0f8b-475c-a40c-90732dd41572"

    print("=" * 70)
    print("CALIFORNIA 511 WZDX FEED ANALYSIS")
    print("=" * 70)
    print(f"\nFetching feed from: 511.org (California)")

    try:
        # Fetch the feed
        print("Downloading feed...")
        response = requests.get(ca_feed_url, timeout=30)
        response.raise_for_status()

        # Save raw feed
        with open('ca_wzdx_feed.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
        print("✓ Feed saved to: ca_wzdx_feed.json")

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

            # Display key info
            print(f"\nTotal Active Work Zones: {len(df)}\n")

            # Show sample of work zones
            print("Sample Work Zones:")
            print("-" * 70)
            for idx, row in df.head(15).iterrows():
                print(f"\n{idx + 1}. {row['road_names']} ({row.get('direction', 'N/A')})")
                print(f"   Impact: {row.get('vehicle_impact', 'N/A')}")
                if row.get('has_workers'):
                    print(f"   ⚠️  Workers Present")
                if row.get('lanes_closed', 0) > 0:
                    print(f"   🚧 {row['lanes_closed']} lane(s) closed")
                if row.get('reduced_speed_limit_kph'):
                    mph = row['reduced_speed_limit_kph'] * 0.621371
                    print(f"   🚗 Speed Limit: {mph:.0f} mph")
                if row.get('start_date'):
                    print(f"   Start: {row['start_date']}")

            # Additional statistics
            print("\n" + "=" * 70)
            print("CALIFORNIA STATISTICS")
            print("=" * 70)

            if 'direction' in df.columns:
                print(f"\nDirection Distribution:")
                for direction, count in df['direction'].value_counts().head(10).items():
                    print(f"  - {direction}: {count}")

            if 'vehicle_impact' in df.columns:
                print(f"\nVehicle Impact Types:")
                for impact, count in df['vehicle_impact'].value_counts().items():
                    print(f"  - {impact}: {count}")

            # Top roads
            print(f"\nTop 10 Roads with Most Work Zones:")
            for road, count in df['road_names'].value_counts().head(10).items():
                print(f"  - {road}: {count}")

            # Export to CSV for further analysis
            csv_file = 'ca_work_zones_analysis.csv'
            df.to_csv(csv_file, index=False)
            print(f"\n✓ Full data exported to: {csv_file}")

        # Check for devices
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
        print("  - Invalid API key")
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
