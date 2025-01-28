import sqlite3

import pandas as pd

from tennis_predictor.helpers.odds import make_shortname

DATABASE_PATH = "./data/silver/tennis_atp/atpdatabase.db"
OUTPUT_PATH = "./data/silver/tennis_atp/players.csv"


def open_db() -> pd.DataFrame:
    """Open the database and return the players."""
    # Connect to the database
    cnx = sqlite3.connect(DATABASE_PATH)
    # Select sorted matches
    query = "SELECT * FROM player"
    # Execute the query and load the result into a DataFrame
    df_players = pd.read_sql_query(query, cnx)
    # Remove the first row which is bad values
    df_players = df_players.iloc[1:, :]
    # TODO: Filtering on young players make less duplicates therefore more odds joined (61k lost instead of 65k)
    # df_players_young = df_players[df_players['birth'] >= '19700101']
    return df_players


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Make shortNames for players: Ludvig Aaes => Aaes L."""
    df = make_shortname(df)
    return df


def save(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    df_players = open_db()
    df_shortnames = transform(df_players)
    # df_unique = filter_unique(df_shortnames)
    save(df_shortnames)
