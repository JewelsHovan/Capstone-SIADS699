"""
Filter utilities for Texas Work Zone Dashboard
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional


def create_filter_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create sidebar filters for work zone data

    Args:
        df: Work zone dataframe

    Returns:
        dict: Filter values selected by user
    """
    st.sidebar.header("🔍 Filters")

    # County filter
    all_counties = sorted(df['CNTY_NM'].dropna().unique().tolist())
    selected_counties = st.sidebar.multiselect(
        "County",
        options=all_counties,
        default=[],
        help="Select one or more counties to filter"
    )

    # Traffic category filter
    traffic_categories = ['very_low', 'low', 'medium', 'high', 'very_high']
    selected_traffic = st.sidebar.multiselect(
        "Traffic Volume Category",
        options=traffic_categories,
        default=[],
        help="Filter by traffic volume level"
    )

    # AADT range slider
    if 'aadt_filled' in df.columns:
        aadt_min = int(df['aadt_filled'].min())
        aadt_max = int(df['aadt_filled'].max())
        selected_aadt_range = st.sidebar.slider(
            "AADT Range",
            min_value=aadt_min,
            max_value=aadt_max,
            value=(aadt_min, aadt_max),
            step=1000,
            help="Filter by traffic volume (vehicles/day)"
        )
    else:
        selected_aadt_range = None

    # Duration range slider
    if 'duration_days' in df.columns:
        duration_min = int(df['duration_days'].min())
        duration_max = int(df['duration_days'].max())
        selected_duration_range = st.sidebar.slider(
            "Duration Range (days)",
            min_value=duration_min,
            max_value=duration_max,
            value=(duration_min, duration_max),
            help="Filter by work zone duration"
        )
    else:
        selected_duration_range = None

    # Vehicle impact filter
    if 'vehicle_impact' in df.columns:
        all_impacts = sorted(df['vehicle_impact'].dropna().unique().tolist())
        selected_impacts = st.sidebar.multiselect(
            "Vehicle Impact",
            options=all_impacts,
            default=[],
            help="Filter by lane closure type"
        )
    else:
        selected_impacts = []

    # Road name search
    road_search = st.sidebar.text_input(
        "Road Name Search",
        value="",
        help="Search for specific road names"
    )

    # Date range filter
    if 'start_date_parsed' in df.columns:
        min_date = df['start_date_parsed'].min()
        max_date = df['start_date_parsed'].max()

        selected_date_range = st.sidebar.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter by work zone start date"
        )
    else:
        selected_date_range = None

    # Reset button
    if st.sidebar.button("Reset Filters", use_container_width=True):
        st.rerun()

    return {
        'counties': selected_counties,
        'traffic_categories': selected_traffic,
        'aadt_range': selected_aadt_range,
        'duration_range': selected_duration_range,
        'vehicle_impacts': selected_impacts,
        'road_search': road_search,
        'date_range': selected_date_range
    }


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply filters to dataframe

    Args:
        df: Work zone dataframe
        filters: Dictionary of filter values from create_filter_sidebar

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()

    # County filter
    if filters.get('counties'):
        filtered_df = filtered_df[filtered_df['CNTY_NM'].isin(filters['counties'])]

    # Traffic category filter
    if filters.get('traffic_categories'):
        filtered_df = filtered_df[
            filtered_df['traffic_volume_category'].isin(filters['traffic_categories'])
        ]

    # AADT range filter
    if filters.get('aadt_range') and 'aadt_filled' in filtered_df.columns:
        min_aadt, max_aadt = filters['aadt_range']
        filtered_df = filtered_df[
            (filtered_df['aadt_filled'] >= min_aadt) &
            (filtered_df['aadt_filled'] <= max_aadt)
        ]

    # Duration range filter
    if filters.get('duration_range') and 'duration_days' in filtered_df.columns:
        min_dur, max_dur = filters['duration_range']
        filtered_df = filtered_df[
            (filtered_df['duration_days'] >= min_dur) &
            (filtered_df['duration_days'] <= max_dur)
        ]

    # Vehicle impact filter
    if filters.get('vehicle_impacts') and 'vehicle_impact' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['vehicle_impact'].isin(filters['vehicle_impacts'])
        ]

    # Road name search
    if filters.get('road_search'):
        search_term = filters['road_search'].lower()
        if 'road_name' in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df['road_name'].str.lower().str.contains(search_term, na=False)
            ]

    # Date range filter
    if filters.get('date_range') and 'start_date_parsed' in filtered_df.columns:
        if len(filters['date_range']) == 2:
            start_date, end_date = filters['date_range']
            filtered_df = filtered_df[
                (filtered_df['start_date_parsed'] >= pd.Timestamp(start_date)) &
                (filtered_df['start_date_parsed'] <= pd.Timestamp(end_date))
            ]

    return filtered_df


def get_filter_summary(original_count: int, filtered_count: int) -> str:
    """
    Generate a summary string of filter results

    Args:
        original_count: Number of records before filtering
        filtered_count: Number of records after filtering

    Returns:
        str: Summary message
    """
    if filtered_count == original_count:
        return f"Showing all **{original_count:,}** work zones"
    else:
        percentage = (filtered_count / original_count) * 100 if original_count > 0 else 0
        return f"Showing **{filtered_count:,}** of **{original_count:,}** work zones ({percentage:.1f}%)"


def initialize_session_state():
    """
    Initialize session state variables for filter persistence
    """
    if 'filters_applied' not in st.session_state:
        st.session_state.filters_applied = False

    if 'last_filter_count' not in st.session_state:
        st.session_state.last_filter_count = 0
