"""Main module to advise on betting on a tennis match."""

import click
import pandas as pd

from tennis_predictor.config.data import ELO_INTERIM_PATH, JOINED_INTERIM_PATH
from tennis_predictor.helpers.elo import estimate_winrate


def get_id_player(player: str, df_matches: pd.DataFrame) -> int:
    try:
        id_player = int(df_matches[df_matches["Winner"] == player]["id"].iloc[0])
    except IndexError:
        try:
            id_player = int(
                df_matches[df_matches["Loser"] == player]["id_loser"].iloc[0]
            )
        except IndexError as e:
            print(f"Player {player} not found")
            # TODO: Show similar names
            raise e
    return id_player


def get_latest_elo_player(player_id: int, df_elo: pd.DataFrame) -> float:
    try:
        elo, n_matches = df_elo[df_elo["player_id"] == player_id].iloc[-1][
            ["elo", "n_matches"]
        ]
    except IndexError as e:
        print(f"Player {player_id} not found")
        raise e
    print(f"Player {player_id} has ELO {int(elo)} with {n_matches} matches")
    return elo


def get_match_bet_recommandation(
    player1: str,
    player2: str,
    odds1: float,
    odds2: float,
    df_matches: pd.DataFrame,
    df_elo: pd.DataFrame,
) -> None:
    id_player1 = get_id_player(player1, df_matches)
    id_player2 = get_id_player(player2, df_matches)

    elo1 = get_latest_elo_player(id_player1, df_elo)
    elo2 = get_latest_elo_player(id_player2, df_elo)

    p = estimate_winrate(elo1, elo2)
    print(f"{player1} has a {p*100:.1f}% estimated winrate.")

    b = odds1 - 1
    q = 1 - p
    f1 = (b * p - q) / b

    b = odds2 - 1
    f2 = (b * q - p) / b
    if f1 > 0:
        print(f"We should bet {f1*100:.1f}% of our bankroll on {player1}.")
    elif f2 > 0:
        print(f"We should bet {f2*100:.1f}% of our bankroll on {player2}.")
    else:
        print(
            f"We should not bet on this match. (f1 = {f1*100:.1f}%, f2 = {f2*100:.1f}%)"
        )


# Python function
def advise(player1, player2, odds1, odds2):
    df_matches = pd.read_csv(JOINED_INTERIM_PATH, low_memory=False)
    df_elo = pd.read_csv(ELO_INTERIM_PATH.format(surface_type="All"))
    get_match_bet_recommandation(player1, player2, odds1, odds2, df_matches, df_elo)


# Command line interface
@click.command()
@click.option("--player1", help="First player", required=True, type=str, prompt=True)
@click.option("--player2", help="Second player", required=True, type=str, prompt=True)
@click.option(
    "--odds1", help="Odds for the first player", required=True, type=float, prompt=True
)
@click.option(
    "--odds2", help="Odds for the second player", required=True, type=float, prompt=True
)
def advise_cli(player1, player2, odds1, odds2):
    advise(player1, player2, odds1, odds2)


if __name__ == "__main__":
    advise_cli()
