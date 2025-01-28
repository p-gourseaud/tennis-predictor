import pandas as pd

from tennis_predictor.config.data import (
    DEV_PREDICTION_PATH,
    DEV_START_DATE,
    JOINED_INTERIM_PATH,
    TEST_PREDICTION_PATH,
    TEST_START_DATE,
    TRAIN_PREDICTION_PATH,
)


def train_test_split() -> None:
    df = pd.read_csv(JOINED_INTERIM_PATH)

    df_train = df[df["Date"] < DEV_START_DATE]
    df_dev = df[(df["Date"] >= DEV_START_DATE) & (df["Date"] < TEST_START_DATE)]
    df_test = df[df["Date"] >= TEST_START_DATE]

    df_train.to_csv(TRAIN_PREDICTION_PATH, index=False)
    df_dev.to_csv(DEV_PREDICTION_PATH, index=False)
    df_test.to_csv(TEST_PREDICTION_PATH, index=False)


if __name__ == "__main__":
    train_test_split()
