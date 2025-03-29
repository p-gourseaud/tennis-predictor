"""Create features for the model."""

from datetime import datetime

import numpy as np
import pandas as pd

from tennis_predictor.config.data import (
    FEATURES_INTERIM_PATH,
    JOINED_INTERIM_PATH,
    TOURNAMENT_COUNTRY_PATH,
)
from tennis_predictor.helpers.data import open_df, save_df
from tennis_predictor.helpers.elo import estimate_winrate


def get_age(df):
    """Compute age in years for winner and loser."""
    # Constants
    BIRTH_COL = "birth"
    BIRTH_LOSER_COL = "birth_loser"
    BIRTH_FORMAT = "%Y%m%d"
    DATE_COL = "Date"
    DATE_FORMAT = "%Y-%m-%d"
    AGE_COL = "age"
    AGE_LOSER_COL = "age_loser"
    # Cast as time
    df[BIRTH_COL] = df[BIRTH_COL].apply(
        lambda x: (
            datetime.strptime(str(int(x)), BIRTH_FORMAT) if not np.isnan(x) else pd.NaT
        )
    )
    df[BIRTH_LOSER_COL] = df[BIRTH_LOSER_COL].apply(
        lambda x: (
            datetime.strptime(str(int(x)), BIRTH_FORMAT) if not np.isnan(x) else pd.NaT
        )
    )
    df[DATE_COL] = df[DATE_COL].apply(
        lambda x: datetime.strptime(x, DATE_FORMAT) if not x == "" else pd.NaT
    )
    # COmpute age in years
    df[AGE_COL] = (df[DATE_COL] - df[BIRTH_COL]).apply(lambda x: x.days / 365.25)
    df[AGE_LOSER_COL] = (df[DATE_COL] - df[BIRTH_LOSER_COL]).apply(
        lambda x: x.days / 365.25
    )
    return df


def get_country(df, df_country):
    """Add country code and home/away indicator for winner and loser."""
    df = df.merge(df_country, on=["Location", "Tournament"], how="left")
    df["home"] = (df["country"] == df["Country_Code"]).astype(int)
    df["home_loser"] = (df["country_loser"] == df["Country_Code"]).astype(int)
    return df


def get_diff(df):
    # Diff features
    df["hand_diff"] = df["hand"].apply(lambda x: 1 if x == "L" else 0) - df[
        "hand_loser"
    ].apply(lambda x: 1 if x == "L" else 0)
    df["rank_diff"] = df["rank_winner"] - df["rank_loser"]
    df["points_diff"] = df["points_winner"] - df["points_loser"]
    df["elo_diff"] = df["elo_winner"] - df["elo_loser"]
    df["elo_surface_diff"] = df["elo_surface_winner"] - df["elo_surface_loser"]
    df["age_diff"] = df["age"] - df["age_loser"]
    df["home_diff"] = df["home"] - df["home_loser"]
    df[
        [
            "hand_diff",
            "rank_diff",
            "points_diff",
            "elo_diff",
            "elo_surface_diff",
            "age_diff",
            "home_diff",
        ]
    ].fillna(0, inplace=True)
    return df


def get_elo_prob(df):
    df["elo_prob"] = df[["elo_winner", "elo_loser"]].apply(
        lambda x: estimate_winrate(*x), axis=1
    )
    df["elo_surface_prob"] = df[["elo_surface_winner", "elo_surface_loser"]].apply(
        lambda x: estimate_winrate(*x), axis=1
    )
    return df


def get_label(df):
    df["y"] = 1
    return df


if __name__ == "__main__":
    df_country = open_df(TOURNAMENT_COUNTRY_PATH)
    df_features = open_df(JOINED_INTERIM_PATH)
    df_features = get_age(df_features)
    df_features = get_country(df_features, df_country)
    df_features = get_diff(df_features)
    df_features = get_elo_prob(df_features)
    df_features = get_label(df_features)
    save_df(df_features, FEATURES_INTERIM_PATH)
