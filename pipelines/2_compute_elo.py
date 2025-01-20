import sqlite3
import pandas as pd

from tennis_predictor.helpers.elo import update_elo

DATABASE_PATH = './data/silver/tennis_atp/atpdatabase.db'
OUTPUT_PATH = './data/silver/elo_any.csv'
COLUMNS = ['player_id', 'date', 'tourney_id', 'match_num', 'elo', 'n_matches']

def open_db() -> pd.DataFrame:
    # Connect to the database
    cnx = sqlite3.connect(DATABASE_PATH)
    # Select sorted matches
    query = "SELECT * FROM matches ORDER BY tourney_date, tourney_id, CAST(match_num AS INT)"
    # Execute the query and load the result into a DataFrame
    df = pd.read_sql_query(query, cnx)
    # Filter df where player_id and tourney_date can be cast as int
    df_filtered = df[
        (df['tourney_date'].astype(str).str.isnumeric())
        & (df['winner_id'].astype(str).str.isnumeric())
        & (df['loser_id'].astype(str).str.isnumeric())
    ]
    return df_filtered

def initialize_elo(df_matches: pd.DataFrame = open_db()) -> pd.DataFrame:
    # Initialize the ELO scores at 1500
    ids = set(df_matches['winner_id'].unique()) | set(df_matches['loser_id'].unique())
    df_elo = pd.DataFrame([[str(p), '18770701', None, None, 1500, 0] for p in ids], columns=COLUMNS)
    return df_elo

def update_elo_row(row: pd.Series, df_elo: pd.DataFrame) -> pd.DataFrame:
    winner_id = str(row['winner_id'])
    loser_id = str(row['loser_id'])
    date = str(row['tourney_date'])
    tourney_id = str(row['tourney_id'])
    match_num = str(row['match_num'])
    winner_elo, winner_n_matches = df_elo.loc[df_elo['player_id'] == winner_id, ['elo', 'n_matches']].iloc[-1]  # Get the last ELO score of the player
    loser_elo, loser_n_matches = df_elo.loc[df_elo['player_id'] == loser_id, ['elo', 'n_matches']].iloc[-1]  # Get the last ELO score of the player
    winner_new_elo, loser_new_elo = update_elo(winner_elo, loser_elo)

    new_rows = pd.DataFrame([
        [winner_id, date, tourney_id, match_num, winner_new_elo, winner_n_matches + 1], 
        [loser_id, date, tourney_id, match_num, loser_new_elo, loser_n_matches + 1]
    ], columns=COLUMNS)
    df_elo = pd.concat([df_elo, new_rows], ignore_index=True)
    return df_elo

if __name__ == "__main__":
    df_matches = open_db()
    df_elo = initialize_elo(df_matches)
    for row in df_matches.iterrows():
        if row[0] % 1000 == 0:
            print(f'Processing row {row[0]}')
            df_elo.to_csv(OUTPUT_PATH, index=False)
        df_elo = update_elo_row(row[1], df_elo)
    df_elo.to_csv(OUTPUT_PATH, index=False)
