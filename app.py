import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Steam Games Marketplace Analytics Dashboard",
    page_icon="🎮",
    layout="wide"
)

# -------------------------
# Load Dataset
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/merged_data.csv")

df = load_data()
#temp
st.write(df.columns.tolist())
st.write(df.head())
#temp
# -------------------------
# Data Cleaning
# -------------------------

# Clean Original Price
df["Price"] = (
    df["Original Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("Free", "0", regex=False)
)

df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Release Year
df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
df["Release Year"] = df["Release Date"].dt.year
#temp
st.write("Release Year Min:", df["Release Year"].min())
st.write("Release Year Max:", df["Release Year"].max())

st.write(
    df[
        (df["Release Year"] < 1997) |
        (df["Release Year"] > 2026)
    ][["Title", "Release Date", "Release Year"]]
)
#temp
# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("🎛 Dashboard Filters")

selected_year = st.sidebar.selectbox(
    "Release Year",
    ["All"] + sorted(df["Release Year"].dropna().astype(int).unique().tolist())
)

price_range = st.sidebar.slider(
    "Price Range ($)",
    0,
    int(df["Price"].max()),
    (0, int(df["Price"].max()))
)

# Apply Filters

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["Release Year"] == selected_year
    ]

filtered_df = filtered_df[
    (filtered_df["Price"] >= price_range[0]) &
    (filtered_df["Price"] <= price_range[1])
]

st.sidebar.divider()

chart_option = st.sidebar.radio(
    "📊 View Charts",
    [
        "Show All Charts",
        "📈 Release Trend",
        "🍩 Free vs Paid",
        "🏆 Top Developers",
        "🏢 Top Publishers",
        "🏷️ Top Game Tags",
        "🌍 Supported Languages",
        "💰 Price vs Discount"
    ]
)

# -------------------------
# Dashboard Title
# -------------------------
st.title("🎮 Steam Games Marketplace Analytics Dashboard")

st.markdown("""
Welcome to the Steam Games Marketplace Analytics Dashboard.

This dashboard provides interactive insights into Steam games, including pricing, discounts, developers, publishers, release trends, and more.
""")

st.divider()

# -------------------------
# KPI Cards
# -------------------------

