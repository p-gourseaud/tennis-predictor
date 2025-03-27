"""Split the dataset into train, dev and test sets."""

import pandas as pd

from tennis_predictor.config.data import (
    DEV_PATH,
    DEV_START_DATE,
    JOINED_INTERIM_PATH,
    TEST_PATH,
    TEST_START_DATE,
    TRAIN_PATH,
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
    save_df(df_train, TRAIN_PATH)
    save_df(df_dev, DEV_PATH)
    save_df(df_test, TEST_PATH)
