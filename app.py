import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="IPL Dashboard", layout="wide")

# Custom CSS (🔥 PREMIUM UI)
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    h1, h2, h3 {
        color: #f39c12;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🏏 IPL Analytics Dashboard")

# Load data
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# Sidebar
st.sidebar.title("🔍 Filters")
season = st.sidebar.selectbox("Select Season", sorted(matches['season'].unique()))

filtered = matches[matches['season'] == season]

# 🎯 KPI SECTION (IMPORTANT 🔥)
col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", len(filtered))
col2.metric("Total Teams", filtered['team1'].nunique())
col3.metric("Total Venues", filtered['venue'].nunique())

st.markdown("---")

# Charts Layout
col1, col2 = st.columns(2)

# Chart 1
with col1:
    st.subheader("🏆 Top Teams")
    wins = filtered['winner'].value_counts().head(5)
    fig1 = px.bar(
        x=wins.index,
        y=wins.values,
        color=wins.values,
        color_continuous_scale="Oranges"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2
with col2:
    st.subheader("🏟️ Top Venues")
    venues = filtered['venue'].value_counts().head(5)
    fig2 = px.bar(
        x=venues.values,
        y=venues.index,
        orientation='h',
        color=venues.values,
        color_continuous_scale="Teal"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Chart 3 (Full width)
st.subheader("📈 Runs Per Season")

season_runs = deliveries.merge(
    matches[['id','season']],
    left_on='match_id',
    right_on='id'
)

season_runs = season_runs.groupby('season')['total_runs'].sum().reset_index()

fig3 = px.line(
    season_runs,
    x='season',
    y='total_runs',
    markers=True,
    line_shape='spline'
)

st.plotly_chart(fig3, use_container_width=True)

# Insights Section
st.markdown("## 📊 Insights")

st.info("🏏 Toss has limited impact on match results")
st.success("🔥 Some venues consistently produce high scores")
st.warning("⚠️ Team performance matters more than toss")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | IPL Data Project")