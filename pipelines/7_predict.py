import pandas as pd

from tennis_predictor.helpers.elo import estimate_winrate

INPUT_TRAIN_PATH = "data/gold/train.csv"
INPUT_DEV_PATH = "data/gold/dev.csv"
INPUT_TEST_PATH = "data/gold/test.csv"

OUTPUT_TRAIN_PATH = "data/gold/train_predictions.csv"
OUTPUT_DEV_PATH = "data/gold/dev_predictions.csv"
OUTPUT_TEST_PATH = "data/gold/test_predictions.csv"

def open_dataset(path: str) -> pd.DataFrame:
    """Open the dataset and filter out row with missing ELO."""
    df = pd.read_csv(path)
    return df

def predict_winner(df: pd.DataFrame):
    """Predict winner based on ELO."""
    df["winner_estimated_winrate"] = df[['elo_winner', 'elo_loser']].apply(lambda x: estimate_winrate(*x), axis=1)
    df["loser_estimated_winrate"] = 1 - df["winner_estimated_winrate"]
    df["y"] = 1
    df["y_hat"] = (df["winner_estimated_winrate"] > 0.5).astype(int)
    return df

def compute_kelly_criterion(df: pd.DataFrame):
    """Compute the Kelly criterion."""
    b = (df['AvgW'] - 1)
    p = df['winner_estimated_winrate']
    q = 1 - p
    df["winner_kelly"] = (b*p - q) / b

    b = (df['AvgL'] - 1)
    p, q = q, p
    df["loser_kelly"] = (b*p - q) / b
    return df

def save_predictions(df: pd.DataFrame, path: str) -> None:
    """Save the predictions."""
    df.to_csv(path, index=False)

if __name__ == "__main__":
    df_train = open_dataset(INPUT_TRAIN_PATH)
    df_train = predict_winner(df_train)
    df_train = compute_kelly_criterion(df_train)
    save_predictions(df_train, OUTPUT_TRAIN_PATH)

    df_dev = open_dataset(INPUT_DEV_PATH)
    df_dev = predict_winner(df_dev)
    df_dev = compute_kelly_criterion(df_dev)
    save_predictions(df_dev, OUTPUT_DEV_PATH)

    df_test = open_dataset(INPUT_TEST_PATH)
    df_test = predict_winner(df_test)
    df_test = compute_kelly_criterion(df_test)
    save_predictions(df_test, OUTPUT_TEST_PATH)
