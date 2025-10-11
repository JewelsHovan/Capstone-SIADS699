import streamlit as st
import os
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Work Zone Map Viewer",
    page_icon="🚧",
    layout="wide"
)

# Title and description
st.title("🚧 Work Zone Interactive Map Viewer")
st.markdown("Explore work zone data for Texas and California")

# Define the maps directory
maps_dir = Path("outputs/maps")

# Map selection
map_options = {
    "Texas Work Zones": "texas_workzones_map.html",
    "California Work Zones": "california_work_zones_map.html"
}

# Create a selectbox for choosing the map
selected_map = st.selectbox(
    "Select a state to view:",
    options=list(map_options.keys()),
    index=0
)

# Load and display the selected map
map_file = maps_dir / map_options[selected_map]

if map_file.exists():
    # Read the HTML file
    with open(map_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Display the map using an iframe
    st.components.v1.html(html_content, height=700, scrolling=True)

    # Add some statistics or information
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**Map:** {selected_map}")

    with col2:
        file_size = os.path.getsize(map_file) / (1024 * 1024)  # Convert to MB
        st.info(f"**File Size:** {file_size:.2f} MB")

else:
    st.error(f"Map file not found: {map_file}")
    st.info("Please ensure the map files are in the 'outputs/maps' directory")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    Interactive maps generated from work zone and crash data
    </div>
    """,
    unsafe_allow_html=True
)
