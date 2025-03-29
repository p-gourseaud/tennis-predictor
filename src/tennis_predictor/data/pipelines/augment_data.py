"""Augment the dataset by inverting the winner and loser."""

import random

import numpy as np
import pandas as pd

from tennis_predictor.config.data import TRAIN_AUGMENTED_PATH, TRAIN_PATH
from tennis_predictor.helpers.data import open_df, save_df


def augment_data(df_train):
    """Augment the dataset by inverting the winner and loser."""
    df_train2 = df_train.copy()
    # Invert winner and loser
    df_train2[["hand", "hand_loser"]] = df_train[["hand_loser", "hand"]]
    df_train2[["rank_winner", "rank_loser"]] = df_train[
        [
            "rank_loser",
            "rank_winner",
        ]
    ]
    df_train2[["points_winner", "points_loser"]] = df_train[
        ["points_loser", "points_winner"]
    ]
    df_train2[["elo_winner", "elo_loser"]] = df_train[["elo_loser", "elo_winner"]]
    df_train2[["elo_surface_winner", "elo_surface_loser"]] = df_train[
        ["elo_surface_loser", "elo_surface_winner"]
    ]
    df_train2[["age", "age_loser"]] = df_train[["age_loser", "age"]]
    df_train2[["home", "home_loser"]] = df_train[["home_loser", "home"]]
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
    df_train2["y"] = 0
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
