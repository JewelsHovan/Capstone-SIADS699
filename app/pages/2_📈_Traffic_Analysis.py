"""
Texas Work Zone Dashboard - Traffic Analysis Page
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_work_zones
from utils.charts import (
    create_aadt_histogram,
    create_aadt_boxplot,
    create_traffic_pie_chart,
    create_scatter_plot,
    create_duration_histogram,
    create_top_exposure_table
)
from config import PAGE_CONFIG, TRAFFIC_COLORS, TRAFFIC_LABELS

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Title
st.title("📈 Traffic Analysis")
st.markdown("Deep dive into AADT traffic volumes and exposure metrics")
st.markdown("---")

# Load data
try:
    df = load_work_zones()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Key metrics
st.subheader("🚗 Traffic Volume Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Mean AADT", f"{df['aadt_filled'].mean():,.0f}", help="Average traffic volume")

with col2:
    st.metric("Median AADT", f"{df['aadt_filled'].median():,.0f}", help="Middle value traffic volume")

with col3:
    st.metric("Max AADT", f"{df['aadt_filled'].max():,.0f}", help="Highest traffic volume")

with col4:
    st.metric("Min AADT", f"{df['aadt_filled'].min():,.0f}", help="Lowest traffic volume")

st.markdown("---")

# AADT Distribution Section
st.subheader("📊 AADT Distribution")

col1, col2 = st.columns(2)

with col1:
    # Histogram
    st.plotly_chart(
        create_aadt_histogram(df, title="AADT Distribution with Mean/Median"),
        use_container_width=True,
        key="traffic_aadt_hist"
    )

with col2:
    # Box plot by category
    st.plotly_chart(
        create_aadt_boxplot(df, title="AADT by Traffic Category"),
        use_container_width=True,
        key="traffic_aadt_box"
    )

st.markdown("---")

# Traffic Categories Section
st.subheader("🚦 Traffic Volume Categories")

col1, col2 = st.columns([1, 2])

with col1:
    # Pie chart
    st.plotly_chart(
        create_traffic_pie_chart(df, title="Distribution by Category"),
        use_container_width=True,
        key="traffic_pie"
    )

with col2:
    # Category breakdown table
    st.markdown("### Category Details")

    if 'traffic_volume_category' in df.columns:
        category_stats = []

        for cat in ['very_high', 'high', 'medium', 'low', 'very_low']:
            cat_df = df[df['traffic_volume_category'] == cat]
            count = len(cat_df)
            percentage = (count / len(df) * 100) if len(df) > 0 else 0

            if count > 0:
                mean_aadt = cat_df['aadt_filled'].mean()
                min_aadt = cat_df['aadt_filled'].min()
                max_aadt = cat_df['aadt_filled'].max()
            else:
                mean_aadt = min_aadt = max_aadt = 0

            category_stats.append({
                'Category': TRAFFIC_LABELS.get(cat, cat),
                'Count': count,
                'Percentage': f"{percentage:.1f}%",
                'Mean AADT': f"{mean_aadt:,.0f}",
                'Range': f"{min_aadt:,.0f} - {max_aadt:,.0f}"
            })

        stats_df = pd.DataFrame(category_stats)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

st.markdown("---")

# Duration Analysis
st.subheader("⏱️ Duration Analysis")

col1, col2 = st.columns(2)

with col1:
    # Duration histogram
    st.plotly_chart(
        create_duration_histogram(df, title="Work Zone Duration Distribution"),
        use_container_width=True,
        key="traffic_duration_hist"
    )

with col2:
    # Duration statistics
    st.markdown("### Duration Statistics")
    st.markdown(f"**Mean Duration**: {df['duration_days'].mean():.1f} days")
    st.markdown(f"**Median Duration**: {df['duration_days'].median():.1f} days")
    st.markdown(f"**Max Duration**: {df['duration_days'].max():.0f} days")
    st.markdown(f"**Min Duration**: {df['duration_days'].min():.0f} days")

    # Duration by category
    st.markdown("### Mean Duration by Traffic Category")
    if 'traffic_volume_category' in df.columns:
        for cat in ['very_high', 'high', 'medium', 'low', 'very_low']:
            cat_df = df[df['traffic_volume_category'] == cat]
            if len(cat_df) > 0:
                mean_dur = cat_df['duration_days'].mean()
                st.markdown(f"- **{TRAFFIC_LABELS.get(cat, cat)}**: {mean_dur:.1f} days")

st.markdown("---")

# Exposure Analysis Section
st.subheader("🎯 Exposure Analysis")
st.markdown("Exposure score combines AADT and duration to measure traffic exposure risk")

# Scatter plot
st.plotly_chart(
    create_scatter_plot(
        df,
        x_col='duration_days',
        y_col='aadt_filled',
        size_col='exposure_score',
        color_col='traffic_volume_category',
        title="AADT vs Duration (size = exposure score)"
    ),
    use_container_width=True,
    key="traffic_scatter"
)

st.markdown("---")

# Top Exposure Zones
st.subheader("🔝 Top 10 Highest Exposure Work Zones")

top_exposure_df = create_top_exposure_table(df, top_n=10)

if not top_exposure_df.empty:
    st.dataframe(top_exposure_df, use_container_width=True, hide_index=True)
else:
    st.warning("Exposure score data not available")

st.markdown("---")

# Match Quality Section
st.subheader("✅ AADT Data Quality")

col1, col2, col3 = st.columns(3)

if 'aadt_source' in df.columns:
    matched = (df['aadt_source'] == 'matched').sum()
    county_avg = (df['aadt_source'] == 'county_avg').sum()
    state_median = (df['aadt_source'] == 'state_median').sum()
    match_rate = matched / len(df) if len(df) > 0 else 0

    with col1:
        st.metric("Direct Matches", f"{matched:,}", help="Work zones with direct AADT match")
        st.metric("Match Rate", f"{match_rate:.1%}", help="Percentage of direct matches")

    with col2:
        st.metric("County Average", f"{county_avg:,}", help="Filled with county average AADT")
        st.metric("State Median", f"{state_median:,}", help="Filled with state median AADT")

    with col3:
        st.markdown("### Data Source Breakdown")
        source_dist = df['aadt_source'].value_counts()
        for source, count in source_dist.items():
            percentage = (count / len(df) * 100) if len(df) > 0 else 0
            st.markdown(f"- **{source.replace('_', ' ').title()}**: {count:,} ({percentage:.1f}%)")
else:
    st.info("AADT source information not available in dataset")

# Distance to station stats
if 'distance_to_station_m' in df.columns:
    matched_df = df[df['aadt_source'] == 'matched']

    if len(matched_df) > 0:
        st.markdown("---")
        st.subheader("📍 Spatial Match Quality")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Mean Distance", f"{matched_df['distance_to_station_m'].mean():.0f}m",
                     help="Average distance to nearest AADT station")

        with col2:
            st.metric("Median Distance", f"{matched_df['distance_to_station_m'].median():.0f}m",
                     help="Middle value distance to station")

        with col3:
            st.metric("Max Distance", f"{matched_df['distance_to_station_m'].max():.0f}m",
                     help="Farthest matched station")

        with col4:
            within_100m = (matched_df['distance_to_station_m'] <= 100).sum()
            pct_within_100m = (within_100m / len(matched_df) * 100) if len(matched_df) > 0 else 0
            st.metric("Within 100m", f"{pct_within_100m:.1f}%",
                     help="Percentage of matches within 100 meters")

st.markdown("---")

# Additional insights
st.subheader("💡 Key Insights")

# Calculate insights
high_traffic = df[df['traffic_volume_category'] == 'very_high']
long_duration = df[df['duration_days'] > df['duration_days'].quantile(0.75)]

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px;">', unsafe_allow_html=True)
    st.markdown("### 🚗 High Traffic Zones")
    st.markdown(f"- **{len(high_traffic):,}** zones with very high traffic (>30K AADT)")
    st.markdown(f"- **{(len(high_traffic)/len(df)*100):.1f}%** of all work zones")

    if len(high_traffic) > 0:
        st.markdown(f"- Mean duration: **{high_traffic['duration_days'].mean():.0f} days**")
        if 'CNTY_NM' in high_traffic.columns:
            top_county = high_traffic['CNTY_NM'].value_counts().index[0]
            top_count = high_traffic['CNTY_NM'].value_counts().iloc[0]
            st.markdown(f"- Top county: **{top_county}** ({top_count} zones)")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px;">', unsafe_allow_html=True)
    st.markdown("### ⏱️ Long Duration Zones")
    st.markdown(f"- **{len(long_duration):,}** zones in top 25% duration")
    st.markdown(f"- Duration threshold: **>{df['duration_days'].quantile(0.75):.0f} days**")

    if len(long_duration) > 0:
        st.markdown(f"- Mean AADT: **{long_duration['aadt_filled'].mean():,.0f}**")
        if 'CNTY_NM' in long_duration.columns:
            top_county = long_duration['CNTY_NM'].value_counts().index[0]
            top_count = long_duration['CNTY_NM'].value_counts().iloc[0]
            st.markdown(f"- Top county: **{top_county}** ({top_count} zones)")
    st.markdown('</div>', unsafe_allow_html=True)
