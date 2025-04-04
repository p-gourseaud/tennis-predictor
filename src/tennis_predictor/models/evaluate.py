"""Evaluation of the models."""

import numpy as np
from sklearn.metrics import accuracy_score, log_loss

from tennis_predictor.config.columns import Y
from tennis_predictor.config.data import (
    DEV_EVALUATION_PATH,
    DEV_PREDICTION_PATH,
    DEV_SCORES_PATH,
    TEST_EVALUATION_PATH,
    TEST_PREDICTION_PATH,
    TEST_SCORES_PATH,
    TRAIN_EVALUATION_PATH,
    TRAIN_PREDICTION_PATH,
    TRAIN_SCORES_PATH,
)
from tennis_predictor.helpers.data import open_df, save_df, save_dict


def get_accuracy_score(df) -> float:
    return accuracy_score(df[Y], df["P1_wins_prediction"])


def get_log_loss(df) -> float:
    return log_loss(df[Y], df["P1_estimated_winrate"], labels=[0, 1])


def compute_kelly_capital(df):
    capital = 1
    # MAX_BET = 25000  # Gain maximal : 550 000€ avec côte de 20

    bets = []
    capitals = []

    for row in df.iterrows():
        winner_kelly, loser_kelly = row[1][["P1_kelly", "P2_kelly"]]
        if winner_kelly > 0:
            # Pari gagnant
            bet = capital * winner_kelly  # min(capital * winner_kelly, MAX_BET)
            capital += bet * (row[1]["P1_odds_Avg"] - 1)
        elif loser_kelly > 0:
            # Pari perdant, on ne perd que la mise
            bet = capital * loser_kelly  # min(capital * loser_kelly, MAX_BET)
            bet = -bet  # On met un signe négatif pour les paris perdants
            capital += bet
        else:
            # Aucun pari
            bet = 0
            capital = capital
        bets.append(bet)
        capitals.append(capital)
    df["bets"] = bets
    df["capitals"] = capitals
    # TODO: Compute bankroll growth
    df["growth"] = df["capitals"].pct_change().fillna(0) + 1
    return df


def get_bankroll_mean_growth(df) -> float:
    """Geometric mean of the bankroll growth."""
    return np.exp(np.log(df["growth"]).mean())


def get_bankroll_risk(df) -> float:
    return df["growth"].std()


def get_bankroll_sharpe_ratio(df) -> float:
    # FIXME: Check if the formula is correct
    return (df["growth"].mean() - 1) / df["growth"].std()


if __name__ == "__main__":
    df_train = open_df(TRAIN_PREDICTION_PATH)
    df_train = compute_kelly_capital(df_train)
    save_df(df_train, TRAIN_EVALUATION_PATH)
    evaluation_dict = {
        "accuracy_score": get_accuracy_score(df_train),
        "log_loss": get_log_loss(df_train),
        "mean_growth": get_bankroll_mean_growth(df_train),
        "risk": get_bankroll_risk(df_train),
        "sharpe_ratio": get_bankroll_sharpe_ratio(df_train),
    }
    save_dict(evaluation_dict, TRAIN_SCORES_PATH)

    df_dev = open_df(DEV_PREDICTION_PATH)
    df_dev = compute_kelly_capital(df_dev)
    save_df(df_dev, DEV_EVALUATION_PATH)
    evaluation_dict = {
        "accuracy_score": get_accuracy_score(df_dev),
        "log_loss": get_log_loss(df_dev),
        "mean_growth": get_bankroll_mean_growth(df_dev),
        "risk": get_bankroll_risk(df_dev),
        "sharpe_ratio": get_bankroll_sharpe_ratio(df_dev),
    }
    save_dict(evaluation_dict, DEV_SCORES_PATH)

    df_test = open_df(TEST_PREDICTION_PATH)
    df_test = compute_kelly_capital(df_test)
    save_df(df_test, TEST_EVALUATION_PATH)
    evaluation_dict = {
        "accuracy_score": get_accuracy_score(df_test),
        "log_loss": get_log_loss(df_test),
        "mean_growth": get_bankroll_mean_growth(df_test),
        "risk": get_bankroll_risk(df_test),
        "sharpe_ratio": get_bankroll_sharpe_ratio(df_test),
    }
    save_dict(evaluation_dict, TEST_SCORES_PATH)
