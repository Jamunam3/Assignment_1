import streamlit as st
import pandas as pd
import sqlalchemy
import plotly.express as px

# ---------------- DATABASE CONNECTION ---------------- #
engine = sqlalchemy.create_engine(
    "mysql+pymysql://root:sindhuravi@localhost:3306/usgs"
)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="🌋 SeismoScope | Earthquake Intelligence Hub",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM SIDEBAR STYLE ---------------- #
st.markdown("""
    <style>
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;  /* White background */
    }

    /* Sidebar title style */
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        color: #FF4B4B;  /* You can keep red or change */
    }

    /* Sidebar text color (so text is visible on white) */
    .css-1d391kg {  /* sidebar content text */
        color: #000000;  /* black text */
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR BRANDING ---------------- #
st.sidebar.markdown("<p class='sidebar-title'>🌍 SeismoScope</p>", unsafe_allow_html=True)
st.sidebar.caption("Real-Time Seismic Intelligence Dashboard")

st.sidebar.markdown("---")

# ---------------- CREATIVE NAVIGATION ---------------- #
page = st.sidebar.radio(
    "🧭 Explore the Dashboard",
    [
        "🏠 Project Overview",
        "🗄️ Data Lab (SQL Explorer)",
        "📊 Seismic Insights",
        "👩‍💻 About the Creator"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Powered by USGS Earthquake Data")


# -------------------------------- PAGE 1 --------------------------------
if page == "🏠 Project Overview":

    # Hero Section
    st.markdown("""
        <h1 style='text-align: center; color: #FF4B4B;'>
        🌋 SeismoScope: Global Earthquake Intelligence Platform
        </h1>
        <p style='text-align: center; font-size:18px;'>
        Turning Seismic Data into Actionable Insights
        </p>
    """, unsafe_allow_html=True)

    # Banner Image
    st.image("DashboardImage.png", width="stretch")

    st.markdown("---")

    # Project Description
    st.markdown("""
    ## 🌍 About This Project

    **SeismoScope** is an interactive seismic analytics dashboard built using 
    Python, SQL, and Streamlit to explore global earthquake activity over the last five years.

    The data is sourced from the 
    **United States Geological Survey (USGS)** and transformed into 
    meaningful insights using advanced SQL queries and visual analytics.

    This platform helps analyze:

    - 🌊 Tsunami-triggering events  
    - 🌎 Regional seismic intensity  
    - 📉 Depth vs Magnitude relationships  
    - 📈 Year-over-year earthquake trends  

    ---
    """)

    # Interactive Highlights Section
    st.subheader("⚡ Platform Capabilities")

    col1, col2, col3 = st.columns(3)

    col1.info("🗄️ **SQL Intelligence Lab**  \nRun advanced analytical queries on real earthquake data.")

    col2.success("📊 **Dynamic Visual Dashboards**  \nInteractive charts powered by Plotly.")

    col3.warning("🌍 **Geospatial Mapping**  \nVisualize global earthquake distribution in real-time.")

    st.markdown("---")

    # Tech Stack Section
    st.subheader("🛠️ Technology Stack")

    tech1, tech2, tech3, tech4 = st.columns(4)

    tech1.metric("Language", "Python 🐍")
    tech2.metric("Database", "MySQL 🗄️")
    tech3.metric("Framework", "Streamlit 🚀")
    tech4.metric("Visualization", "Plotly 📊")

    st.markdown("---")

    st.caption("📌 Database Used: `usgs_db` | Designed for Data-Driven Decision Making")

# -------------------------------- PAGE 2 --------------------------------
elif page == "🗄️ Data Lab (SQL Explorer)":

    st.markdown("""
    <h1 style='color:#FF4B4B;'>🧪 Seismic Intelligence Lab</h1>
    <p style='font-size:17px;'>Explore advanced earthquake analytics powered by SQL.</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Categorized Query Selection
    category = st.selectbox(
        "🔎 Choose Analysis Category",
        ["🌋 Magnitude Analysis",
         "🌊 Tsunami & Alerts",
         "🌍 Geographic Insights",
         "📈 Temporal Trends"]
    )

    query_options = {
        "🌋 Magnitude Analysis": {
            "Top 10 Strongest Earthquakes": """
                SELECT place, mag, depth_km, country
                FROM earthquakes
                WHERE type='earthquake'
                ORDER BY mag DESC LIMIT 10;
            """,
            "Top 10 Deepest Earthquakes": """
                SELECT place, depth_km, mag, country
                FROM earthquakes
                WHERE type='earthquake'
                ORDER BY depth_km DESC LIMIT 10;
            """
        },

        "🌊 Tsunami & Alerts": {
            "Tsunamis per Year": """
                SELECT year, COUNT(*) AS tsunami_count
                FROM earthquakes
                WHERE tsunami = 1
                GROUP BY year ORDER BY year;
            """,
            "Alert Level Distribution": """
                SELECT alert, COUNT(*) AS count
                FROM earthquakes
                WHERE alert IS NOT NULL
                GROUP BY alert ORDER BY count DESC;
            """
        },

        "🌍 Geographic Insights": {
            "Top Active Countries": """
                SELECT country, COUNT(*) AS total_quakes
                FROM earthquakes
                GROUP BY country
                ORDER BY total_quakes DESC LIMIT 10;
            """
        },

        "📈 Temporal Trends": {
            "Year with Most Earthquakes": """
                SELECT year, COUNT(*) AS count
                FROM earthquakes
                GROUP BY year
                ORDER BY count DESC LIMIT 1;
            """
        }
    }

    selected_query = st.selectbox(
        "📌 Select Analysis",
        list(query_options[category].keys())
    )

    query = query_options[category][selected_query]

    df = pd.read_sql(query, engine)

    st.markdown(f"### 📊 Results: {selected_query}")
    st.dataframe(df, width="stretch")

    st.success("✅ Query executed successfully.")

# -------------------------------- PAGE 3 --------------------------------
elif page == "📊 Seismic Insights":

    st.markdown("""
    <h1 style='color:#FF4B4B;'>🌍 Global Seismic Intelligence Dashboard</h1>
    <p style='font-size:17px;'>Real-time analytical overview of global earthquake activity.</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    base_query = """
        SELECT mag, depth_km, tsunami
        FROM earthquakes
        WHERE type='earthquake';
    """
    df = pd.read_sql(base_query, engine)

    # KPI Section
    st.subheader("⚡ Key Performance Indicators")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Events", len(df))
    k2.metric("Average Magnitude", round(df['mag'].mean(), 2))
    k3.metric("Average Depth (km)", round(df['depth_km'].mean(), 2))
    k4.metric("Tsunami Events", df[df['tsunami'] == 1].shape[0])

    st.markdown("---")

    # Year Trend
    st.subheader("📈 Earthquake Trend Over Time")

    year_query = """
        SELECT year, COUNT(*) AS count
        FROM earthquakes
        WHERE type='earthquake'
        GROUP BY year ORDER BY year;
    """
    df_year = pd.read_sql(year_query, engine)

    fig_year = px.line(df_year, x="year", y="count", title="Earthquake Count by Year")
    fig_year.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0), xaxis_fixedrange=True)
    st.plotly_chart(fig_year, use_container_width=True, config={"scrollZoom": False})

    st.markdown("---")

    # Top Countries Bar Chart
    st.subheader("🌍 Top 10 Countries by Average Magnitude")

    mag_query = """
        SELECT country, AVG(mag) AS avg_mag
        FROM earthquakes
        GROUP BY country
        ORDER BY avg_mag DESC LIMIT 10;
    """
    df_mag = pd.read_sql(mag_query, engine)

    fig = px.bar(
        df_mag,
        x="avg_mag",
        y="country",
        orientation="h",
        color="avg_mag",
        color_continuous_scale="RdYlBu_r",
        title="Average Magnitude by Country"
    )
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0), xaxis_fixedrange=True)
    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False})

    st.markdown("---")

    # Magnitude Distribution
    st.subheader("📊 Earthquake Magnitude Distribution")
    
    fig_mag_dist = px.histogram(df, x="mag", nbins=30, title="Magnitude Frequency Distribution")
    fig_mag_dist.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0), xaxis_fixedrange=True)
    st.plotly_chart(fig_mag_dist, use_container_width=True, config={"scrollZoom": False})

    st.markdown("---")

    # Depth Analysis
    st.subheader("⬇️ Depth Analysis")
    
    fig_depth = px.box(df, y="depth_km", title="Earthquake Depth Distribution")
    fig_depth.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_depth, use_container_width=True, config={"scrollZoom": False})

    st.markdown("---")

    # 2025 Geo Visualization
    st.subheader("🌎 Global Earthquake Distribution (2025)")

    df_2025 = pd.read_sql("""
        SELECT latitude, longitude, mag, place
        FROM earthquakes
        WHERE type='earthquake' AND year=2025;
    """, engine)

    if df_2025.empty:
        st.warning("No earthquake data available for 2025.")
    else:
        geo_fig = px.scatter_geo(
            df_2025,
            lat="latitude",
            lon="longitude",
            color="mag",
            size="mag",
            projection="natural earth",
            hover_name="place",
            color_continuous_scale="RdYlBu_r",
            title="Global Earthquake Epicenters 2025"
        )
        geo_fig.update_layout(height=600, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(geo_fig, use_container_width=True, config={"scrollZoom": False})

    st.markdown("---")

    # Tsunami Events Table
    st.subheader("🌊 Tsunami-Related Earthquakes")
    
    tsunami_query = """
        SELECT place, mag, depth_km, country, year
        FROM earthquakes
        WHERE tsunami = 1
        ORDER BY year DESC LIMIT 15;
    """
    df_tsunami = pd.read_sql(tsunami_query, engine)
    
    if not df_tsunami.empty:
        st.dataframe(df_tsunami, use_container_width=True)
    else:
        st.info("No tsunami data available.")

    st.markdown("---")

    # Statistical Summary
    st.subheader("📈 Statistical Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Max Magnitude", round(df['mag'].max(), 2))
        st.metric("Min Magnitude", round(df['mag'].min(), 2))
    
    with col2:
        st.metric("Max Depth (km)", round(df['depth_km'].max(), 2))
        st.metric("Min Depth (km)", round(df['depth_km'].min(), 2))

# -------------------------------- PAGE 4 --------------------------------
elif page == "👩‍💻 About the Creator":

    st.markdown("""
    <h1 style='color:#FF4B4B;'>👩‍💻 About the Creator</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🌋 Project Developed By

    **Jamuna Murugavel**  
    Data Analyst | Python Developer | SQL Specialist  

    ---

    ### 🛠️ Core Skills
    - Python (Pandas, NumPy)
    - SQL (Advanced Queries & Window Functions)
    - Streamlit Dashboard Development
    - Data Visualization (Plotly)
    - Geospatial Analytics

    ---

    ### 🎯 Project Vision
    To transform raw seismic data into meaningful insights that help governments,
    engineers, and policy makers make informed disaster-management decisions.
    """)

    st.success("🚀 Thank you for exploring SeismoScope!")
