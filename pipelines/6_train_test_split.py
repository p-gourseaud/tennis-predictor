import pandas as pd

INPUT_PATH = "data/silver/joined_dataset.csv"
OUTPUT_TRAIN_PATH = "data/gold/train.csv"
OUTPUT_DEV_PATH = "data/gold/dev.csv"
OUTPUT_TEST_PATH = "data/gold/test.csv"
DEV_CUTOFF_DATE = "2023-01-01"
TEST_CUTOFF_DATE = "2024-01-01"

def train_test_split() -> None:
    df = pd.read_csv(INPUT_PATH)

    df_train = df[df["Date"] < DEV_CUTOFF_DATE]
    df_dev = df[(df["Date"] >= DEV_CUTOFF_DATE) & (df["Date"] < TEST_CUTOFF_DATE)]
    df_test = df[df["Date"] >= TEST_CUTOFF_DATE]

    df_train.to_csv(OUTPUT_TRAIN_PATH, index=False)
    df_dev.to_csv(OUTPUT_DEV_PATH, index=False)
    df_test.to_csv(OUTPUT_TEST_PATH, index=False)

if __name__ == "__main__":
    train_test_split()