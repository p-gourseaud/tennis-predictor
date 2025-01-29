"""Configuration file for data paths."""

# External
# # Tennis ATP
TENNIS_ATP_EXTERNAL_FOLDER = "./data/external/tennis_atp/"
SQLITE_SCRIPT_PATH = "./examples/SQLite/convert_sqlite.sh"
PATH_BACKTRACK = "../../.."
# # Tennis Odds
ODDS_EXTERNAL_FOLDER = "./data/external/tennis_odds"
ODDS_XLS_MEN_YEAR_RANGE = list(range(2001, 2013))
ODDS_XLS_WOMEN_YEAR_RANGE = list(range(2007, 2013))
ODDS_XLSX_YEAR_RANGE = list(range(2013, 2026))

# Intermediate
# # Tennis ATP
TENNIS_ATP_DB_NAME = "atpdatabase.db"
TENNIS_ATP_INTERIM_FOLDER = "./data/interim/tennis_atp/"
TENNIS_ATP_DATABASE_PATH = TENNIS_ATP_INTERIM_FOLDER + TENNIS_ATP_DB_NAME
# # # Players
PLAYERS_INTERIM_PATH = "./data/interim/tennis_atp/players.csv"
# # # Tennis Elo
ELO_INTERIM_PATH = "./data/interim/elo/elo_{surface_type}.csv"
ELO_COLUMNS = ["player_id", "date", "tourney_id", "match_num", "elo", "n_matches"]
# # Tennis Odds
ODDS_INTERIM_PATH = "./data/interim/tennis_odds/odds.csv"
# # Joined
JOINED_INTERIM_PATH = "./data/interim/joined_dataset.csv"

# Processed
# # Input
TRAIN_PATH = "data/processed/train.csv"
DEV_PATH = "data/processed/dev.csv"
TEST_PATH = "data/processed/test.csv"
DEV_START_DATE = "2023-01-01"
TEST_START_DATE = "2024-01-01"
# # Prediction
TRAIN_PREDICTION_PATH = "data/processed/train_predictions.csv"
DEV_PREDICTION_PATH = "data/processed/dev_predictions.csv"
TEST_PREDICTION_PATH = "data/processed/test_predictions.csv"
# # Evaluation
TRAIN_EVALUATION_PATH = "data/processed/train_evaluation.csv"
DEV_EVALUATION_PATH = "data/processed/dev_evaluation.csv"
TEST_EVALUATION_PATH = "data/processed/test_evaluation.csv"
TRAIN_SCORES_PATH = "data/processed/train_scores.json"
DEV_SCORES_PATH = "data/processed/dev_scores.json"
TEST_SCORES_PATH = "data/processed/test_scores.json"
