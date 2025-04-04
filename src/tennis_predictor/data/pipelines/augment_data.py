"""Augment the dataset by inverting the winner and loser."""

import random

import numpy as np
import pandas as pd

from tennis_predictor.config.columns import Y
from tennis_predictor.config.data import TRAIN_AUGMENTED_PATH, TRAIN_PATH
from tennis_predictor.helpers.data import open_df, save_df


def augment_data(df_train):
    """Augment the dataset by inverting the winner and loser."""
    df_train2 = df_train.copy()
    # Invert winner and loser
    df_train2[["P1", "P2"]] = df_train[["P2", "P1"]]
    df_train2[["P1_rank", "P2_rank"]] = df_train[["P2_rank", "P1_rank"]]
    df_train2[["P1_points", "P2_points"]] = df_train[["P2_points", "P1_points"]]
    df_train2[["P1_set1", "P2_set1"]] = df_train[["P2_set1", "P1_set1"]]
    df_train2[["P1_set2", "P2_set2"]] = df_train[["P2_set2", "P1_set2"]]
    df_train2[["P1_set3", "P2_set3"]] = df_train[["P2_set3", "P1_set3"]]
    df_train2[["P1_set4", "P2_set4"]] = df_train[["P2_set4", "P1_set4"]]
    df_train2[["P1_set5", "P2_set5"]] = df_train[["P2_set5", "P1_set5"]]
    df_train2[["P1_sets", "P2_sets"]] = df_train[["P2_sets", "P1_sets"]]
    df_train2[["P1_odds_CB", "P2_odds_CB"]] = df_train[["P2_odds_CB", "P1_odds_CB"]]
    df_train2[["P1_odds_GB", "P2_odds_GB"]] = df_train[["P2_odds_GB", "P1_odds_GB"]]
    df_train2[["P1_odds_IW", "P2_odds_IW"]] = df_train[["P2_odds_IW", "P1_odds_IW"]]
    df_train2[["P1_odds_SB", "P2_odds_SB"]] = df_train[["P2_odds_SB", "P1_odds_SB"]]
    df_train2[["P1_odds_B365", "P2_odds_B365"]] = df_train[
        ["P2_odds_B365", "P1_odds_B365"]
    ]
    df_train2[["P1_odds_B&W", "P2_odds_B&W"]] = df_train[["P2_odds_B&W", "P1_odds_B&W"]]
    df_train2[["P1_odds_EX", "P2_odds_EX"]] = df_train[["P2_odds_EX", "P1_odds_EX"]]
    df_train2[["P1_odds_PS", "P2_odds_PS"]] = df_train[["P2_odds_PS", "P1_odds_PS"]]
    df_train2[["P1_odds_UB", "P2_odds_UB"]] = df_train[["P2_odds_UB", "P1_odds_UB"]]
    df_train2[["P1_odds_LB", "P2_odds_LB"]] = df_train[["P2_odds_LB", "P1_odds_LB"]]
    df_train2[["P1_odds_SJ", "P2_odds_SJ"]] = df_train[["P2_odds_SJ", "P1_odds_SJ"]]
    df_train2[["P1_odds_Max", "P2_odds_Max"]] = df_train[["P2_odds_Max", "P1_odds_Max"]]
    df_train2[["P1_odds_Avg", "P2_odds_Avg"]] = df_train[["P2_odds_Avg", "P1_odds_Avg"]]
    df_train2[["P1_id", "P2_id"]] = df_train[["P2_id", "P1_id"]]
    df_train2[["P1_firstName", "P2_firstName"]] = df_train[
        ["P2_firstName", "P1_firstName"]
    ]
    df_train2[["P1_lastName", "P2_lastName"]] = df_train[["P2_lastName", "P1_lastName"]]
    df_train2[["P1_hand", "P2_hand"]] = df_train[["P2_hand", "P1_hand"]]
    df_train2[["P1_birth", "P2_birth"]] = df_train[["P2_birth", "P1_birth"]]
    df_train2[["P1_country", "P2_country"]] = df_train[["P2_country", "P1_country"]]
    df_train2[["P1_elo", "P2_elo"]] = df_train[["P2_elo", "P1_elo"]]
    df_train2[["P1_elo_surface", "P2_elo_surface"]] = df_train[
        ["P2_elo_surface", "P1_elo_surface"]
    ]
    df_train2[["P1_age", "P2_age"]] = df_train[["P2_age", "P1_age"]]
    df_train2[["P1_home", "P2_home"]] = df_train[["P2_home", "P1_home"]]
    # Invert the probabilities
    df_train2["elo_prob"] = 1 - df_train["elo_prob"]
    df_train2["elo_surface_prob"] = 1 - df_train["elo_surface_prob"]
    # Negate the diff features
    df_train2["hand_diff"] = -df_train["hand_diff"]
    df_train2["rank_diff"] = -df_train["rank_diff"]
    df_train2["points_diff"] = -df_train["points_diff"]
    df_train2["elo_diff"] = -df_train["elo_diff"]
    df_train2["elo_surface_diff"] = -df_train["elo_surface_diff"]
    df_train2["age_diff"] = -df_train["age_diff"]
    df_train2["home_diff"] = -df_train["home_diff"]
    # Change the label
    df_train2[Y] = 0
    # Concatenate
    df_train_augmented = pd.concat([df_train, df_train2], axis=0)
    return df_train_augmented


def shuffle_data(df_train_augmented):
    """Shuffle the dataset."""
    # Set seed for reproducible shuffle
    random.seed(42)
    np.random.seed(42)
    df_train_augmented = df_train_augmented.sample(frac=1).reset_index(drop=True)
    return df_train_augmented


if __name__ == "__main__":
    df_train = open_df(TRAIN_PATH)
    df_train_augmented = augment_data(df_train)
    df_train_augmented = shuffle_data(df_train_augmented)
    save_df(df_train_augmented, TRAIN_AUGMENTED_PATH)
