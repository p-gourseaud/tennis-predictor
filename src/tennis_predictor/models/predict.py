"""Predict the winner of a tennis match based on ELO."""

import pickle

import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder

from tennis_predictor.config.columns import COLUMNS_TO_ENCODE, FEATURES
from tennis_predictor.config.data import (
    DEV_PATH,
    DEV_PREDICTION_PATH,
    ENCODER_PATH,
    MEDIAN_PATH,
    MODEL_PATH,
    TEST_PATH,
    TEST_PREDICTION_PATH,
    TRAIN_PATH,
    TRAIN_PREDICTION_PATH,
)
from tennis_predictor.helpers.data import open_df, save_df


def preprocess(df: pd.DataFrame):
    """Preprocess the data."""
    X = df[FEATURES]
    # One-hot encode the categorical features
    with open(ENCODER_PATH, "rb") as f:
        encoder: OneHotEncoder = pickle.load(f)
    # Create a DataFrame with the encoded columns
    encoded_df = pd.DataFrame(
        encoder.transform(X[COLUMNS_TO_ENCODE]),
        columns=encoder.get_feature_names_out(COLUMNS_TO_ENCODE),
    )
    # Concatenate the encoded columns with the original dataframe
    X_encoded = pd.concat([X.drop(COLUMNS_TO_ENCODE, axis=1), encoded_df], axis=1)

    features2 = sorted(set(FEATURES) - set(COLUMNS_TO_ENCODE) | set(encoded_df.columns))
    X_encoded = X_encoded[features2]
    # Fill missing values with the median
    with open(MEDIAN_PATH, "rb") as f:
        medians = pickle.load(f)
    X_filled = X_encoded.fillna(medians)
    return X_filled


def predict_winner(df: pd.DataFrame):
    """Predict winner with XGBoost model."""
    X_filled = preprocess(df)
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(MODEL_PATH)
    y_pred = xgb_model.predict(X_filled)
    y_pred_proba = xgb_model.predict_proba(X_filled)
    df["y_hat"] = y_pred
    df["winner_estimated_winrate"] = y_pred_proba[:, 1]
    df["loser_estimated_winrate"] = 1 - df["winner_estimated_winrate"]
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
