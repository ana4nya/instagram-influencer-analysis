import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analysis import (
    load_data,
    calculate_creator_metrics,
    calculate_performance_score,
    classify_creators,
    rank_creators
)

st.set_page_config(
    page_title="Instagram Influencer Analysis",
    layout="wide"
)

st.title(
    "Instagram Influencer Selection & Performance Analysis System"
)

st.write(
    "An analytical system for evaluating Instagram creator "
    "performance and identifying high potential creators."
)

st.sidebar.header("Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload Campaign Excel / CSV",
    type=["xlsx", "csv"]
)

if uploaded_file is None:
    st.stop()

df = load_data(uploaded_file)

creator_data = calculate_creator_metrics(df)

creator_data = calculate_performance_score(
    creator_data
)

creator_data = classify_creators(
    creator_data
)

creator_data = rank_creators(
    creator_data
)

st.header("Campaign Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Creators",
        creator_data["Creator"].nunique()
    )

with col2:
    st.metric(
        "Tracked Reels",
        len(df)
    )

with col3:
    st.metric(
        "Total Views",
        f"{df['Views'].sum():,.0f}"
    )

with col4:
    st.metric(
        "Average Reel Views",
        f"{df['Views'].mean():,.0f}"
    )

st.header("Top Performing Creators")

top_creators = creator_data.head(10)

fig, ax = plt.subplots()

ax.bar(
    top_creators["Creator"],
    top_creators["Performance_Score"],
    color="#7C3AED"
)

ax.set_title("Top Creators by Performance Score")
ax.set_xlabel("Creator")
ax.set_ylabel("Performance Score")

plt.xticks(rotation=45)

st.pyplot(fig)

st.header("Followers vs Average Views")

fig, ax = plt.subplots()

ax.scatter(
    creator_data["Followers"],
    creator_data["Average_Views"],
    color="#EC4899",
    alpha=0.8,
    s=80
)

ax.set_title("Followers vs Average Views")
ax.set_xlabel("Followers")
ax.set_ylabel("Average Views")

st.pyplot(fig)

st.header("Influencer Selection")

min_followers = st.number_input(
    "Minimum Followers",
    min_value=0,
    value=0,
    step=1000
)

min_average_views = st.number_input(
    "Minimum Average Views",
    min_value=0,
    value=0,
    step=1000
)

min_score = st.slider(
    "Minimum Performance Score",
    min_value=0,
    max_value=100,
    value=0
)

recommended = creator_data[
    (creator_data["Followers"] >= min_followers)
    &
    (creator_data["Average_Views"] >= min_average_views)
    &
    (creator_data["Performance_Score"] >= min_score)
]

st.subheader("Recommended Creators")

if recommended.empty:
    st.warning(
        "No creators match the selected criteria."
    )
else:
    st.dataframe(
        recommended[
            [
                "Rank",
                "Creator",
                "Followers",
                "Reels",
                "Total_Views",
                "Average_Views",
                "Best_Reel_Views",
                "Performance_Score",
                "Category"
            ]
        ],
        use_container_width=True
    )

st.header("Creator Details")

selected_creator = st.selectbox(
    "Select a creator",
    creator_data["Creator"].tolist()
)

selected_data = creator_data[
    creator_data["Creator"] == selected_creator
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Followers",
        f"{selected_data['Followers']:,.0f}"
    )

with c2:
    st.metric(
        "Tracked Reels",
        int(selected_data["Reels"])
    )

with c3:
    st.metric(
        "Average Views",
        f"{selected_data['Average_Views']:,.0f}"
    )

with c4:
    st.metric(
        "Performance Score",
        f"{selected_data['Performance_Score']:.2f}"
    )

creator_reels = df[
    df["Creator"] == selected_creator
].copy()

fig, ax = plt.subplots()

ax.bar(
    range(1, len(creator_reels) + 1),
    creator_reels["Views"],
    color="#F59E0B"
)

ax.set_title(
    f"Reel Performance - {selected_creator}"
)

ax.set_xlabel("Reel")
ax.set_ylabel("Views")

st.pyplot(fig)

st.header("Complete Creator Ranking")

st.dataframe(
    creator_data[
        [
            "Rank",
            "Creator",
            "Followers",
            "Reels",
            "Total_Views",
            "Average_Views",
            "Best_Reel_Views",
            "Views_Follower_Ratio",
            "Performance_Score",
            "Category"
        ]
    ],
    use_container_width=True
)