# Clean Original Price column
price = (
    df["Original Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("Free", "0", regex=False)
)

price = pd.to_numeric(price, errors="coerce")

# KPI calculations
total_games = len(filtered_df)
free_games = (filtered_df["Price"] == 0).sum()
paid_games = total_games - free_games
average_price = filtered_df["Price"].mean()

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎮 Total Games", f"{total_games:,}")

with col2:
    st.metric("🆓 Free Games", f"{free_games:,}")

with col3:
    st.metric("💰 Paid Games", f"{paid_games:,}")

with col4:
    st.metric("💲 Average Price", f"${average_price:.2f}")


#Chart 1: Game Releases Over Time
if chart_option in ["Show All Charts", "📈 Release Trend"]:
 st.divider()

 st.subheader("📈 Game Releases Over Time")
 release_trend = (
    filtered_df.groupby("Release Year")
    .size()
    .reset_index(name="Number of Games")
 )

 fig = px.line(
    release_trend,
    x="Release Year",
    y="Number of Games",
    markers=True,
    title="Steam Game Releases by Year"
 )

 fig.update_layout(
    template="plotly_white",
    xaxis_title="Release Year",
    yaxis_title="Number of Games"
 )

 st.plotly_chart(fig, use_container_width=True)

#Chart 2 & 3: Free vs Paid Games & Top 10 Developers
if chart_option == "Show All Charts":

    st.divider()

    col1, col2 = st.columns([1, 1])

    # -------- LEFT : Free vs Paid --------
    with col1:

        st.subheader("🆓 Free vs Paid Games")

        game_type = filtered_df["Price"].apply(
            lambda x: "Free" if x == 0 else "Paid"
        )

        game_counts = game_type.value_counts().reset_index()
        game_counts.columns = ["Game Type", "Count"]

        fig1 = px.pie(
            game_counts,
            names="Game Type",
            values="Count",
            hole=0.5,
            title="Free vs Paid Games"
        )

        fig1.update_layout(template="plotly_white")

        st.plotly_chart(fig1, use_container_width=True)

    # -------- RIGHT : Top Developers --------
    with col2:

        st.subheader("🏆 Top 10 Developers")

        top_dev = (
            filtered_df["Developer"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_dev.columns = ["Developer", "Games"]

        fig2 = px.bar(
            top_dev,
            x="Games",
            y="Developer",
            orientation="h",
            title="Top 10 Developers",
            height=450
        )

        fig2.update_layout(
            template="plotly_white",
            yaxis=dict(categoryorder="total ascending"),
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(fig2, use_container_width=True)


# -------------------- FREE VS PAID ONLY --------------------
elif chart_option == "🍩 Free vs Paid":

    st.subheader("🆓 Free vs Paid Games")

    game_type = filtered_df["Price"].apply(
        lambda x: "Free" if x == 0 else "Paid"
    )

    game_counts = game_type.value_counts().reset_index()
    game_counts.columns = ["Game Type", "Count"]

    fig1 = px.pie(
        game_counts,
        names="Game Type",
        values="Count",
        hole=0.5,
        title="Free vs Paid Games"
    )

    fig1.update_layout(template="plotly_white")

    st.plotly_chart(fig1, use_container_width=True)


# -------------------- TOP DEVELOPERS ONLY --------------------
elif chart_option == "🏆 Top Developers":

    st.subheader("🏆 Top 10 Developers")

    top_dev = (
        filtered_df["Developer"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_dev.columns = ["Developer", "Games"]

    fig2 = px.bar(
        top_dev,
        x="Games",
        y="Developer",
        orientation="h",
        title="Top 10 Developers",
        height=500
    )

    fig2.update_layout(
        template="plotly_white",
        yaxis=dict(categoryorder="total ascending"),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    st.plotly_chart(fig2, use_container_width=True)

# CHART 4 : Top 10 Publishers
if chart_option in ["Show All Charts", "🏢 Top Publishers"]:
 st.divider()
 st.subheader("🏢 Top 10 Publishers")

 top_pub = (
    filtered_df["Publisher"]
    .value_counts()
    .head(10)
    .reset_index()
 )

 top_pub.columns = ["Publisher", "Games"]

 fig3 = px.bar(
    top_pub,
    x="Publisher",
    y="Games",
    title="Top 10 Publishers",
    color="Games",
    color_continuous_scale="Blues",
    text="Games"
 )

 fig3.update_traces(textposition="outside")

 fig3.update_layout(
    template="plotly_white",
    xaxis_title="Publisher",
    yaxis_title="Number of Games",
    xaxis_tickangle=-45,
    margin=dict(l=10, r=10, t=50, b=80)
 )

 st.plotly_chart(fig3, use_container_width=True)

# CHART 5 : Most Popular Game Tags
if chart_option in ["Show All Charts", "🏷️ Top Game Tags"]:
 st.divider()

 st.subheader("🏷️ Top 15 Game Tags")

 # Split tags into individual values
 tags = (
    filtered_df["Popular Tags"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
 )

 top_tags = (
    tags.value_counts()
    .head(15)
    .reset_index()
 )

 top_tags.columns = ["Tag", "Count"]

 fig4 = px.bar(
    top_tags,
    x="Count",
    y="Tag",
    orientation="h",
    title="Top 10 Most Popular Steam Tags",
    color="Count",
    color_continuous_scale="Viridis",
    text="Count",
    height=500
 )

 fig4.update_traces(textposition="outside")

 fig4.update_layout(
    template="plotly_white",
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Number of Games",
    yaxis_title="Game Tags",
    margin=dict(l=10, r=40, t=50, b=10)
 )

 st.plotly_chart(fig4, use_container_width=True)

# CHART 6 : Top Supported Languages
if chart_option in ["Show All Charts", "🌍 Supported Languages"]:

 st.divider()
 st.subheader("🌍 Top 15 Supported Languages")

 languages = (
    filtered_df["Supported Languages"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
 )

 top_languages = (
    languages.value_counts()
    .head(15)
    .reset_index()
 )

 top_languages.columns = ["Language", "Games"]

 fig5 = go.Figure()

 # Lollipop sticks
 fig5.add_trace(
    go.Scatter(
        x=top_languages["Games"],
        y=top_languages["Language"],
        mode="lines",
        line=dict(color="lightgray", width=3),
        showlegend=False
    )
 )

 # Lollipop heads
 fig5.add_trace(
    go.Scatter(
        x=top_languages["Games"],
        y=top_languages["Language"],
        mode="markers+text",
        marker=dict(
            size=16,
            color=top_languages["Games"],
            colorscale="Viridis",
            showscale=True
        ),
        text=top_languages["Games"],
        textposition="middle right",
        showlegend=False
    )
 )

 fig5.update_layout(
    title="Top 10 Supported Languages",
    template="plotly_white",
    xaxis_title="Number of Games",
    yaxis_title="Language",
    margin=dict(l=10, r=40, t=50, b=10)
 )

 st.plotly_chart(fig5, use_container_width=True)

# CHART 7 : Price vs Discount
if chart_option in ["Show All Charts", "💰 Price vs Discount"]:
 st.divider()
 st.subheader("💰 Price vs Discount Analysis")

 scatter_df = filtered_df.copy()

 scatter_df["Original Price"] = (
    scatter_df["Original Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("Free", "0", regex=False)
 )

 scatter_df["Discounted Price"] = (
    scatter_df["Discounted Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("Free", "0", regex=False)
 )

 scatter_df["Original Price"] = pd.to_numeric(
    scatter_df["Original Price"],
    errors="coerce"
 )

 scatter_df["Discounted Price"] = pd.to_numeric(
    scatter_df["Discounted Price"],
    errors="coerce"
 )

 # Calculate discount percentage
 scatter_df["Discount (%)"] = (
    (
        scatter_df["Original Price"] -
        scatter_df["Discounted Price"]
    )
    / scatter_df["Original Price"]
 ) * 100

 scatter_df = scatter_df.dropna(
    subset=["Original Price", "Discount (%)"]
 )

 fig6 = px.scatter(
    scatter_df,
    x="Original Price",
    y="Discount (%)",
    hover_name="Title",
    color="Discount (%)",
    color_continuous_scale="Turbo",
    opacity=0.7,
    title="Relationship Between Original Price and Discount"
 )

 fig6.update_layout(
    template="plotly_white",
    xaxis_title="Original Price ($)",
    yaxis_title="Discount (%)",
    xaxis=dict(range=[0, 100]),
    margin=dict(l=10, r=10, t=50, b=10)
 )

 st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

with st.expander("📄 View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

st.caption(
    "🎮 Steam Games Marketplace Analytics Dashboard | Built with Streamlit & Plotly | Data Source: Steam Games Dataset"
)