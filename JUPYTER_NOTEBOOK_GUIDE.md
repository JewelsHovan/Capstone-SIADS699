# Work Zone Analysis - Jupyter Notebook Setup Guide

Complete copy-paste code blocks for Deepnote/Jupyter notebooks for team collaboration.

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
import folium from folium import plugins
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
    print(f"  Feed version: {ca_data.get('feed_info', {}).get('version', 'Unknown')}")

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
                # Use middle point
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
                'location_method': props.get('location_method', 'unknown'),
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

### Cell 5: Create DataFrame
```python
# Convert to DataFrame for easy analysis
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
impact_counts = df['vehicle_impact'].value_counts()
for impact, count in impact_counts.items():
    pct = count / len(df) * 100
    print(f"  {impact}: {count} ({pct:.1f}%)")

# Worker presence
workers_count = df['workers_present'].sum()
print(f"\nWork Zones with Workers Present: {workers_count} ({workers_count/len(df)*100:.1f}%)")

# Direction distribution
print(f"\nDirection Distribution:")
for direction, count in df['direction'].value_counts().head(5).items():
    print(f"  {direction}: {count}")

# Duration statistics
if df['duration_days'].notna().any():
    print(f"\nDuration Statistics:")
    print(f"  Mean: {df['duration_days'].mean():.1f} days")
    print(f"  Median: {df['duration_days'].median():.1f} days")
    print(f"  Max: {df['duration_days'].max():.0f} days")

# Top roads
print(f"\nTop 10 Roads by Work Zone Count:")
for road, count in df['road_name'].value_counts().head(10).items():
    print(f"  {road}: {count}")

# Geographic bounds
print(f"\nGeographic Coverage:")
print(f"  Latitude range: {df['latitude'].min():.4f} to {df['latitude'].max():.4f}")
print(f"  Longitude range: {df['longitude'].min():.4f} to {df['longitude'].max():.4f}")
print(f"  Center: ({df['latitude'].mean():.4f}, {df['longitude'].mean():.4f})")
```

---

### Cell 7: Export to CSV
```python
# Export data for sharing with team
csv_filename = 'california_work_zones.csv'
df.to_csv(csv_filename, index=False)
print(f"✓ Data exported to {csv_filename}")
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(df.columns)}")
```

---

## Notebook 2: Interactive Map Visualization

### Cell 1: Setup (if starting fresh notebook)
```python
import folium
from folium import plugins
import pandas as pd
import json

# Load data (if not already in memory)
try:
    df = pd.read_csv('california_work_zones.csv')
    print(f"✓ Loaded {len(df)} work zones from CSV")
except:
    print("❌ CSV not found. Run data ingestion notebook first.")
```

---

### Cell 2: Define Color and Icon Mapping
```python
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
    'unknown': 'gray'
}

# Icon mapping
IMPACT_ICONS = {
    'all-lanes-closed': 'road',
    'some-lanes-closed': 'exclamation-triangle',
    'all-lanes-open': 'info-sign',
    'unknown': 'question-sign'
}

def get_color(impact):
    """Get color for vehicle impact type"""
    return IMPACT_COLORS.get(impact, 'gray')

def get_icon(impact):
    """Get icon for vehicle impact type"""
    # Check for exact match first
    if impact in IMPACT_ICONS:
        return IMPACT_ICONS[impact]
    # Then check for partial match
    for key in IMPACT_ICONS:
        if key in impact:
            return IMPACT_ICONS[key]
    return 'question-sign'

print("✓ Color and icon mapping defined")
```

---

### Cell 3: Create Base Map
```python
# Create base map centered on California work zones
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=9,
    tiles='OpenStreetMap'
)

print(f"✓ Base map created")
print(f"  Center: ({center_lat:.4f}, {center_lon:.4f})")
```

---

### Cell 4: Create Feature Groups (Layers)
```python
# Create separate layers for different impact types
layer_all_closed = folium.FeatureGroup(name='All Lanes Closed', show=True)
layer_some_closed = folium.FeatureGroup(name='Some Lanes Closed', show=True)
layer_shifts = folium.FeatureGroup(name='Lane Shifts', show=True)
layer_open = folium.FeatureGroup(name='All Lanes Open', show=False)
layer_unknown = folium.FeatureGroup(name='Unknown Impact', show=False)

print("✓ Feature groups created")
```

---

