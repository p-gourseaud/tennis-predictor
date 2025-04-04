"""Join the rank and ELO of a player for a match according to the date."""

import multiprocessing
from functools import partial

import pandas as pd

from tennis_predictor.config.data import (
    ELO_INTERIM_PATH,
    JOINED_INTERIM_PATH,
    ODDS_INTERIM_PATH,
)
from tennis_predictor.helpers.data import open_df, save_df  # open_db


def filter_rank(df_ranks: pd.DataFrame) -> pd.DataFrame:
    # Remove rows with bad values
    df_filtered = df_ranks[
        (df_ranks["date"].astype(str).str.isnumeric())
    ]  # Remove bad rows
    df_filtered["date"] = df_filtered["date"].astype(int)
    return df_filtered.reset_index(drop=True)


def open_elo(surface_type: str) -> pd.DataFrame:
    """Open ELO dataset."""
    ALLOWED_SURFACES = ["Grass", "Clay", "Hard", "Carpet", "All"]
    surface_type = surface_type.capitalize()
    if surface_type not in ALLOWED_SURFACES:
        raise ValueError(f"surface_type must be one of {ALLOWED_SURFACES}")
    return open_df(ELO_INTERIM_PATH.format(surface_type=surface_type))


def _find_latest_rank(
    df_rank: pd.DataFrame, iter_row: tuple[int, pd.Series], winner: bool = True
) -> tuple[int, int]:
    """Given a row, find the latest rank and points of the player."""
    i, row = iter_row
    if i % 1000 == 0:
        print(f"Processing row {i}...")  # TODO: Use log.info
    date = row["Date"]
    date = int(date.replace("-", ""))
    if winner:
        id_ = row["id"]
    else:
        id_ = row["id_loser"]

    try:
        rank, points = df_rank.loc[
            (df_rank["player_id"] == id_) & (df_rank["date"] < date), ["pos", "pts"]
        ].iloc[-1]
    except IndexError:
        rank, points = 0, 0
    return rank, points


def join_rank(df_odds: pd.DataFrame, df_rank: pd.DataFrame) -> pd.DataFrame:
    """Join the rank and points of a player for a match according to the date."""
    rank_winners: list[int] = []
    points_winners: list[int] = []
    rank_losers: list[int] = []
    points_losers: list[int] = []

    # Use multiprocessing to speed up rank search
    partial_find_latest_rank = partial(_find_latest_rank, df_rank, winner=True)
    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        res = pool.map(partial_find_latest_rank, df_odds.iterrows())
    rank_winners, points_winners = zip(*res)  # type: ignore

    partial_find_latest_rank = partial(_find_latest_rank, df_rank, winner=False)
    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        res = pool.map(partial_find_latest_rank, df_odds.iterrows())
    rank_losers, points_losers = zip(*res)  # type: ignore

    df_odds["rank_winner"] = rank_winners
    df_odds["points_winner"] = points_winners
    df_odds["rank_loser"] = rank_losers
    df_odds["points_loser"] = points_losers
    return df_odds


def _find_latest_elo(
    df_elo: pd.DataFrame,
    df_elo_carpet: pd.DataFrame,
    df_elo_clay: pd.DataFrame,
    df_elo_grass: pd.DataFrame,
    df_elo_hard: pd.DataFrame,
    iter_row: tuple[int, pd.Series],
    winner: bool = True,
) -> tuple[float, float]:
    """Given a row, find the latest ELO of the player (all / surface)."""
    # TODO: Add ELO Outdoor / Indoor
    i, row = iter_row
    if i % 1000 == 0:
        print(f"Processing row {i}...")
    date = row["Date"]
    date = int(date.replace("-", ""))
    surface = row["Surface"]
    if surface == "Carpet":
        df_elo_surface = df_elo_carpet
    elif surface == "Clay":
        df_elo_surface = df_elo_clay
    elif surface == "Grass":
        df_elo_surface = df_elo_grass
    elif surface == "Hard":
        df_elo_surface = df_elo_hard
    else:
        df_elo_surface = pd.DataFrame()

    if winner:
        id_ = row["id"]
    else:
        id_ = row["id_loser"]

    try:
        elo: float = df_elo.loc[
            (df_elo["player_id"] == id_) & (df_elo["date"] < date), "elo"
        ].iloc[-1]
    except IndexError:
        elo = 1500.0

    try:
        elo_surface: float = df_elo_surface.loc[
            (df_elo["player_id"] == id_) & (df_elo["date"] < date), "elo"
        ].iloc[-1]
    except IndexError:
        elo_surface = 1500.0
    return elo, elo_surface


def join_elo(
    df_odds: pd.DataFrame,
    df_elo: pd.DataFrame,
    df_elo_carpet: pd.DataFrame,
    df_elo_clay: pd.DataFrame,
    df_elo_grass: pd.DataFrame,
    df_elo_hard: pd.DataFrame,
) -> pd.DataFrame:
    """Join the ELO of a player for a match according to the date and surface."""
    elo_winners: list[float] = []
    elo_surface_winners: list[float] = []
    elo_losers: list[float] = []
    elo_surface_losers: list[float] = []

    # Use multiprocessing to speed up ELO search
    # Find ELO for winners
    partial_find_latest_elo = partial(
        _find_latest_elo,
        df_elo,
        df_elo_carpet,
        df_elo_clay,
        df_elo_grass,
        df_elo_hard,
        winner=True,
    )
    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        res = pool.map(partial_find_latest_elo, df_odds.iterrows())
    elo_winners, elo_surface_winners = zip(*res)  # type: ignore

    # Find ELO for losers
    partial_find_latest_elo = partial(
        _find_latest_elo,
        df_elo,
        df_elo_carpet,
        df_elo_clay,
        df_elo_grass,
        df_elo_hard,
        winner=False,
    )
    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        res = pool.map(partial_find_latest_elo, df_odds.iterrows())
    elo_losers, elo_surface_losers = zip(*res)  # type: ignore

    df_odds["elo_winner"] = elo_winners
    df_odds["elo_surface_winner"] = elo_surface_winners
    df_odds["elo_loser"] = elo_losers
    df_odds["elo_surface_loser"] = elo_surface_losers
    return df_odds


# Take odds.csv
# Join rank and points on date
# Join ELO
# Join ELO on Surface
# Train_dev_test_split
# Save

if __name__ == "__main__":
    df_odds = open_df(ODDS_INTERIM_PATH)
    # FIXME: Ranks and points are redundant in the dataset but are not exactly the same: investigate
    # df_rank = open_db("SELECT * FROM ranking")
    # df_rank = filter_rank(df_rank)
    # df_joined = join_rank(df_odds, df_rank)

    df_elo = open_elo("all")
    df_elo_carpet = open_elo("carpet")
    df_elo_clay = open_elo("clay")
    df_elo_grass = open_elo("grass")
    df_elo_hard = open_elo("hard")
    df_joined = join_elo(
        df_odds, df_elo, df_elo_carpet, df_elo_clay, df_elo_grass, df_elo_hard
    )
    save_df(df_joined, JOINED_INTERIM_PATH)
