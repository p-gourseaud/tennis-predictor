# TODO: Refactor as read / preprocess / merge
# TODO: Improve merge to keep more rows
import pandas as pd

train_years = list(range(2015, 2023))
test_years = [2023]


def get_short_name(name: str) -> str:
    # TODO: Improve, we miss somes players this way.
    names = name.split(" ")
    short_name = f"{names[-1]} {names[0][0]}."
    return short_name


def to_date(date: int) -> str:
    date_str = str(date)
    date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    return date_str


def get_train():
    dfs_match = []
    dfs_odds = []
    for y in train_years:
        dfs_match.append(pd.read_csv(f"./data/bronze/tennis_atp/atp_matches_{y}.csv"))
        dfs_odds.append(pd.read_excel(f"./data/bronze/tennis_odds/{y}.xlsx"))
    df_train_match = pd.concat(dfs_match, ignore_index=True)
    df_train_odds = pd.concat(dfs_odds, ignore_index=True)

    df_train_match.winner_name = df_train_match.winner_name.apply(get_short_name)
    df_train_match.loser_name = df_train_match.loser_name.apply(get_short_name)
    df_train_match.tourney_date = pd.to_datetime(
        df_train_match.tourney_date.apply(to_date)
    )

    df_train = pd.merge(
        df_train_match,
        df_train_odds,
        left_on=["winner_name", "loser_name", "tourney_date"],
        right_on=["Winner", "Loser", "Date"],
    )
    return df_train


def get_test():
    dfs_match = []
    dfs_odds = []
    for y in test_years:
        dfs_match.append(pd.read_csv(f"./data/bronze/tennis_atp/atp_matches_{y}.csv"))
        dfs_odds.append(pd.read_excel(f"./data/bronze/tennis_odds/{y}.xlsx"))
    df_test_match = pd.concat(dfs_match, ignore_index=True)
    df_test_odds = pd.concat(dfs_odds, ignore_index=True)

    df_test_match.winner_name = df_test_match.winner_name.apply(get_short_name)
    df_test_match.loser_name = df_test_match.loser_name.apply(get_short_name)
    df_test_match.tourney_date = pd.to_datetime(
        df_test_match.tourney_date.apply(to_date)
    )

    df_test = pd.merge(
        df_test_match,
        df_test_odds,
        left_on=["winner_name", "loser_name", "tourney_date"],
        right_on=["Winner", "Loser", "Date"],
    )
    return df_test


if __name__ == "__main__":
    train = get_train()
    test = get_test()

    train.to_csv("./data/silver/train.csv", index=False)
    test.to_csv("./data/silver/test.csv", index=False)
