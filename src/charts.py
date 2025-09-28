from __future__ import annotations

"""Plotly chart helpers with a consistent colorway and styling."""

from typing import Optional

import pandas as pd
import plotly.express as px


COLORWAY = [
    "#3B82F6",  # primary blue
    "#10B981",  # emerald
    "#F59E0B",  # amber
    "#EF4444",  # red
    "#8B5CF6",  # violet
    "#14B8A6",  # teal
]


def bar_by_department(df: pd.DataFrame, x: str = "department", y: str = "total_amount"):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=x,
        color_discrete_sequence=COLORWAY,
        title="Department Performance",
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        hovermode='closest'
    )
    fig.update_yaxes(
        title="Revenue ($)",
        gridcolor='rgba(128,128,128,0.2)',
        zeroline=False
    )
    fig.update_xaxes(
        title="Department",
        gridcolor='rgba(128,128,128,0.2)'
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        marker_line_width=1,
        marker_line_color='white'
    )
    return fig


def pie_by_region(df: pd.DataFrame, names: str = "region", values: str = "total_amount"):
    fig = px.pie(
        df,
        names=names,
        values=values,
        color=names,
        color_discrete_sequence=COLORWAY,
        title="Regional Distribution",
        hole=0.4,
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16,
        title_x=0.5,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        )
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        textinfo='label+percent',
        textfont_size=12
    )
    return fig


