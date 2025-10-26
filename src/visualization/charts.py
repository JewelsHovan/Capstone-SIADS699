"""
Chart utilities for Texas Work Zone Dashboard
Reusable Plotly chart functions
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import TRAFFIC_COLORS, TRAFFIC_LABELS, CHART_COLORS, PLOTLY_THEME


def create_traffic_pie_chart(df: pd.DataFrame, title: str = "Work Zones by Traffic Volume") -> go.Figure:
    """
    Create pie chart showing distribution of traffic volume categories

    Args:
        df: Work zone dataframe
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if 'traffic_volume_category' not in df.columns:
        return go.Figure()

    # Count by category
    category_counts = df['traffic_volume_category'].value_counts()

    # Ensure all categories are present
    all_categories = ['very_low', 'low', 'medium', 'high', 'very_high']
    for cat in all_categories:
        if cat not in category_counts:
            category_counts[cat] = 0

    # Sort by category order
    category_counts = category_counts.reindex(all_categories, fill_value=0)

    # Create labels with counts
    labels = [f"{TRAFFIC_LABELS.get(cat, cat)}<br>({count:,} zones)"
              for cat, count in category_counts.items()]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=category_counts.values,
        marker=dict(colors=[TRAFFIC_COLORS.get(cat, '#cccccc') for cat in category_counts.index]),
        hole=0.3,
        textinfo='percent',
        hovertemplate='%{label}<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        title=title,
        template=PLOTLY_THEME,
        showlegend=True,
        height=400
    )

    return fig


def create_county_bar_chart(df: pd.DataFrame, top_n: int = 10, title: str = "Top Counties by Work Zone Count") -> go.Figure:
    """
    Create bar chart showing top counties by work zone count

    Args:
        df: Work zone dataframe
        top_n: Number of top counties to show
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if 'CNTY_NM' not in df.columns:
        return go.Figure()

    # Count by county
    county_counts = df['CNTY_NM'].value_counts().head(top_n)

    fig = go.Figure(data=[go.Bar(
        x=county_counts.values,
        y=county_counts.index,
        orientation='h',
        marker=dict(color=CHART_COLORS[0]),
        text=county_counts.values,
        textposition='outside',
        hovertemplate='%{y}<br>%{x:,} work zones<extra></extra>'
    )])

    fig.update_layout(
        title=title,
        xaxis_title="Number of Work Zones",
        yaxis_title="",
        template=PLOTLY_THEME,
        height=400,
        yaxis=dict(autorange="reversed")
    )

    return fig


def create_aadt_histogram(df: pd.DataFrame, title: str = "AADT Distribution") -> go.Figure:
    """
    Create histogram showing AADT distribution with mean/median lines

    Args:
        df: Work zone dataframe
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if 'aadt_filled' not in df.columns:
        return go.Figure()

    # Calculate statistics
    mean_aadt = df['aadt_filled'].mean()
    median_aadt = df['aadt_filled'].median()

    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=df['aadt_filled'],
        nbinsx=50,
        name='AADT',
        marker=dict(color=CHART_COLORS[0], opacity=0.7),
        hovertemplate='AADT: %{x:,.0f}<br>Count: %{y}<extra></extra>'
    ))

    # Mean line
    fig.add_vline(
        x=mean_aadt,
        line_dash="dash",
        line_color=CHART_COLORS[1],
        annotation_text=f"Mean: {mean_aadt:,.0f}",
        annotation_position="top"
    )

    # Median line
    fig.add_vline(
        x=median_aadt,
        line_dash="dash",
        line_color=CHART_COLORS[2],
        annotation_text=f"Median: {median_aadt:,.0f}",
        annotation_position="bottom"
    )

    fig.update_layout(
        title=title,
        xaxis_title="AADT (vehicles/day)",
        yaxis_title="Number of Work Zones",
        template=PLOTLY_THEME,
        height=400,
        showlegend=False
    )

    return fig


