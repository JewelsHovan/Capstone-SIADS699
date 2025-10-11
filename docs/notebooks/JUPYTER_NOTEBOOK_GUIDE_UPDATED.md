# Work Zone Analysis - Jupyter Notebook Setup Guide (Updated)

Complete copy-paste code blocks using the `wzdx_mapping.py` module for cleaner notebooks.

---

## Setup: Upload the Module File

**Before starting, upload `wzdx_mapping.py` to your Deepnote project**

Or create it in a cell:
```python
# Run this ONCE to create the mapping module
%%writefile wzdx_mapping.py
# ... paste the entire contents of wzdx_mapping.py here ...
```

---

## Notebook 1: Data Ingestion and Basic Analysis

### Cell 1: Install Required Libraries
```python
# Install required packages
!pip install folium pandas requests -q

print("✓ Libraries installed successfully!")
```

---

### Cell 2: Import Libraries
```python
import pandas as pd
import json
import requests
from datetime import datetime, timezone
import warnings
warnings.filterwarnings('ignore')

print("✓ Libraries imported successfully!")
```

---

### Cell 3: Fetch California WZDx Feed
```python
# California 511 API Configuration
CA_API_KEY = "e6f51f24-0f8b-475c-a40c-90732dd41572"
CA_FEED_URL = f"https://api.511.org/traffic/wzdx?api_key={CA_API_KEY}"

print("Fetching California work zone data...")
try:
    response = requests.get(CA_FEED_URL, timeout=30)
    response.raise_for_status()
    ca_data = response.json()

    # Save to file for backup
    with open('ca_wzdx_feed.json', 'w') as f:
        json.dump(ca_data, f, indent=2)

    print(f"✓ Successfully fetched California data")
    print(f"  Total features: {len(ca_data.get('features', []))}")

except Exception as e:
    print(f"❌ Error fetching data: {e}")
    ca_data = None
```

---

### Cell 4: Parse Work Zone Data
```python
def parse_work_zones(data):
    """Extract work zone information from WZDx GeoJSON feed"""

    work_zones = []
    features = data.get('features', [])

    for feature in features:
        try:
            # Get geometry
            geom = feature.get('geometry', {})
            geom_type = geom.get('type')
            coords = geom.get('coordinates', [])

            if not coords:
                continue

            # Extract coordinates based on geometry type
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

            # Extract work zone data
            wz = {
                'id': feature.get('id'),
                'road_name': ', '.join(core.get('road_names', ['Unknown'])),
                'direction': core.get('direction', 'unknown'),
                'description': core.get('description', 'No description'),
                'vehicle_impact': props.get('vehicle_impact', 'unknown'),
                'start_date': props.get('start_date', ''),
                'end_date': props.get('end_date', ''),
                'latitude': lat,
                'longitude': lon,
                'workers_present': props.get('worker_presence', {}).get('are_workers_present', False),
            }

            # Calculate duration if dates available
            if wz['start_date'] and wz['end_date']:
                try:
                    start = datetime.fromisoformat(wz['start_date'].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(wz['end_date'].replace('Z', '+00:00'))
                    wz['duration_days'] = (end - start).days
                except:
                    wz['duration_days'] = None
            else:
                wz['duration_days'] = None

            work_zones.append(wz)

        except Exception as e:
            continue

    return work_zones

# Parse the data
work_zones = parse_work_zones(ca_data)
print(f"✓ Parsed {len(work_zones)} work zones")
```

---

### Cell 5: Create DataFrame and View
```python
# Convert to DataFrame
df = pd.DataFrame(work_zones)

print(f"Dataset shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
df.head()
```

---

### Cell 6: Basic Statistics
```python
print("=" * 70)
print("CALIFORNIA WORK ZONE STATISTICS")
print("=" * 70)

print(f"\nTotal Work Zones: {len(df)}")

# Vehicle impact distribution
print(f"\nVehicle Impact Distribution:")
for impact, count in df['vehicle_impact'].value_counts().items():
    pct = count / len(df) * 100
    print(f"  {impact}: {count} ({pct:.1f}%)")

# Worker presence
workers_count = df['workers_present'].sum()
print(f"\nWorkers Present: {workers_count} ({workers_count/len(df)*100:.1f}%)")

# Top roads
print(f"\nTop 10 Roads:")
for road, count in df['road_name'].value_counts().head(10).items():
    print(f"  {road}: {count}")
```

---

