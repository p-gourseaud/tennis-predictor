"""Script to compute the ELO scores for all players for all matches."""

import pandas as pd

from tennis_predictor.config.data import (
    ELO_COLUMNS,
    ELO_INTERIM_PATH,
)
from tennis_predictor.helpers.data import open_db, save_df
from tennis_predictor.helpers.elo import update_elo


def filter_db(df: pd.DataFrame, surface_type: str) -> pd.DataFrame:
    """Filter the database, keeping only the matches on the specified surface."""
    # Filter df where player_id and tourney_date can be cast as int
    ALLOWED_SURFACES = ["Grass", "Clay", "Hard", "Carpet", "All"]
    surface_type = surface_type.capitalize()
    if surface_type not in ALLOWED_SURFACES:
        raise ValueError(f"surface_type must be one of {ALLOWED_SURFACES}")
    surface_condition = (
        (df["surface"] == surface_type) if surface_type != "All" else True
    )
    df_filtered = df[
        (df["tourney_date"].astype(str).str.isnumeric())  # Remove bad rows
        & (df["winner_id"].astype(str).str.isnumeric())
        & (df["loser_id"].astype(str).str.isnumeric())
        & surface_condition  # Surface condition
    ]
    return df_filtered.reset_index(drop=True)


def initialize_elo(df_matches: pd.DataFrame) -> dict[int, pd.DataFrame]:
    """Initialize the ELO scores at 1500 for all players."""
    ids = set(df_matches["winner_id"].unique()) | set(df_matches["loser_id"].unique())
    dfs_elo = {
        int(p): pd.DataFrame(
            [[int(p), int("18770701"), None, None, 1500.0, int(0)]], columns=ELO_COLUMNS
        )
        for p in ids
    }
    return dfs_elo


def append_elo_row(row: pd.Series, dfs_elo: dict[int, pd.DataFrame]) -> None:
    """Compute 2 ELO rows from 1 match row."""
    winner_id = int(row["winner_id"])
    loser_id = int(row["loser_id"])
    date = int(row["tourney_date"])
    tourney_id = str(row["tourney_id"])
    match_num = int(row["match_num"])

    winner_elo, winner_n_matches = (
        dfs_elo[winner_id].loc[:, ["elo", "n_matches"]].iloc[-1]
    )  # Get the last ELO score of the player
    loser_elo, loser_n_matches = (
        dfs_elo[loser_id].loc[:, ["elo", "n_matches"]].iloc[-1]
    )  # Get the last ELO score of the player
    winner_new_elo, loser_new_elo = update_elo(winner_elo, loser_elo)

    dfs_elo[winner_id] = pd.concat(
        [
            dfs_elo[winner_id],
            pd.DataFrame(
                [
                    [
                        winner_id,
                        date,
                        tourney_id,
                        match_num,
                        winner_new_elo,
                        int(winner_n_matches + 1),
                    ]
                ],
                columns=ELO_COLUMNS,
            ),
        ],
        ignore_index=True,
    )
    dfs_elo[loser_id] = pd.concat(
        [
            dfs_elo[loser_id],
            pd.DataFrame(
                [
                    [
                        loser_id,
                        date,
                        tourney_id,
                        match_num,
                        loser_new_elo,
                        int(loser_n_matches + 1),
                    ]
                ],
                columns=ELO_COLUMNS,
            ),
        ],
        ignore_index=True,
    )


def make_elo_df(dfs_elo: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Make the ELO DataFrame."""
    SORT_COLUMNS = ["date", "tourney_id", "match_num"]
    return pd.concat(list(dfs_elo.values()), ignore_index=True).sort_values(
        by=SORT_COLUMNS
    )


def compute_elo(surface_type: str) -> None:
    """Compute the ELO scores for all matches."""
    SAVE_EVERY = 3000
    df_matches = open_db(
        "SELECT * FROM matches ORDER BY tourney_date, tourney_id, CAST(match_num AS INT)"
    )
    df_matches = filter_db(df_matches, surface_type)
    dfs_elo = initialize_elo(df_matches)
    for row in df_matches.iterrows():
        if row[0] % SAVE_EVERY == 0:
            print(f"Processing row {row[0]}")
            save_df(
                make_elo_df(dfs_elo), ELO_INTERIM_PATH.format(surface_type=surface_type)
            )
        append_elo_row(row[1], dfs_elo)
    save_df(make_elo_df(dfs_elo), ELO_INTERIM_PATH.format(surface_type=surface_type))


# def is_seen_match(row: pd.Series, df_elo: pd.DataFrame) -> bool:
#     """Check if the match is seen."""
#     date = int(row['tourney_date'])
#     tourney_id = str(row['tourney_id'])
#     match_num = int(row['match_num'])
#     return (
#         (df_elo['date'] == date) &
#         (df_elo['tourney_id'] == tourney_id) &
#         (df_elo['match_num'] == match_num)
#     ).any()

# def compute_elo_update():
#     """Compute the ELO score for unseen matches."""
#     # FIXME: Very slow
#     df_matches = open_db()
#     df_elo = pd.read_csv(OUTPUT_PATH, dtype={'player_id': int, 'date': int, 'tourney_id': str, 'match_num': float, 'elo': float, 'n_matches': float})
#     for row in df_matches.iterrows():
#         if row[0] % 1000 == 0:
#             print(f'Processing row {row[0]}')
#         if is_seen_match(row[1], df_elo):
#             continue
#         if row[0] % 1000 == 0:
#             df_elo.to_csv(OUTPUT_PATH, index=False)
#         df_elo = compute_elo_row(row[1], df_elo)
#     df_elo.to_csv(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    compute_elo(surface_type="Grass")
    compute_elo(surface_type="Clay")
    compute_elo(surface_type="Hard")
    compute_elo(surface_type="Carpet")
    compute_elo(surface_type="All")