### Cell 5: Add Markers to Map
```python
# Statistics for legend
stats = {
    'total': len(df),
    'all_closed': 0,
    'some_closed': 0,
    'shifts': 0,
    'open': 0,
    'workers': df['workers_present'].sum()
}

# Add markers for each work zone
for idx, row in df.iterrows():
    try:
        # Get marker properties
        color = get_color(row['vehicle_impact'])
        icon = get_icon(row['vehicle_impact'])

        # Update statistics
        if 'all-lanes-closed' in row['vehicle_impact']:
            stats['all_closed'] += 1
        elif 'some-lanes-closed' in row['vehicle_impact']:
            stats['some_closed'] += 1
        elif 'shift' in row['vehicle_impact']:
            stats['shifts'] += 1
        elif 'all-lanes-open' in row['vehicle_impact']:
            stats['open'] += 1

        # Create popup HTML
        popup_html = f"""
        <div style="width: 300px; font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0; color: {color};">
                <b>{row['road_name']}</b>
            </h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;">
                <b>Direction:</b> {row['direction']}<br>
                <b>Impact:</b> {row['vehicle_impact'].replace('-', ' ').title()}<br>
                {'<b style="color: red;">⚠️ Workers Present</b><br>' if row['workers_present'] else ''}
                <b>Start:</b> {row['start_date'][:10] if pd.notna(row['start_date']) and len(str(row['start_date'])) > 10 else row['start_date']}<br>
                <b>End:</b> {row['end_date'][:10] if pd.notna(row['end_date']) and len(str(row['end_date'])) > 10 else row['end_date']}
            </p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; font-size: 11px; color: #666;">
                {str(row['description'])[:200]}{'...' if len(str(row['description'])) > 200 else ''}
            </p>
        </div>
        """

        # Create marker
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['road_name']} - {row['vehicle_impact'].replace('-', ' ').title()}",
            icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
        )

        # Add to appropriate layer
        if 'all-lanes-closed' in row['vehicle_impact']:
            marker.add_to(layer_all_closed)
        elif 'some-lanes-closed' in row['vehicle_impact']:
            marker.add_to(layer_some_closed)
        elif 'shift' in row['vehicle_impact']:
            marker.add_to(layer_shifts)
        elif 'all-lanes-open' in row['vehicle_impact']:
            marker.add_to(layer_open)
        else:
            marker.add_to(layer_unknown)

    except Exception as e:
        print(f"Warning: Error adding marker for row {idx}: {e}")
        continue

print(f"✓ Added {stats['total']} markers to map")
```

---

### Cell 6: Add Layers and Controls
```python
# Add all layers to map
layer_all_closed.add_to(m)
layer_some_closed.add_to(m)
layer_shifts.add_to(m)
layer_open.add_to(m)
layer_unknown.add_to(m)

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)

print("✓ Layers and controls added")
```

---

### Cell 7: Add Legend
```python
# Create custom legend with statistics
legend_html = f"""
<div style="position: fixed;
            bottom: 50px; right: 50px; width: 280px; height: auto;
            background-color: white; z-index: 9999; font-size: 14px;
            border: 2px solid grey; border-radius: 5px; padding: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);">
    <h4 style="margin: 0 0 10px 0; text-align: center;">
        California Work Zones
    </h4>
    <hr style="margin: 5px 0;">
    <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">
        Total: {stats['total']} work zones
    </p>
    <hr style="margin: 5px 0;">
    <p style="margin: 5px 0;">
        <i class="glyphicon glyphicon-road" style="color: red;"></i>
        All lanes closed: <b>{stats['all_closed']}</b>
    </p>
    <p style="margin: 5px 0;">
        <i class="glyphicon glyphicon-exclamation-triangle" style="color: orange;"></i>
        Some lanes closed: <b>{stats['some_closed']}</b>
    </p>
    <p style="margin: 5px 0;">
        <i class="glyphicon glyphicon-info-sign" style="color: blue;"></i>
        Lane shifts: <b>{stats['shifts']}</b>
    </p>
    <p style="margin: 5px 0;">
        <i class="glyphicon glyphicon-info-sign" style="color: green;"></i>
        All lanes open: <b>{stats['open']}</b>
    </p>
    <hr style="margin: 5px 0;">
    <p style="margin: 5px 0; color: red; font-weight: bold;">
        ⚠️ Workers present: {stats['workers']}
    </p>
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

print("✓ Legend added")
```

---

### Cell 8: Display Map
```python
# Display the map in the notebook
m
```

---

