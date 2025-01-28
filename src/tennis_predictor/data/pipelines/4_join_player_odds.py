import warnings

import pandas as pd


PLAYER_PATH = './data/silver/tennis_atp/players.csv'
ODDS_FOLDER = './data/bronze/tennis_odds'
XLS_MEN = list(range(2001, 2013))
XLS_WOMEN = list(range(2007, 2013))
XLSX = list(range(2013, 2026))
OUTPUT_PATH = './data/silver/tennis_odds/odds.csv'

def open_odds() -> pd.DataFrame:
    """Open and concat all odds files."""
    dfs = []
    for year in XLS_MEN:
        df = pd.read_excel(f"{ODDS_FOLDER}/{year}.xls")
        dfs.append(df)
    for year in XLS_WOMEN:
        df = pd.read_excel(f"{ODDS_FOLDER}/women_{year}.xls")
        dfs.append(df)
    for year in XLSX:
        df = pd.read_excel(f"{ODDS_FOLDER}/{year}.xlsx")
        dfs.append(df)
        df = pd.read_excel(f"{ODDS_FOLDER}/women_{year}.xlsx")
        dfs.append(df)
    return pd.concat(dfs)

def open_players() -> pd.DataFrame:
    """Open the players dataset."""
    return pd.read_csv(PLAYER_PATH)

def filter_unique(df: pd.DataFrame) -> pd.DataFrame:
    """Remove players having the same shortName (for join purposes)."""
    df_count = df.groupby('shortName')['id'].count()
    df_count_one = df_count[df_count == 1]
    df_unique = df.merge(df_count_one, on='shortName', how='right', suffixes=['', '_y']).drop(columns=['id_y'])
    return df_unique

def join(df_odds: pd.DataFrame, df_players: pd.DataFrame) -> pd.DataFrame:
    df_joined = (
        df_odds
        .merge(df_players, left_on='Winner', right_on='shortName', how='left', suffixes=['', '_winner'], indicator=True)
        .rename(columns={'_merge': '_merge_winner'})
        .merge(df_players, left_on='Loser', right_on='shortName', how='left', suffixes=['', '_loser'], indicator=True)
    )
    # Count the number of matches without joined players
    # FIXME: Find every players for every matches
    n_lost = df_joined[
        (df_joined['_merge'] == 'left_only') 
        | (df_joined['_merge_winner'] == 'left_only')
    ].shape[0]
    warnings.warn(f"{n_lost} matches haven't find their joined players.")

    # Return inner selection
    df_final = df_joined[
        (df_joined['_merge'] == 'both') 
        & (df_joined['_merge_winner'] == 'both')
    ].drop(columns=['_merge', '_merge_winner'])
    return df_final

def save(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    df_odds = open_odds()
    df_players = open_players()
    df_unique = filter_unique(df_players)
    df_joined = join(df_odds, df_unique)
    save(df_joined)