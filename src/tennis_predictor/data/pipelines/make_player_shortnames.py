"""Make shortNames for players, eg: Ludvig Aaes => Aaes L.

Required for joining the player dataset with the odds dataset.
"""

import pandas as pd

from tennis_predictor.config.data import PLAYERS_INTERIM_PATH
from tennis_predictor.helpers.data import open_db, save_df
from tennis_predictor.helpers.odds import make_shortname


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Make shortNames for players, eg: Ludvig Aaes => Aaes L."""
    df = make_shortname(df)
    return df


if __name__ == "__main__":
    df_players = open_db("SELECT * FROM player")
    df_players = df_players.iloc[1:, :]
    df_shortnames = transform(df_players)  # Remove the first row which is bad values
    # df_unique = filter_unique(df_shortnames)
    save_df(df_shortnames, PLAYERS_INTERIM_PATH)