### Cell 7: Export Data
```python
# Export for team sharing
df.to_csv('california_work_zones.csv', index=False)
print(f"✓ Exported to california_work_zones.csv")
```

---

## Notebook 2: Interactive Map (Using Module)

### Cell 1: Import Mapping Module
```python
import folium
from wzdx_mapping import WorkZoneMapper
import pandas as pd

# Load data
df = pd.read_csv('california_work_zones.csv')
work_zones = df.to_dict('records')

print(f"✓ Loaded {len(work_zones)} work zones")
```

---

### Cell 2: Create Map - Simple Version
```python
# Create mapper instance
mapper = WorkZoneMapper(work_zones)

# Create complete map with all features
m = mapper.create_map(
    zoom_start=9,
    use_layers=True,
    add_legend=True,
    state_name="California Work Zones"
)

# Display in notebook
m
```

---

### Cell 3: Create Map - Custom Options
```python
# Create mapper
mapper = WorkZoneMapper(work_zones)

# Create map with custom settings
m = mapper.create_map(
    center=(37.5, -122.0),  # Custom center
    zoom_start=10,           # More zoomed in
    use_layers=True,         # Separate layers
    use_clustering=False,    # No clustering
    add_legend=True,
    state_name="California Bay Area Work Zones"
)

# Display
m
```

---

### Cell 4: Create Map - With Clustering (for large datasets)
```python
# Use clustering for better performance with many markers
mapper = WorkZoneMapper(work_zones)

m = mapper.create_map(
    use_clustering=True,  # Use marker clustering
    use_layers=False,     # Can't use both
    add_legend=True
)

m
```

---

### Cell 5: Save Map
```python
# Save to HTML file
filename = mapper.save_map('california_work_zones_map.html')
print(f"✓ Map saved to {filename}")

# Get statistics
stats = mapper.get_statistics()
print(f"\nMap Statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")
```

---

## Notebook 3: Multi-State Comparison (Using Module)

### Cell 1: Fetch Multiple States
```python
import requests
import json
from wzdx_mapping import MultiStateMapper

# Fetch California
ca_response = requests.get(
    "https://api.511.org/traffic/wzdx?api_key=e6f51f24-0f8b-475c-a40c-90732dd41572"
)
ca_data = ca_response.json()

# Fetch New York
ny_response = requests.get("https://511ny.org/api/wzdx")
ny_data = ny_response.json()

print("✓ Fetched data from both states")
```

---

### Cell 2: Parse Both States
```python
# Parse both states (using same parse function from Notebook 1)
ca_zones = parse_work_zones(ca_data)
ny_zones = parse_work_zones(ny_data)

print(f"California: {len(ca_zones)} work zones")
print(f"New York: {len(ny_zones)} work zones")
```

---

### Cell 3: Create Comparison Map
```python
# Create multi-state mapper
multi_mapper = MultiStateMapper({
    'California': ca_zones,
    'New York': ny_zones
})

# Create comparison map
m_compare = multi_mapper.create_comparison_map(
    center=(39.8, -98.6),  # Center of USA
    zoom_start=4,
    max_markers_per_state=500  # Limit for performance
)

# Display
m_compare
```

---

### Cell 4: Save Comparison Map
```python
# Save map
filename = multi_mapper.save_map('multi_state_comparison.html')
print(f"✓ Saved to {filename}")

# View statistics
print("\nState Statistics:")
for state, stats in multi_mapper.stats_by_state.items():
    print(f"\n{state}:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
```

---

## Notebook 4: Advanced - Custom Map Styling

### Cell 1: Step-by-Step Custom Map
```python
from wzdx_mapping import WorkZoneMapper

# Load data
df = pd.read_csv('california_work_zones.csv')
work_zones = df.to_dict('records')

# Create mapper
mapper = WorkZoneMapper(work_zones)

# Step 1: Create base map
mapper.create_base_map(
    center=(37.5, -122.0),
    zoom_start=9,
    tiles='OpenStreetMap'  # or 'CartoDB positron', 'Stamen Terrain', etc.
)

# Step 2: Add markers with custom options
mapper.add_markers(
    use_layers=True,
    use_clustering=False
)

# Step 3: Add controls
mapper.add_layer_control()

# Step 4: Add legend
mapper.add_legend(state_name="California Work Zones")

# Display
mapper.map
```

---

### Cell 2: Get Color/Icon for Custom Markers
```python
# You can access color/icon methods directly
mapper = WorkZoneMapper(work_zones)

# Example: Get colors for different impacts
impacts = ['all-lanes-closed', 'some-lanes-closed', 'all-lanes-open']
for impact in impacts:
    color = mapper.get_color(impact)
    icon = mapper.get_icon(impact)
    print(f"{impact}: color={color}, icon={icon}")
```

