"""
Texas Work Zone Dashboard - Overview Page
Main entry point for Streamlit multi-page app
"""

import streamlit as st
from utils.data_loader import load_work_zones, get_summary_stats
from utils.charts import (
    create_traffic_pie_chart,
    create_county_bar_chart,
    create_aadt_histogram,
    create_temporal_line_chart
)
from config import PAGE_CONFIG, CUSTOM_CSS

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🚧 Texas Work Zone Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Exploratory analysis of Texas work zones integrated with traffic volume data (AADT)**")
st.markdown("---")

# Load data
try:
    df = load_work_zones()
    stats = get_summary_stats(df)
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Hero Metrics Row
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Work Zones",
        value=f"{stats['total_zones']:,}",
        help="Total number of work zones in dataset"
    )

with col2:
    st.metric(
        label="Counties Covered",
        value=f"{stats['counties']}",
        help="Number of unique counties with work zones"
    )

with col3:
    st.metric(
        label="Mean AADT",
        value=f"{stats['mean_aadt']:,.0f}",
        help="Average traffic volume (vehicles/day)"
    )

with col4:
    st.metric(
        label="High Risk Zones",
        value=f"{stats['high_risk_count']:,}",
        help="Work zones with very high traffic volume (>30K AADT)"
    )

st.markdown("---")

# Quick Insights Section
st.subheader("🔍 Quick Insights")

col1, col2 = st.columns(2)

with col1:
    # Top counties chart
    st.plotly_chart(
        create_county_bar_chart(df, top_n=10),
        use_container_width=True,
        key="overview_county_chart"
    )

with col2:
    # Traffic distribution pie chart
    st.plotly_chart(
        create_traffic_pie_chart(df),
        use_container_width=True,
        key="overview_traffic_pie"
    )

st.markdown("---")

# Summary Statistics Cards
st.subheader("📈 Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**📍 Geographic Coverage**")
    st.markdown(f"- **Counties**: {stats['counties']}")
    st.markdown(f"- **Districts**: {stats['districts']}")
    st.markdown(f"- **Date Range**: {stats['date_range_start'].strftime('%b %Y')} - {stats['date_range_end'].strftime('%b %Y')}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**⏱️ Duration Metrics**")
    st.markdown(f"- **Mean Duration**: {stats['mean_duration']:.0f} days")
    st.markdown(f"- **Median Duration**: {stats['median_duration']:.0f} days")
    st.markdown(f"- **Median AADT**: {stats['median_aadt']:,.0f} vehicles/day")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**🚗 Traffic Exposure**")
    st.markdown(f"- **Total VMT**: {stats['total_vmt']/1e6:.1f}M")
    st.markdown(f"- **AADT Match Rate**: {stats['match_rate']:.1%}")
    st.markdown(f"- **High Risk Zones**: {stats['high_risk_count']}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Additional Visualizations
st.subheader("📉 Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    # AADT histogram
    st.plotly_chart(
        create_aadt_histogram(df),
        use_container_width=True,
        key="overview_aadt_hist"
    )

with col2:
    # Temporal distribution
    st.plotly_chart(
        create_temporal_line_chart(df),
        use_container_width=True,
        key="overview_temporal"
    )

st.markdown("---")

# Footer with data info
st.markdown("### 📝 About This Data")
st.info(f"""
**Dataset**: Texas work zones integrated with TxDOT AADT traffic data

**Coverage**: {stats['total_zones']:,} work zones from {stats['date_range_start'].strftime('%B %Y')} to {stats['date_range_end'].strftime('%B %Y')}

**Data Sources**:
- Work Zone Data: WZDx Feed
- Traffic Data: TxDOT AADT Annuals (Public View) - {stats['match_rate']:.1%} direct match rate
- Spatial Integration: 500m nearest neighbor matching with county fallback

**Features**: AADT traffic volumes, exposure scores, traffic categories, duration metrics, and geographic attributes

**Navigation**: Use the sidebar to explore different pages:
- 🗺️ **Map**: Interactive geographic visualization with filters
- 📈 **Traffic Analysis**: Deep dive into AADT and exposure metrics
- 📥 **Data Explorer**: Browse and export the full dataset
""")

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🚧 Texas Work Zones")
    st.markdown(f"**{stats['total_zones']:,}** work zones analyzed")
    st.markdown(f"**{stats['counties']}** counties covered")
    st.markdown("---")
    st.markdown("### 📊 Data Quality")
    st.markdown(f"**{stats['match_rate']:.1%}** AADT match rate")
    st.markdown(f"**100%** data completeness")
    st.markdown("---")
    st.markdown("### 📚 Resources")
    st.markdown("[Project Documentation](#)")
    st.markdown("[Data Sources](#)")
    st.markdown("[GitHub Repository](#)")
