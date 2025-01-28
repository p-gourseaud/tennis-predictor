import pandas as pd

from tennis_predictor.config.data import (
    DEV_PREDICTION_PATH,
    DEV_START_DATE,
    JOINED_INTERIM_PATH,
    TEST_PREDICTION_PATH,
    TEST_START_DATE,
    TRAIN_PREDICTION_PATH,
)
from tennis_predictor.helpers.data import open_df, save_df


def train_test_split(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split the dataset into train, dev and test sets."""
    df = pd.read_csv(JOINED_INTERIM_PATH)

    df_train = df[df["Date"] < DEV_START_DATE]
    df_dev = df[(df["Date"] >= DEV_START_DATE) & (df["Date"] < TEST_START_DATE)]
    df_test = df[df["Date"] >= TEST_START_DATE]
    return df_train, df_dev, df_test


if __name__ == "__main__":
    df = open_df(JOINED_INTERIM_PATH)
    df_train, df_dev, df_test = train_test_split(df)
    save_df(df_train, TRAIN_PREDICTION_PATH)
    save_df(df_dev, DEV_PREDICTION_PATH)
    save_df(df_test, TEST_PREDICTION_PATH)
