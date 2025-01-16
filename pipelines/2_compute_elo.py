import sqlite3
import pandas as pd

from tennis_predictor.helpers.elo import update_elo

DATABASE_PATH = './data/silver/tennis_atp/atpdatabase.db'
OUTPUT_PATH = './data/silver/elo.csv'

def compute_elo():
    # Connect to the database
    cnx = sqlite3.connect(DATABASE_PATH)
    # Select oldest matches
    query = "SELECT * FROM matches ORDER BY tourney_date, CAST(match_num AS INT)"
    # Execute the query and load the result into a DataFrame
    df = pd.read_sql_query(query, cnx)
    # Filter df where tourney_date can be cast as int
    df_filtered = df[df['tourney_date'].astype(str).str.isnumeric()]
    
    # Initialize the ELO scores at 1500
    ids = set(df['winner_id'].unique()) | set(df['loser_id'].unique())
    df_elo = pd.DataFrame([[p, '18770701', 0, 1500] for p in ids], columns=['player_id', 'date', 'match_num', 'elo'])

    # Update ELO scores
    for row in df_filtered.iterrows():
        if row[0] % 1000 == 0:
            print(f'Processing row {row[0]}')
            df_elo.to_csv(OUTPUT_PATH, index=False)
        row = row[1]
        winner_id = row['winner_id']  # FIXME: winner_id int or str?
        loser_id = row['loser_id']
        date = row['tourney_date']
        match_num = row['match_num']
        # FIXME: tourney_date and match_num can be equal for different matches on different tournaments
        # FIXME: compute the number of matches played by the player (to filter out new players)
        winner_elo = df_elo.loc[df_elo['player_id'] == winner_id, 'elo'].iloc[-1]  # Get the last ELO score of the player
        loser_elo = df_elo.loc[df_elo['player_id'] == loser_id, 'elo'].iloc[-1]  # Get the last ELO score of the player
        winner_new_elo, loser_new_elo = update_elo(winner_elo, loser_elo)

        new_rows = pd.DataFrame([
            [winner_id, date, match_num, winner_new_elo], 
            [loser_id, date, match_num, loser_new_elo]
        ], columns=['player_id', 'date', 'match_num', 'elo'])
        df_elo = pd.concat([df_elo, new_rows], ignore_index=True)

if __name__ == "__main__":
    compute_elo()
