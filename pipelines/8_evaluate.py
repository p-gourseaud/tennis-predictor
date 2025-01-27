import json

import numpy as np
import pandas as pd

from tennis_predictor.helpers.elo import estimate_winrate
from sklearn.metrics import accuracy_score, log_loss

INPUT_TRAIN_PATH = "data/gold/train_predictions.csv"
INPUT_DEV_PATH = "data/gold/dev_predictions.csv"
INPUT_TEST_PATH = "data/gold/test_predictions.csv"

OUTPUT_DF_TRAIN_PATH = "data/gold/train_evaluation.csv"
OUTPUT_DF_DEV_PATH = "data/gold/dev_evaluation.csv"
OUTPUT_DF_TEST_PATH = "data/gold/test_evaluation.csv"

OUTPUT_JSON_TRAIN_PATH = "data/gold/train_evaluation.json"
OUTPUT_JSON_DEV_PATH = "data/gold/dev_evaluation.json"
OUTPUT_JSON_TEST_PATH = "data/gold/test_evaluation.json"


def open_dataset(path: str) -> pd.DataFrame:
    """Open the dataset and filter out row with missing ELO."""
    df = pd.read_csv(path)
    return df

def get_accuracy_score(df) -> float:
    return accuracy_score(df['y'], df['y_hat'])

def get_log_loss(df) -> float:
    return log_loss(df['y'], df['winner_estimated_winrate'], labels=[0, 1])

def compute_kelly_capital(df):
    capital = 1
    # MAX_BET = 25000  # Gain maximal : 550 000€ avec côte de 20

    bets = []
    capitals = []

    for row in df.iterrows():
        winner_kelly, loser_kelly = row[1][['winner_kelly', 'loser_kelly']]
        if winner_kelly > 0:
            # Pari gagnant
            bet = capital * winner_kelly  # min(capital * winner_kelly, MAX_BET)
            capital += bet * (row[1]['AvgW'] - 1)
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
    df['bets'] = bets
    df['capitals'] = capitals
    # TODO: Compute bankroll growth
    df['growth'] = df['capitals'].pct_change().fillna(0) + 1
    return df

def get_bankroll_mean_growth(df) -> float:
    """Geometric mean of the bankroll growth."""
    return np.exp(np.log(df['growth']).mean())

def get_bankroll_risk(df) -> float:
    return df['growth'].std()

def get_bankroll_sharpe_ratio(df) -> float:
    # FIXME: Check if the formula is correct
    return (df['growth'].mean() - 1) / df['growth'].std()

def save_evaluation_df(df, path):
    df.to_csv(path, index=False)

def save_evaluation_dict(evaluation_dict, path):
    with open(path, 'w') as f:
        json.dump(evaluation_dict, f, indent=4)

if __name__ == "__main__":
    df_train = open_dataset(INPUT_TRAIN_PATH)
    df_train = compute_kelly_capital(df_train)
    save_evaluation_df(df_train, OUTPUT_DF_TRAIN_PATH)
    evaluation_dict = {
        'accuracy_score': get_accuracy_score(df_train),
        'log_loss': get_log_loss(df_train),
        'mean_growth': get_bankroll_mean_growth(df_train),
        'risk': get_bankroll_risk(df_train),
        'sharpe_ratio': get_bankroll_sharpe_ratio(df_train),
    }
    save_evaluation_dict(evaluation_dict, OUTPUT_JSON_TRAIN_PATH)

    df_dev = open_dataset(INPUT_DEV_PATH)
    df_dev = compute_kelly_capital(df_dev)
    save_evaluation_df(df_dev, OUTPUT_DF_DEV_PATH)
    evaluation_dict = {
        'accuracy_score': get_accuracy_score(df_dev),
        'log_loss': get_log_loss(df_dev),
        'mean_growth': get_bankroll_mean_growth(df_dev),
        'risk': get_bankroll_risk(df_dev),
        'sharpe_ratio': get_bankroll_sharpe_ratio(df_dev),
    }
    save_evaluation_dict(evaluation_dict, OUTPUT_JSON_DEV_PATH)

    df_test = open_dataset(INPUT_TEST_PATH)
    df_test = compute_kelly_capital(df_test)
    save_evaluation_df(df_test, OUTPUT_DF_TEST_PATH)
    evaluation_dict = {
        'accuracy_score': get_accuracy_score(df_test),
        'log_loss': get_log_loss(df_test),
        'mean_growth': get_bankroll_mean_growth(df_test),
        'risk': get_bankroll_risk(df_test),
        'sharpe_ratio': get_bankroll_sharpe_ratio(df_test),
    }
    save_evaluation_dict(evaluation_dict, OUTPUT_JSON_TEST_PATH)