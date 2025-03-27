"""Helper functions to load and save data."""

import json
import sqlite3

import pandas as pd

from tennis_predictor.config.data import (
    TENNIS_ATP_DATABASE_PATH,
)


def open_db(query: str) -> pd.DataFrame:
    """Open the database and return the query result."""
    # Connect to the database
    cnx = sqlite3.connect(TENNIS_ATP_DATABASE_PATH)
    # Execute the query and load the result into a DataFrame
    df = pd.read_sql_query(query, cnx)
    return df


def open_df(path: str) -> pd.DataFrame:
    """Open the DataFrame from a CSV file."""
    return pd.read_csv(path)


def save_df(df: pd.DataFrame, path: str) -> None:
    """Save the DataFrame to a CSV file."""
    df.to_csv(path, index=False)


def save_dict(evaluation_dict, path):
    with open(path, "w") as f:
        json.dump(evaluation_dict, f, indent=4)