### Cell 9: Save Map
```python
# Save map to HTML file
output_file = 'california_work_zones_map.html'
m.save(output_file)

print(f"✓ Map saved to {output_file}")
print(f"\nMap Statistics:")
print(f"  Total markers: {stats['total']}")
print(f"  All lanes closed: {stats['all_closed']}")
print(f"  Some lanes closed: {stats['some_closed']}")
print(f"  Lane shifts: {stats['shifts']}")
print(f"  Workers present: {stats['workers']}")
```

---

## Notebook 3: Multi-State Comparison (Optional)

### Cell 1: Fetch New York Data
```python
import requests
import json

# Fetch NY 511 WZDx feed
NY_FEED_URL = "https://511ny.org/api/wzdx"

print("Fetching New York work zone data...")
try:
    response = requests.get(NY_FEED_URL, timeout=30)
    response.raise_for_status()
    ny_data = response.json()

    print(f"✓ Successfully fetched New York data")
    print(f"  Total features: {len(ny_data.get('features', []))}")

except Exception as e:
    print(f"❌ Error fetching data: {e}")
    ny_data = None
```

---

### Cell 2: Parse Both States
```python
# Use the same parse function from earlier
ca_zones = parse_work_zones(ca_data)
ny_zones = parse_work_zones(ny_data)

# Add state identifier
for zone in ca_zones:
    zone['state'] = 'California'

for zone in ny_zones:
    zone['state'] = 'New York'

# Combine
all_zones = ca_zones + ny_zones

print(f"✓ Combined data from both states")
print(f"  California: {len(ca_zones)} work zones")
print(f"  New York: {len(ny_zones)} work zones")
print(f"  Total: {len(all_zones)} work zones")

# Create combined DataFrame
df_multi = pd.DataFrame(all_zones)
df_multi.head()
```

---

### Cell 3: Create Comparison Map
```python
# Create map centered on USA
m_compare = folium.Map(
    location=[39.8, -98.6],
    zoom_start=4,
    tiles='OpenStreetMap'
)

# Create state layers
ca_layer = folium.FeatureGroup(name='California (Blue)', show=True)
ny_layer = folium.FeatureGroup(name='New York (Red)', show=True)

# Add California markers (blue)
for zone in ca_zones[:500]:  # Limit for performance
    try:
        folium.Marker(
            location=[zone['latitude'], zone['longitude']],
            popup=f"<b>CA:</b> {zone['road_name']}<br>{zone['vehicle_impact']}",
            tooltip=f"CA: {zone['road_name']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(ca_layer)
    except:
        continue

# Add New York markers (red)
for zone in ny_zones[:500]:  # Limit for performance
    try:
        folium.Marker(
            location=[zone['latitude'], zone['longitude']],
            popup=f"<b>NY:</b> {zone['road_name']}<br>{zone['vehicle_impact']}",
            tooltip=f"NY: {zone['road_name']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(ny_layer)
    except:
        continue

ca_layer.add_to(m_compare)
ny_layer.add_to(m_compare)
folium.LayerControl().add_to(m_compare)

print("✓ Comparison map created")
m_compare
```

---

## Notebook 4: Analysis and Visualizations

### Cell 1: Vehicle Impact Analysis
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Vehicle impact by state (if using multi-state data)
if 'state' in df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # California
    ca_data = df[df['state'] == 'California']
    ca_data['vehicle_impact'].value_counts().plot(kind='bar', ax=axes[0], color='blue', alpha=0.7)
    axes[0].set_title('California - Vehicle Impact Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Impact Type')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)

    # New York
    ny_data = df[df['state'] == 'New York']
    ny_data['vehicle_impact'].value_counts().plot(kind='bar', ax=axes[1], color='red', alpha=0.7)
    axes[1].set_title('New York - Vehicle Impact Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Impact Type')
    axes[1].set_ylabel('Count')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