---

### Cell 3: Custom Popup HTML
```python
# Create custom popup for specific work zone
sample_zone = work_zones[0]
mapper = WorkZoneMapper([sample_zone])

# Get the popup HTML
popup_html = mapper.create_popup_html(pd.Series(sample_zone))
print("Sample popup HTML:")
print(popup_html)
```

---

## Quick Reference: All-in-One Cells

### Option A: Quick Map (Minimal Code)
```python
from wzdx_mapping import WorkZoneMapper
import pandas as pd

# Load data
df = pd.read_csv('california_work_zones.csv')
work_zones = df.to_dict('records')

# Create and display map (one line!)
WorkZoneMapper(work_zones).create_map(state_name="California")
```

---

### Option B: Quick Multi-State Map
```python
from wzdx_mapping import MultiStateMapper
import requests

# Fetch and parse (you need parse_work_zones from earlier)
ca_data = requests.get(
    "https://api.511.org/traffic/wzdx?api_key=e6f51f24-0f8b-475c-a40c-90732dd41572"
).json()
ny_data = requests.get("https://511ny.org/api/wzdx").json()

ca_zones = parse_work_zones(ca_data)
ny_zones = parse_work_zones(ny_data)

# Create and display comparison map
MultiStateMapper({
    'California': ca_zones,
    'New York': ny_zones
}).create_comparison_map()
```

---

## Module Benefits

### Before (Without Module)
- 100+ lines of map creation code
- Duplicate code across notebooks
- Hard to maintain
- Difficult to share with team

### After (With Module)
- 3-5 lines of code
- Reusable across notebooks
- Easy to maintain
- Professional code organization
- Team can import and use

---

## Module Usage Examples

### Example 1: Basic Map
```python
from wzdx_mapping import WorkZoneMapper

mapper = WorkZoneMapper(work_zones)
m = mapper.create_map(state_name="My Work Zones")
m  # Display
```

---

### Example 2: Custom Center and Zoom
```python
mapper = WorkZoneMapper(work_zones)
m = mapper.create_map(
    center=(37.7749, -122.4194),  # San Francisco
    zoom_start=12,
    state_name="SF Work Zones"
)
m
```

---

### Example 3: With Clustering
```python
mapper = WorkZoneMapper(work_zones)
m = mapper.create_map(use_clustering=True)
mapper.save_map('clustered_map.html')
```

---

### Example 4: Access Statistics
```python
mapper = WorkZoneMapper(work_zones)
stats = mapper.get_statistics()

print(f"Total: {stats['total']}")
print(f"All closed: {stats['all_closed']}")
print(f"Workers present: {stats['workers']}")
```

---

### Example 5: Multi-State with 3+ States
```python
from wzdx_mapping import MultiStateMapper

# Assuming you have data for 3 states
multi = MultiStateMapper({
    'California': ca_zones,
    'New York': ny_zones,
    'Colorado': co_zones
})

m = multi.create_comparison_map()
multi.save_map('three_state_comparison.html')
```

---

## Tips for Deepnote

### 1. Upload Module Once
Upload `wzdx_mapping.py` to your Deepnote workspace, then import in any notebook

### 2. Share with Team
Everyone can use the same module - consistent results!

### 3. Version Control
Keep module in version control (git) for team collaboration

### 4. Extend the Module
Add your own methods to `WorkZoneMapper` class:
```python
# In wzdx_mapping.py
class WorkZoneMapper:
    # ... existing code ...

    def filter_by_road(self, road_name):
        """Filter work zones by road name"""
        filtered = [wz for wz in self.work_zones if road_name in wz['road_name']]
        return WorkZoneMapper(filtered)
```

---

## Summary

**Old way (Notebook 2 original)**:
- 9 cells of map creation code
- ~150 lines total
- Hard to modify
- Duplicate across notebooks

**New way (with module)**:
- 2-5 cells total
- ~10-20 lines of code
- Easy to customize
- Reuse everywhere

**Benefits**:
✅ Cleaner notebooks
✅ Easier to share
✅ Professional organization
✅ Maintainable code
✅ Team-friendly

---

## Next Steps

1. Upload `wzdx_mapping.py` to Deepnote
2. Import in your notebooks
3. Create maps with 3-5 lines of code!
4. Share with team members

Happy mapping! 🗺️
