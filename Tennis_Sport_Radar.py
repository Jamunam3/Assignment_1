import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# Connect to the SQL database
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Sindhuravi@3",
    database="Sportradar"
)
mycursor = conn.cursor()

# Sidebar - Navigation
st.sidebar.title("Sports Dashboard")
menu = st.sidebar.selectbox(
    "Go to:",
    ["Homepage", "Competitor Analysis", "Competition Overview", "Venue & Complex Analysis", "Leaderboard"]
)

# Homepage
if menu == "Homepage":
    st.title("Sports Data Dashboard")
    st.subheader("Welcome to the interactive sports dashboard!")
    st.markdown("""
    This dashboard provides detailed analytics on sports competitions, rankings, competitors, and venues across different categories.
    """)

    # Overview of total competitions, competitors, and venues
    mycursor.execute("SELECT COUNT(*) FROM competitions_table")
    total_competitions = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM Competitors_table")
    total_competitors = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM Venues_table")
    total_venues = mycursor.fetchone()[0]

    st.metric("Total competitions", total_competitions)
    st.metric("Total Competitors", total_competitors)
    st.metric("Total Venues", total_venues)

    mycursor.execute("SELECT COUNT(DISTINCT country) FROM competitors_table")
    countries_represented = mycursor.fetchone()[0]
    st.metric("COUNTRY REPRESENTED", countries_represented)

    mycursor.execute("SELECT MAX(points) FROM competitor_rankings_table")
    highest_points = mycursor.fetchone()[0]
    st.metric("HIGHEST POINTS", highest_points)

# Competitor Analysis


elif menu == "Competitor Analysis":
    st.title("Competitor Analysis")

        # Search filters
    competitor_name = st.text_input("SEARCH COMPETITOR BY NAME")
    rank_range = st.slider("FILTER BY RANK RANGE", 1, 500, (1, 50))
    points_threshold = st.number_input("POINTS THRESHOLD", min_value=0, step=1)

    # Query
    query1 = f"""
    SELECT c.competitor_id, c.name, c.country, r.rank, r.points
    FROM competitors_table c
    JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
    WHERE c.name LIKE '%{competitor_name}%'
    AND r.rank BETWEEN {rank_range[0]} AND {rank_range[1]}
    AND r.points >= {points_threshold}
    ORDER BY r.points DESC
    """
    mycursor.execute(query1)
    competitors = mycursor.fetchall()

    # Display results
    if competitors:
        df_competitors = pd.DataFrame(
            competitors, 
            columns=["Competitor ID", "Name", "Country", "Rank", "Points"]
        )
        st.dataframe(df_competitors)
    else:
        st.write("No competitors found.")
    
    # Filter by country and category
    countries_query = "SELECT DISTINCT country FROM Competitors_table"
    mycursor.execute(countries_query)
    countries = [row[0] for row in mycursor.fetchall()]
    selected_country = st.selectbox("Select Country", countries)
    
    categories_query = "SELECT DISTINCT category_name FROM Categories_table"
    mycursor.execute(categories_query)
    categories = [row[0] for row in mycursor.fetchall()]
    selected_category = st.selectbox("Select Category", categories)
    
    # Query competitors based on filters
    query = f"""
    SELECT c.name, c.country, r.rank, r.points, r.movement
    FROM Competitors_table c
    JOIN Competitor_Rankings_table r ON c.competitor_id = r.competitor_id
    JOIN Competitions_table comp ON r.competitor_id = comp.competition_id
    JOIN Categories_table cat ON comp.category_id = cat.category_id
    WHERE c.country = '{selected_country}' AND cat.category_name = '{selected_category}'
    ORDER BY r.points DESC
    """
    mycursor.execute(query)
    competitors = mycursor.fetchall()

    if competitors:
        df_competitors = pd.DataFrame(competitors, columns=["Name", "Country", "Rank", "Points", "Movement"])
        st.dataframe(df_competitors)
        st.subheader("Competitor Rank Movement")
        fig = px.line(df_competitors, x="Name", y="Movement", title="Competitor Rank Movement")
        st.plotly_chart(fig)
    else:
        st.write("No competitors found for the selected filters.")

