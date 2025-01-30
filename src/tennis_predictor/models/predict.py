import pandas as pd

from tennis_predictor.config.data import (
    DEV_PATH,
    DEV_PREDICTION_PATH,
    TEST_PATH,
    TEST_PREDICTION_PATH,
    TRAIN_PATH,
    TRAIN_PREDICTION_PATH,
)
from tennis_predictor.helpers.data import open_df, save_df
from tennis_predictor.helpers.elo import estimate_winrate


def predict_winner(df: pd.DataFrame):
    """Predict winner based on ELO."""
    df["winner_estimated_winrate"] = df[["elo_winner", "elo_loser"]].apply(
        lambda x: estimate_winrate(*x), axis=1
    )
    df["loser_estimated_winrate"] = 1 - df["winner_estimated_winrate"]
    df["y"] = 1
    df["y_hat"] = (df["winner_estimated_winrate"] > 0.5).astype(int)
    return df


def compute_kelly_criterion(df: pd.DataFrame):
    """Compute the Kelly criterion."""
    b = df["AvgW"] - 1
    p = df["winner_estimated_winrate"]
    q = 1 - p
    df["winner_kelly"] = (b * p - q) / b

    b = df["AvgL"] - 1
    p, q = q, p
    df["loser_kelly"] = (b * p - q) / b
    return df


if __name__ == "__main__":
    df_train = open_df(TRAIN_PATH)
    df_train = predict_winner(df_train)
    df_train = compute_kelly_criterion(df_train)
    save_df(df_train, TRAIN_PREDICTION_PATH)

    df_dev = open_df(DEV_PATH)
    df_dev = predict_winner(df_dev)
    df_dev = compute_kelly_criterion(df_dev)
    save_df(df_dev, DEV_PREDICTION_PATH)

    df_test = open_df(TEST_PATH)
    df_test = predict_winner(df_test)
    df_test = compute_kelly_criterion(df_test)
    save_df(df_test, TEST_PREDICTION_PATH)
