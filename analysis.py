import pandas as pd
import numpy as np


def load_data(file_path):

    if str(file_path).lower().endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
    )

    
    column_mapping = {
        "PAGES": "Creator",
        "PAGE": "Creator",
        "FOLLOWERS": "Followers",
        "VIEWS": "Views",
        "PROFILE LINK": "Profile_Link",
        "REEL LINK": "Reel_Link"
    }

    df = df.rename(columns=column_mapping)

    
    df["Creator"] = (
        df["Creator"]
        .astype(str)
        .str.strip()
    )

    
    df["Followers"] = pd.to_numeric(
        df["Followers"],
        errors="coerce"
    )

    df["Views"] = pd.to_numeric(
        df["Views"],
        errors="coerce"
    )

    
    df = df.dropna(
        subset=[
            "Creator",
            "Followers",
            "Views"
        ]
    )

    return df


def calculate_creator_metrics(df):

    creator_data = (
        df.groupby("Creator")
        .agg(
            Followers=("Followers", "max"),
            Reels=("Views", "count"),
            Total_Views=("Views", "sum"),
            Average_Views=("Views", "mean"),
            Best_Reel_Views=("Views", "max")
        )
        .reset_index()
    )

   
    creator_data["Views_Follower_Ratio"] = (
        creator_data["Average_Views"]
        / creator_data["Followers"]
    ) * 100

    return creator_data


def normalize(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return (
        (series - minimum)
        / (maximum - minimum)
    ) * 100


def calculate_performance_score(creator_data):

    creator_data["Average_View_Score"] = normalize(
        creator_data["Average_Views"]
    )

    creator_data["Efficiency_Score"] = normalize(
        creator_data["Views_Follower_Ratio"]
    )

    creator_data["Performance_Score"] = (
        0.60 * creator_data["Average_View_Score"]
        + 0.40 * creator_data["Efficiency_Score"]
    )

    creator_data["Performance_Score"] = (
        creator_data["Performance_Score"]
        .round(2)
    )

    return creator_data


def classify_creator(score):

    if score >= 60:
        return "High Potential"

    elif score >= 30:
        return "Moderate Potential"

    else:
        return "Low Potential"


def classify_creators(creator_data):

    creator_data["Category"] = (
        creator_data["Performance_Score"]
        .apply(classify_creator)
    )

    return creator_data


def rank_creators(creator_data):

    creator_data = creator_data.sort_values(
        by="Performance_Score",
        ascending=False
    ).reset_index(drop=True)

    creator_data["Rank"] = (
        creator_data.index + 1
    )

    return creator_data