else:
    # Single state
    df['vehicle_impact'].value_counts().plot(kind='bar', color='steelblue', alpha=0.7)
    plt.title('Vehicle Impact Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Impact Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

---

### Cell 2: Top Roads Analysis
```python
# Top 15 roads by work zone count
top_roads = df['road_name'].value_counts().head(15)

plt.figure(figsize=(12, 6))
top_roads.plot(kind='barh', color='darkgreen', alpha=0.7)
plt.title('Top 15 Roads by Number of Work Zones', fontsize=14, fontweight='bold')
plt.xlabel('Number of Work Zones')
plt.ylabel('Road Name')
plt.tight_layout()
plt.show()

print("\nTop 10 Roads:")
for road, count in top_roads.head(10).items():
    print(f"  {road}: {count}")
```

---

### Cell 3: Duration Analysis (if available)
```python
if df['duration_days'].notna().any():
    # Filter out extreme outliers
    duration_data = df[df['duration_days'].notna() & (df['duration_days'] > 0) & (df['duration_days'] < 365)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(duration_data['duration_days'], bins=30, color='coral', alpha=0.7, edgecolor='black')
    axes[0].set_title('Work Zone Duration Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Duration (days)')
    axes[0].set_ylabel('Frequency')
    axes[0].axvline(duration_data['duration_days'].median(), color='red',
                    linestyle='--', label=f'Median: {duration_data["duration_days"].median():.0f} days')
    axes[0].legend()

    # Box plot
    axes[1].boxplot(duration_data['duration_days'], vert=True)
    axes[1].set_title('Duration Box Plot', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Duration (days)')

    plt.tight_layout()
    plt.show()

    print("\nDuration Statistics:")
    print(f"  Mean: {duration_data['duration_days'].mean():.1f} days")
    print(f"  Median: {duration_data['duration_days'].median():.1f} days")
    print(f"  Min: {duration_data['duration_days'].min():.0f} days")
    print(f"  Max: {duration_data['duration_days'].max():.0f} days")
```

---

## Quick Reference: Complete Single-Cell Version

### All-in-One Cell (for quick demos)
```python
# Complete work zone map in one cell
import folium
import requests
import pandas as pd

# Fetch data
url = "https://api.511.org/traffic/wzdx?api_key=e6f51f24-0f8b-475c-a40c-90732dd41572"
data = requests.get(url).json()

# Create map
m = folium.Map(location=[37.5, -122.0], zoom_start=9)

# Add markers
for feature in data['features'][:100]:  # First 100 for speed
    try:
        coords = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'MultiPoint':
            lat, lon = coords[0][1], coords[0][0]
        else:
            lat, lon = coords[1], coords[0]

        props = feature['properties']
        road = props['core_details']['road_names'][0]
        impact = props.get('vehicle_impact', 'unknown')

        color = 'red' if 'closed' in impact else 'orange' if 'some' in impact else 'blue'

        folium.Marker(
            [lat, lon],
            popup=f"{road}<br>{impact}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    except:
        continue

m  # Display map
```

---

## Tips for Deepnote/Team Collaboration

### 1. Share Data Files
```python
# Export data for team members
df.to_csv('work_zones_data.csv', index=False)
df.to_excel('work_zones_data.xlsx', index=False)  # Requires openpyxl

# Share JSON
with open('ca_wzdx_feed.json', 'w') as f:
    json.dump(ca_data, f, indent=2)
```

### 2. Version Control
```python
# Add metadata to your exports
metadata = {
    'date_fetched': datetime.now().isoformat(),
    'feed_url': CA_FEED_URL,
    'record_count': len(df),
    'version': '1.0'
}

with open('metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

### 3. Notebook Organization
- **Notebook 1**: Data Ingestion (fetch and parse)
- **Notebook 2**: Map Visualization (create maps)
- **Notebook 3**: Analysis (statistics and charts)
- **Notebook 4**: Multi-State Comparison (combine datasets)

### 4. Performance Tips
```python
# For large datasets, sample for initial exploration
df_sample = df.sample(n=100)  # Random 100 work zones

# Or limit markers on map
for zone in work_zones[:500]:  # First 500 only
    # Add marker
```

---

## Environment Setup for Deepnote

### Create requirements.txt
```
folium==0.15.0
pandas==2.1.3
requests==2.31.0
matplotlib==3.8.2
seaborn==0.13.0
```

### Install in Deepnote
```python
!pip install -r requirements.txt
```

---

## Common Issues and Solutions

### Issue 1: Map not displaying
```python
# Make sure the cell returns the map object
m  # Just the variable name at the end of cell
```

### Issue 2: Too many markers (slow)
```python
# Use marker clustering
from folium import plugins

marker_cluster = plugins.MarkerCluster().add_to(m)
# Then add markers to marker_cluster instead of m
```

### Issue 3: API timeout
```python
# Increase timeout and add retry
import time

for attempt in range(3):
    try:
        response = requests.get(url, timeout=60)
        break
    except:
        time.sleep(5)
        continue
```

---

## Next Steps

1. **Copy each cell** into your Deepnote notebook
2. **Run sequentially** from top to bottom
3. **Customize** colors, filters, analysis as needed
4. **Share** with team members via Deepnote sharing

Good luck with your analysis! 🚀
