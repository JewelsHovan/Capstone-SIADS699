"""
Data loading utilities with caching for Texas Work Zone Dashboard
"""

import streamlit as st
import pandas as pd
from config import DATA_PATH


@st.cache_data
def load_work_zones():
    """
    Load and prepare work zone data with caching

    Returns:
        pd.DataFrame: Work zone data
    """
    df = pd.read_csv(DATA_PATH)

    # Convert date columns
    df['start_date_parsed'] = pd.to_datetime(df['start_date_parsed'], errors='coerce')
    df['end_date_parsed'] = pd.to_datetime(df['end_date_parsed'], errors='coerce')

    # Ensure numeric columns
    numeric_cols = ['aadt_filled', 'duration_days', 'exposure_score',
                    'vehicle_miles_traveled', 'lane_closure_risk']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


@st.cache_data
def get_summary_stats(df):
    """
    Calculate summary statistics

    Args:
        df: Work zone dataframe

    Returns:
        dict: Summary statistics
    """
    return {
        'total_zones': len(df),
        'counties': df['CNTY_NM'].nunique(),
        'districts': df['DIST_NM'].nunique() if 'DIST_NM' in df.columns else 0,
        'mean_aadt': df['aadt_filled'].mean(),
        'median_aadt': df['aadt_filled'].median(),
        'median_duration': df['duration_days'].median(),
        'mean_duration': df['duration_days'].mean(),
        'total_vmt': df['vehicle_miles_traveled'].sum() if 'vehicle_miles_traveled' in df.columns else 0,
        'match_rate': (df['aadt_source'] == 'matched').sum() / len(df) if 'aadt_source' in df.columns else 0,
        'high_risk_count': (df['traffic_volume_category'] == 'very_high').sum() if 'traffic_volume_category' in df.columns else 0,
        'date_range_start': df['start_date_parsed'].min(),
        'date_range_end': df['end_date_parsed'].max()
    }


@st.cache_data
def get_county_list(df):
    """Get sorted list of counties"""
    return sorted(df['CNTY_NM'].dropna().unique().tolist())


@st.cache_data
def get_road_list(df):
    """Get sorted list of roads"""
    return sorted(df['road_name'].dropna().unique().tolist())


@st.cache_data
def get_traffic_categories():
    """Get traffic volume categories in order"""
    return ['very_low', 'low', 'medium', 'high', 'very_high']


@st.cache_data
def get_vehicle_impacts(df):
    """Get unique vehicle impact types"""
    return sorted(df['vehicle_impact'].dropna().unique().tolist())


def calculate_filtered_stats(df):
    """
    Calculate statistics for filtered dataframe (not cached)

    Args:
        df: Filtered work zone dataframe

    Returns:
        dict: Statistics
    """
    if len(df) == 0:
        return {
            'count': 0,
            'mean_aadt': 0,
            'median_duration': 0,
            'total_vmt': 0
        }

    return {
        'count': len(df),
        'mean_aadt': df['aadt_filled'].mean(),
        'median_aadt': df['aadt_filled'].median(),
        'median_duration': df['duration_days'].median(),
        'mean_duration': df['duration_days'].mean(),
        'total_vmt': df['vehicle_miles_traveled'].sum() if 'vehicle_miles_traveled' in df.columns else 0,
        'counties': df['CNTY_NM'].nunique()
    }
