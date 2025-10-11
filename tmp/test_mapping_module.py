"""
Test script to demonstrate the wzdx_mapping module
"""

from wzdx_mapping import WorkZoneMapper, MultiStateMapper
import pandas as pd


def test_single_state():
    """Test single-state mapping"""
    print("=" * 70)
    print("TEST 1: Single State Map (California)")
    print("=" * 70)

    # Load California data
    df = pd.read_csv('california_work_zones.csv')
    work_zones = df.to_dict('records')

    print(f"\nLoaded {len(work_zones)} work zones")

    # Create mapper
    mapper = WorkZoneMapper(work_zones)

    # Create map
    print("\nCreating map...")
    m = mapper.create_map(
        zoom_start=9,
        use_layers=True,
        state_name="California Work Zones"
    )

    # Save
    filename = mapper.save_map('test_california_map.html')
    print(f"✓ Map saved to {filename}")

    # Get statistics
    stats = mapper.get_statistics()
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def test_clustering():
    """Test map with clustering"""
    print("\n" + "=" * 70)
    print("TEST 2: Map with Clustering")
    print("=" * 70)

    df = pd.read_csv('california_work_zones.csv')
    work_zones = df.to_dict('records')

    mapper = WorkZoneMapper(work_zones)
    m = mapper.create_map(
        use_clustering=True,
        use_layers=False,
        state_name="California (Clustered)"
    )

    filename = mapper.save_map('test_clustered_map.html')
    print(f"✓ Clustered map saved to {filename}")


def test_multi_state():
    """Test multi-state comparison"""
    print("\n" + "=" * 70)
    print("TEST 3: Multi-State Comparison")
    print("=" * 70)

    # Load California
    ca_df = pd.read_csv('california_work_zones.csv')
    ca_zones = ca_df.to_dict('records')
    print(f"California: {len(ca_zones)} work zones")

    # Load New York
    ny_df = pd.read_csv('ny_work_zones_analysis.csv')
    ny_zones = ny_df.to_dict('records')
    print(f"New York: {len(ny_zones)} work zones")

    # Create multi-state mapper
    multi = MultiStateMapper({
        'California': ca_zones,
        'New York': ny_zones
    })

    print("\nCreating comparison map...")
    m = multi.create_comparison_map(max_markers_per_state=500)

    filename = multi.save_map('test_multi_state_map.html')
    print(f"✓ Comparison map saved to {filename}")

    print("\nState Statistics:")
    for state, stats in multi.stats_by_state.items():
        print(f"\n{state}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")


def test_custom_options():
    """Test custom map options"""
    print("\n" + "=" * 70)
    print("TEST 4: Custom Map Options")
    print("=" * 70)

    df = pd.read_csv('california_work_zones.csv')
    work_zones = df.to_dict('records')

    # Create mapper
    mapper = WorkZoneMapper(work_zones)

    # Create map with custom center (San Francisco)
    print("\nCreating map centered on San Francisco...")
    m = mapper.create_map(
        center=(37.7749, -122.4194),
        zoom_start=12,
        use_layers=True,
        state_name="San Francisco Work Zones"
    )

    filename = mapper.save_map('test_sf_map.html')
    print(f"✓ SF map saved to {filename}")


def test_step_by_step():
    """Test step-by-step map creation"""
    print("\n" + "=" * 70)
    print("TEST 5: Step-by-Step Map Creation")
    print("=" * 70)

    df = pd.read_csv('california_work_zones.csv')
    work_zones = df.to_dict('records')[:100]  # First 100 for speed

    mapper = WorkZoneMapper(work_zones)

    print("\nStep 1: Create base map")
    mapper.create_base_map(zoom_start=9)

    print("Step 2: Add markers")
    mapper.add_markers(use_layers=True)

    print("Step 3: Add layer control")
    mapper.add_layer_control()

    print("Step 4: Add legend")
    mapper.add_legend(state_name="California (Step by Step)")

    print("Step 5: Save map")
    filename = mapper.save_map('test_step_by_step_map.html')
    print(f"✓ Map saved to {filename}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TESTING WZDX MAPPING MODULE")
    print("=" * 70)

    try:
        test_single_state()
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")

    try:
        test_clustering()
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")

    try:
        test_multi_state()
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")

    try:
        test_custom_options()
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")

    try:
        test_step_by_step()
    except Exception as e:
        print(f"❌ Test 5 failed: {e}")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - test_california_map.html")
    print("  - test_clustered_map.html")
    print("  - test_multi_state_map.html")
    print("  - test_sf_map.html")
    print("  - test_step_by_step_map.html")