def create_aadt_boxplot(df: pd.DataFrame, title: str = "AADT by Traffic Category") -> go.Figure:
    """
    Create box plot showing AADT distribution by traffic category

    Args:
        df: Work zone dataframe
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if 'aadt_filled' not in df.columns or 'traffic_volume_category' not in df.columns:
        return go.Figure()

    # Order categories
    category_order = ['very_low', 'low', 'medium', 'high', 'very_high']

    fig = go.Figure()

    for cat in category_order:
        cat_data = df[df['traffic_volume_category'] == cat]['aadt_filled']
        if len(cat_data) > 0:
            fig.add_trace(go.Box(
                y=cat_data,
                name=TRAFFIC_LABELS.get(cat, cat),
                marker_color=TRAFFIC_COLORS.get(cat, '#cccccc'),
                boxmean=True,
                hovertemplate='%{y:,.0f}<extra></extra>'
            ))

    fig.update_layout(
        title=title,
        yaxis_title="AADT (vehicles/day)",
        xaxis_title="Traffic Category",
        template=PLOTLY_THEME,
        height=400,
        showlegend=False
    )

    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str = 'duration_days',
    y_col: str = 'aadt_filled',
    size_col: str = 'exposure_score',
    color_col: str = 'traffic_volume_category',
    title: str = "AADT vs Duration"
) -> go.Figure:
    """
    Create scatter plot with size and color encoding

    Args:
        df: Work zone dataframe
        x_col: Column for x-axis
        y_col: Column for y-axis
        size_col: Column for marker size
        color_col: Column for marker color
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    # Check if columns exist
    required_cols = [x_col, y_col]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    # Prepare data
    plot_df = df[[x_col, y_col, size_col, color_col]].dropna()

    if len(plot_df) == 0:
        return go.Figure()

    # Create color mapping
    if color_col == 'traffic_volume_category':
        color_map = TRAFFIC_COLORS
        category_order = ['very_low', 'low', 'medium', 'high', 'very_high']
    else:
        color_map = None
        category_order = None

    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        color_discrete_map=color_map,
        category_orders={color_col: category_order} if category_order else None,
        template=PLOTLY_THEME,
        hover_data={
            x_col: ':,.0f',
            y_col: ':,.0f',
            size_col: ':,.2f'
        }
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        height=500
    )

    return fig


def create_duration_histogram(df: pd.DataFrame, title: str = "Work Zone Duration Distribution") -> go.Figure:
    """
    Create histogram showing duration distribution

    Args:
        df: Work zone dataframe
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if 'duration_days' not in df.columns:
        return go.Figure()

    mean_duration = df['duration_days'].mean()
    median_duration = df['duration_days'].median()

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df['duration_days'],
        nbinsx=50,
        name='Duration',
        marker=dict(color=CHART_COLORS[3], opacity=0.7),
        hovertemplate='Duration: %{x:,.0f} days<br>Count: %{y}<extra></extra>'
    ))

    fig.add_vline(
        x=mean_duration,
        line_dash="dash",
        line_color=CHART_COLORS[1],
        annotation_text=f"Mean: {mean_duration:.0f} days",
        annotation_position="top"
    )

    fig.add_vline(
        x=median_duration,
        line_dash="dash",
        line_color=CHART_COLORS[2],
        annotation_text=f"Median: {median_duration:.0f} days",
        annotation_position="bottom"
    )

    fig.update_layout(
        title=title,
        xaxis_title="Duration (days)",
        yaxis_title="Number of Work Zones",
        template=PLOTLY_THEME,
        height=400,
        showlegend=False
    )

    return fig


def create_top_exposure_table(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Create table showing top work zones by exposure score

    Args:
        df: Work zone dataframe
        top_n: Number of top zones to return

    Returns:
        pd.DataFrame: Formatted table data
    """
    if 'exposure_score' not in df.columns:
        return pd.DataFrame()

    # Select relevant columns
    cols = ['road_name', 'CNTY_NM', 'aadt_filled', 'duration_days', 'exposure_score']
    available_cols = [col for col in cols if col in df.columns]

    top_zones = df.nlargest(top_n, 'exposure_score')[available_cols].copy()

    # Format numeric columns
    if 'aadt_filled' in top_zones.columns:
        top_zones['aadt_filled'] = top_zones['aadt_filled'].apply(lambda x: f"{x:,.0f}")

    if 'duration_days' in top_zones.columns:
        top_zones['duration_days'] = top_zones['duration_days'].apply(lambda x: f"{x:.0f}")

    if 'exposure_score' in top_zones.columns:
        top_zones['exposure_score'] = top_zones['exposure_score'].apply(lambda x: f"{x:.2f}")

    # Rename columns
    column_rename = {
        'road_name': 'Road',
        'CNTY_NM': 'County',
        'aadt_filled': 'AADT',
        'duration_days': 'Duration (days)',
        'exposure_score': 'Exposure Score'
    }

    top_zones = top_zones.rename(columns=column_rename)

    return top_zones


def create_temporal_line_chart(df: pd.DataFrame, title: str = "Work Zones Over Time") -> go.Figure:
    """
    Create line chart showing work zone counts over time

    Args:
        df: Work zone dataframe
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if 'start_date_parsed' not in df.columns:
        return go.Figure()

    # Group by date
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['start_date_parsed']).dt.date
    daily_counts = df_copy.groupby('date').size().reset_index(name='count')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_counts['date'],
        y=daily_counts['count'],
        mode='lines+markers',
        name='Work Zones',
        line=dict(color=CHART_COLORS[0], width=2),
        marker=dict(size=6),
        hovertemplate='%{x}<br>%{y:,} work zones<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Number of Work Zones",
        template=PLOTLY_THEME,
        height=400,
        showlegend=False
    )

    return fig
