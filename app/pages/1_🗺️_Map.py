"""
Texas Work Zone Dashboard - Interactive Map Page
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils.data_loader import load_work_zones, calculate_filtered_stats
from utils.filters import create_filter_sidebar, apply_filters, get_filter_summary
from config import PAGE_CONFIG, TRAFFIC_COLORS, TRAFFIC_LABELS, MAP_CENTER, MAP_ZOOM

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Title
st.title("🗺️ Interactive Work Zone Map")
st.markdown("Explore Texas work zones geographically with interactive filtering")
st.markdown("---")

# Load data
try:
    df = load_work_zones()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar filters
filters = create_filter_sidebar(df)

# Apply filters
filtered_df = apply_filters(df, filters)

# Filter summary
st.markdown(f"### {get_filter_summary(len(df), len(filtered_df))}")

# Check if we have data to display
if len(filtered_df) == 0:
    st.warning("No work zones match the selected filters. Please adjust your filter criteria.")
    st.stop()

# Display filtered statistics
col1, col2, col3, col4 = st.columns(4)
filtered_stats = calculate_filtered_stats(filtered_df)

with col1:
    st.metric("Work Zones", f"{filtered_stats['count']:,}")

with col2:
    st.metric("Counties", f"{filtered_stats['counties']}")

with col3:
    st.metric("Mean AADT", f"{filtered_stats['mean_aadt']:,.0f}")

with col4:
    st.metric("Median Duration", f"{filtered_stats['median_duration']:.0f} days")

st.markdown("---")

# Map settings
st.markdown("### 🗺️ Map View")

# Map options
col1, col2 = st.columns([3, 1])

with col2:
    use_clusters = st.checkbox("Use marker clusters", value=True, help="Group nearby markers for better performance")
    show_all = st.checkbox("Show all zones", value=False, help="Display all work zones regardless of filters")

# Use all data or filtered data
map_df = df if show_all else filtered_df

# Create map
m = folium.Map(
    location=MAP_CENTER,
    zoom_start=MAP_ZOOM,
    tiles='OpenStreetMap',
    control_scale=True
)

# Add marker cluster if requested
if use_clusters:
    marker_cluster = MarkerCluster().add_to(m)
    container = marker_cluster
else:
    container = m

# Add markers
for idx, row in map_df.iterrows():
    # Skip if missing coordinates
    if pd.isna(row['latitude']) or pd.isna(row['longitude']):
        continue

    # Get color based on traffic category
    traffic_cat = row.get('traffic_volume_category', 'medium')
    color = TRAFFIC_COLORS.get(traffic_cat, '#808080')

    # Create popup content
    popup_html = f"""
    <div style="font-family: Arial; font-size: 12px; width: 250px;">
        <h4 style="margin: 0 0 10px 0; color: {color};">{row.get('road_name', 'Unknown Road')}</h4>
        <hr style="margin: 5px 0;">
        <b>Traffic:</b> {row.get('aadt_filled', 0):,.0f} AADT<br>
        <b>Category:</b> {TRAFFIC_LABELS.get(traffic_cat, traffic_cat)}<br>
        <b>Duration:</b> {row.get('duration_days', 0):.0f} days<br>
        <b>Exposure Score:</b> {row.get('exposure_score', 0):.2f}<br>
        <b>County:</b> {row.get('CNTY_NM', 'Unknown')}<br>
        <b>Vehicle Impact:</b> {row.get('vehicle_impact', 'Unknown')}<br>
        <b>Lanes:</b> {row.get('total_num_lanes', 'N/A')}<br>
        <hr style="margin: 5px 0;">
        <small><b>Event ID:</b> {row.get('road_event_id', 'N/A')}</small>
    </div>
    """

    # Add marker
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=6 if not use_clusters else 8,
        popup=folium.Popup(popup_html, max_width=300),
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7,
        weight=2
    ).add_to(container)

# Add legend
legend_html = f"""
<div style="position: fixed;
     bottom: 50px; right: 50px; width: 200px; height: auto;
     background-color: white; z-index:9999; font-size:12px;
     border:2px solid grey; border-radius: 5px; padding: 10px;
     box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">

<h4 style="margin: 0 0 10px 0;">Traffic Volume</h4>
"""

for cat in ['very_high', 'high', 'medium', 'low', 'very_low']:
    color = TRAFFIC_COLORS.get(cat, '#808080')
    label = TRAFFIC_LABELS.get(cat, cat)
    legend_html += f'<p style="margin: 5px 0;"><span style="background-color:{color}; width: 15px; height: 15px; display: inline-block; border-radius: 50%; margin-right: 8px;"></span>{label}</p>'

legend_html += "</div>"

# Display map
st_folium(m, width=1400, height=600, returned_objects=[])

# Add legend below map
st.markdown(legend_html, unsafe_allow_html=True)

st.markdown("---")

# Additional stats
st.markdown("### 📊 Filtered Data Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Traffic Volume Breakdown**")
    if 'traffic_volume_category' in filtered_df.columns:
        traffic_dist = filtered_df['traffic_volume_category'].value_counts()
        for cat in ['very_high', 'high', 'medium', 'low', 'very_low']:
            count = traffic_dist.get(cat, 0)
            percentage = (count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"- **{TRAFFIC_LABELS.get(cat, cat)}**: {count:,} ({percentage:.1f}%)")

with col2:
    st.markdown("**Top Counties (Filtered)**")
    if 'CNTY_NM' in filtered_df.columns:
        top_counties = filtered_df['CNTY_NM'].value_counts().head(5)
        for county, count in top_counties.items():
            percentage = (count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"- **{county}**: {count:,} ({percentage:.1f}%)")

# Export option
st.markdown("---")
st.markdown("### 💾 Export Filtered Data")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Download CSV", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download",
            data=csv,
            file_name="texas_work_zones_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

with col2:
    st.info(f"Export {len(filtered_df):,} filtered work zones to CSV format")
