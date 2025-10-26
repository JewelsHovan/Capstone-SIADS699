"""
Texas Work Zone Dashboard - Data Explorer Page
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_work_zones, calculate_filtered_stats
from utils.filters import create_filter_sidebar, apply_filters, get_filter_summary
from config import PAGE_CONFIG, DISPLAY_COLUMNS, COLUMN_RENAME

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Title
st.title("📥 Data Explorer")
st.markdown("Browse, filter, and export the complete work zone dataset")
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

# Display filtered statistics
if len(filtered_df) > 0:
    col1, col2, col3, col4 = st.columns(4)
    filtered_stats = calculate_filtered_stats(filtered_df)

    with col1:
        st.metric("Work Zones", f"{filtered_stats['count']:,}")

    with col2:
        st.metric("Counties", f"{filtered_stats['counties']}")

    with col3:
        st.metric("Mean AADT", f"{filtered_stats['mean_aadt']:,.0f}")

    with col4:
        st.metric("Total VMT", f"{filtered_stats['total_vmt']/1e6:.1f}M")
else:
    st.warning("No work zones match the selected filters. Please adjust your filter criteria.")
    st.stop()

st.markdown("---")

# Column selection
st.subheader("📋 Column Selection")

col1, col2 = st.columns([2, 1])

with col1:
    # Get available display columns that exist in the dataframe
    available_display_cols = [col for col in DISPLAY_COLUMNS if col in filtered_df.columns]

    selected_columns = st.multiselect(
        "Select columns to display",
        options=filtered_df.columns.tolist(),
        default=available_display_cols,
        help="Choose which columns to show in the table"
    )

with col2:
    # Quick selection buttons
    if st.button("Select All Columns", use_container_width=True):
        selected_columns = filtered_df.columns.tolist()
        st.rerun()

    if st.button("Reset to Default", use_container_width=True):
        selected_columns = available_display_cols
        st.rerun()

st.markdown("---")

# Data table
st.subheader("📊 Data Table")

if selected_columns:
    # Prepare display dataframe
    display_df = filtered_df[selected_columns].copy()

    # Format numeric columns for better readability
    format_dict = {}
    for col in display_df.columns:
        if col in ['aadt_filled', 'vehicle_miles_traveled']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        elif col in ['duration_days']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.0f}" if pd.notna(x) else "N/A")
        elif col in ['exposure_score', 'lane_closure_risk']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        elif col in ['latitude', 'longitude']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.6f}" if pd.notna(x) else "N/A")

    # Rename columns for display
    display_df = display_df.rename(columns={col: COLUMN_RENAME.get(col, col) for col in display_df.columns})

    # Display with search and sorting
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500,
        hide_index=True
    )

    # Show record count
    st.caption(f"Showing {len(display_df):,} records")
else:
    st.info("Please select at least one column to display")

st.markdown("---")

# Export section
st.subheader("💾 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📄 CSV Export")
    st.markdown("Download filtered data as CSV file")

    export_format = st.radio(
        "Export format",
        ["All columns", "Selected columns only"],
        help="Choose which columns to include in export"
    )

    if export_format == "All columns":
        export_df = filtered_df
    else:
        if selected_columns:
            export_df = filtered_df[selected_columns]
        else:
            export_df = filtered_df

    csv = export_df.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"texas_work_zones_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download the filtered dataset"
    )

with col2:
    st.markdown("### 📊 Export Summary")
    st.markdown(f"**Records**: {len(export_df):,}")
    st.markdown(f"**Columns**: {len(export_df.columns)}")
    st.markdown(f"**File size**: ~{len(csv) / 1024:.0f} KB")
    st.markdown(f"**Date range**: {filtered_df['start_date_parsed'].min().strftime('%Y-%m-%d')} to {filtered_df['end_date_parsed'].max().strftime('%Y-%m-%d')}")

with col3:
    st.markdown("### 📋 Quick Stats")
    st.markdown(f"**Counties**: {filtered_df['CNTY_NM'].nunique()}")
    st.markdown(f"**Mean AADT**: {filtered_df['aadt_filled'].mean():,.0f}")
    st.markdown(f"**Mean Duration**: {filtered_df['duration_days'].mean():.1f} days")

    if 'traffic_volume_category' in filtered_df.columns:
        high_risk = (filtered_df['traffic_volume_category'] == 'very_high').sum()
        st.markdown(f"**High Risk Zones**: {high_risk:,}")

st.markdown("---")

# Data summary section
st.subheader("📈 Data Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🗺️ Geographic Distribution")
    if 'CNTY_NM' in filtered_df.columns:
        top_counties = filtered_df['CNTY_NM'].value_counts().head(10)
        st.markdown("**Top 10 Counties:**")
        for county, count in top_counties.items():
            percentage = (count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"- {county}: {count:,} ({percentage:.1f}%)")

with col2:
    st.markdown("### 🚗 Traffic Distribution")
    if 'traffic_volume_category' in filtered_df.columns:
        traffic_dist = filtered_df['traffic_volume_category'].value_counts()

        from config import TRAFFIC_LABELS

        st.markdown("**By Traffic Category:**")
        for cat in ['very_high', 'high', 'medium', 'low', 'very_low']:
            count = traffic_dist.get(cat, 0)
            percentage = (count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"- {TRAFFIC_LABELS.get(cat, cat)}: {count:,} ({percentage:.1f}%)")

st.markdown("---")

# Additional data info
st.subheader("ℹ️ Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 Available Fields")
    st.markdown(f"**Total columns**: {len(filtered_df.columns)}")

    # Group columns by category
    location_cols = [col for col in filtered_df.columns if any(x in col.lower() for x in ['lat', 'lon', 'county', 'dist'])]
    temporal_cols = [col for col in filtered_df.columns if any(x in col.lower() for x in ['date', 'duration', 'time'])]
    traffic_cols = [col for col in filtered_df.columns if any(x in col.lower() for x in ['aadt', 'traffic', 'exposure', 'vmt'])]
    workzone_cols = [col for col in filtered_df.columns if any(x in col.lower() for x in ['road', 'lane', 'vehicle', 'impact', 'event'])]

    if location_cols:
        st.markdown(f"- **Location fields**: {len(location_cols)}")
    if temporal_cols:
        st.markdown(f"- **Temporal fields**: {len(temporal_cols)}")
    if traffic_cols:
        st.markdown(f"- **Traffic fields**: {len(traffic_cols)}")
    if workzone_cols:
        st.markdown(f"- **Work zone fields**: {len(workzone_cols)}")

with col2:
    st.markdown("### 📊 Data Completeness")

    # Calculate completeness for key fields
    key_fields = ['aadt_filled', 'duration_days', 'CNTY_NM', 'latitude', 'longitude']
    available_key_fields = [f for f in key_fields if f in filtered_df.columns]

    for field in available_key_fields:
        completeness = (filtered_df[field].notna().sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.markdown(f"- **{field}**: {completeness:.1f}%")

st.markdown("---")

# Search functionality
st.subheader("🔍 Advanced Search")

col1, col2 = st.columns([3, 1])

with col1:
    search_term = st.text_input(
        "Search in any column",
        placeholder="Enter search term...",
        help="Search across all text columns in the filtered dataset"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    case_sensitive = st.checkbox("Case sensitive", value=False)

if search_term:
    # Search across all string columns
    mask = pd.Series([False] * len(filtered_df))

    for col in filtered_df.columns:
        if filtered_df[col].dtype == 'object':
            if case_sensitive:
                mask |= filtered_df[col].astype(str).str.contains(search_term, na=False)
            else:
                mask |= filtered_df[col].astype(str).str.lower().str.contains(search_term.lower(), na=False)

    search_results = filtered_df[mask]

    st.markdown(f"**Found {len(search_results):,} matching records**")

    if len(search_results) > 0:
        # Show search results
        available_display_cols = [col for col in DISPLAY_COLUMNS if col in search_results.columns]
        display_search_df = search_results[available_display_cols].copy()

        # Apply same formatting as main table
        for col in display_search_df.columns:
            if col in ['aadt_filled', 'vehicle_miles_traveled']:
                display_search_df[col] = display_search_df[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
            elif col in ['duration_days']:
                display_search_df[col] = display_search_df[col].apply(lambda x: f"{x:.0f}" if pd.notna(x) else "N/A")
            elif col in ['exposure_score']:
                display_search_df[col] = display_search_df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")

        display_search_df = display_search_df.rename(columns={col: COLUMN_RENAME.get(col, col) for col in display_search_df.columns})

        st.dataframe(display_search_df, use_container_width=True, hide_index=True, height=300)

        # Export search results
        csv_search = search_results.to_csv(index=False)
        st.download_button(
            label="📥 Download Search Results",
            data=csv_search,
            file_name=f"texas_work_zones_search_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