# Competition Overview
elif menu == "Competition Overview":
    st.title("Competition Overview")

    # Filter by competition type
    competition_types = ["Doubles", "Singles", "Mixed"]
    selected_type = st.selectbox("Select Competition Type", competition_types)
    
    # Query competition details
    query = f"""
    SELECT comp.competition_name, comp.type, comp.gender, cat.category_name, COUNT(c.competitor_id) AS total_competitors
    FROM Competitions_table comp
    JOIN Categories_table cat ON comp.category_id = cat.category_id
    JOIN Competitor_Rankings_table r ON comp.competition_id = r.competitor_id
    JOIN Competitors_table c ON r.competitor_id = c.competitor_id
    WHERE comp.type = '{selected_type}'
    GROUP BY comp.competition_name, comp.type, comp.gender, cat.category_name  
    """
    mycursor.execute(query)
    competitions = mycursor.fetchall()

    if competitions:
        df_competitions = pd.DataFrame(competitions, columns=["Competition Name", "Type", "Gender", "Category", "Total Competitors"])
        st.dataframe(df_competitions)
        st.subheader("Competition Category Breakdown")
        fig = px.pie(df_competitions, names="Category", values="Total Competitors", title="Competition Category Distribution")
        st.plotly_chart(fig)
    else:
        st.write("No competitions found for the selected type.")

        # Dropdown to select a competitor
    mycursor.execute("SELECT name FROM competitors_table")
    competitors_list = [row[0] for row in mycursor.fetchall()]
    selected_competitor = st.selectbox("Select a competitor:", competitors_list)

    # Query competitor details
    if selected_competitor:
        query2 = f"""
        SELECT r.rank,movement, r.competitions_played, c.country
        FROM competitors_table c
        JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
        WHERE c.name = '{selected_competitor}'
        """
        mycursor.execute(query2)
        details = mycursor.fetchone()

        if details:
            rank, movement, competitions_played, country = details
            st.subheader(f"Details for {selected_competitor}")
            st.write(f"**Rank:** {rank}")
            st.write(f"**Movement:** {movement}")
            st.write(f"**Competitions Played:** {competitions_played}")
            st.write(f"**Country:** {country}")
        else:
            st.error("No details found for the selected competitor.")

# Venue & Complex Analysis
elif menu == "Venue & Complex Analysis":
    st.title("Venue & Complex Analysis")

    # Query for venue and complex details
    query = """
    SELECT v.venue_name, v.city_name, v.country_name, c.complex_name
    FROM Venues_table v
    JOIN Complexes_table c ON v.complex_id = c.complex_id
    """
    mycursor.execute(query)
    venue_data = mycursor.fetchall()

    if venue_data:
        df_venues = pd.DataFrame(venue_data, columns=["Venue Name", "City", "Country", "Complex Name"])
        st.dataframe(df_venues)
        st.subheader("Venues by Country")
        fig = px.bar(df_venues, x="Country", title="Venues Distribution by Country")
        st.plotly_chart(fig)
    else:
        st.write("No venue data available.")

# Leaderboard
elif menu == "Leaderboard":
    st.title("Leaderboard")

    # Top-ranked competitors
    query4 = """
    SELECT c.name, c.country, r.rank
    FROM competitors_table c
    JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
    ORDER BY r.rank ASC
    LIMIT 10
    """
    mycursor.execute(query4)
    top_ranked = mycursor.fetchall()
    df_top_ranked = pd.DataFrame(top_ranked, columns=["Name", "Country", "Rank"])
    st.subheader("Top-Ranked Competitors")
    st.dataframe(df_top_ranked)

    # Competitors with the highest points
    query5 = """
    SELECT c.name, c.country, r.points
    FROM competitors_table c
    JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
    ORDER BY r.points DESC
    LIMIT 10
    """
    mycursor.execute(query5)
    top_points = mycursor.fetchall()
    df_top_points = pd.DataFrame(top_points, columns=["Name", "Country", "Points"])
    st.subheader("Competitors with the Highest Points")
    st.dataframe(df_top_points)
