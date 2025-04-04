"""Create features for the model."""

from datetime import datetime

import numpy as np
import pandas as pd

from tennis_predictor.config.columns import Y
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
    DAYS_PER_YEAR = 365.25
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
    df[AGE_COL] = (df[DATE_COL] - df[BIRTH_COL]).apply(lambda x: x.days / DAYS_PER_YEAR)
    df[AGE_LOSER_COL] = (df[DATE_COL] - df[BIRTH_LOSER_COL]).apply(
        lambda x: x.days / DAYS_PER_YEAR
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
    df["WRank"] = df["WRank"].apply(lambda x: float(x) if x != "NR" else np.nan)
    df["LRank"] = df["LRank"].apply(lambda x: float(x) if x != "NR" else np.nan)
    df["rank_diff"] = df["WRank"] - df["LRank"]
    df["points_diff"] = df["WPts"] - df["LPts"]
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


def rename_columns(df):
    """Rename columns to remove knowledge of winner."""
    df_renamed = df.rename(
        columns={
            "Winner": "P1",
            "Loser": "P2",
            "WRank": "P1_rank",
            "LRank": "P2_rank",
            "WPts": "P1_points",
            "LPts": "P2_points",
            "W1": "P1_set1",
            "L1": "P2_set1",
            "W2": "P1_set2",
            "L2": "P2_set2",
            "W3": "P1_set3",
            "L3": "P2_set3",
            "W4": "P1_set4",
            "L4": "P2_set4",
            "W5": "P1_set5",
            "L5": "P2_set5",
            "Wsets": "P1_sets",
            "Lsets": "P2_sets",
            "CBW": "P1_odds_CB",
            "CBL": "P2_odds_CB",
            "GBW": "P1_odds_GB",
            "GBL": "P2_odds_GB",
            "IWW": "P1_odds_IW",
            "IWL": "P2_odds_IW",
            "SBW": "P1_odds_SB",
            "SBL": "P2_odds_SB",
            "B365W": "P1_odds_B365",
            "B365L": "P2_odds_B365",
            "B&WW": "P1_odds_B&W",
            "B&WL": "P2_odds_B&W",
            "EXW": "P1_odds_EX",
            "EXL": "P2_odds_EX",
            "PSW": "P1_odds_PS",
            "PSL": "P2_odds_PS",
            "UBW": "P1_odds_UB",
            "UBL": "P2_odds_UB",
            "LBW": "P1_odds_LB",
            "LBL": "P2_odds_LB",
            "SJW": "P1_odds_SJ",
            "SJL": "P2_odds_SJ",
            "MaxW": "P1_odds_Max",
            "MaxL": "P2_odds_Max",
            "AvgW": "P1_odds_Avg",
            "AvgL": "P2_odds_Avg",
            "id": "P1_id",
            "firstName": "P1_firstName",
            "lastName": "P1_lastName",
            "hand": "P1_hand",
            "birth": "P1_birth",
            "country": "P1_country",
            "id_loser": "P2_id",
            "firstName_loser": "P2_firstName",
            "lastName_loser": "P2_lastName",
            "hand_loser": "P2_hand",
            "birth_loser": "P2_birth",
            "country_loser": "P2_country",
            "elo_winner": "P1_elo",
            "elo_surface_winner": "P1_elo_surface",
            "elo_loser": "P2_elo",
            "elo_surface_loser": "P2_elo_surface",
            "age": "P1_age",
            "age_loser": "P2_age",
            "home": "P1_home",
            "home_loser": "P2_home",
        }
    )
    return df_renamed


def get_label(df):
    df[Y] = 1
    return df


if __name__ == "__main__":
    df_country = open_df(TOURNAMENT_COUNTRY_PATH)
    df_features = open_df(JOINED_INTERIM_PATH)
    df_features = get_age(df_features)
    df_features = get_country(df_features, df_country)
    df_features = get_diff(df_features)
    df_features = get_elo_prob(df_features)
    df_features = rename_columns(df_features)
    df_features = get_label(df_features)
    save_df(df_features, FEATURES_INTERIM_PATH)
