from tqdm import tqdm

K: int = 32 # ELO update constant
BASE_ELO: float = 1500. # Initial ELO score
SPREAD_ELO: int = 400 # ELO update constant

def update_elo(winner_elo: float, loser_elo: float) -> tuple[float, float]:
    """Compute new elo for winner and loser."""
    if winner_elo < 0 or loser_elo < 0:
        raise ValueError("ELO score must be positive.")
    
    E_winner = estimate_winrate(winner_elo, loser_elo)  # Expected score for winner
    E_loser = 1 - E_winner  # Expected score for loser
    winner_new_elo = winner_elo + K * (1 - E_winner)  # New ELO score for winner
    loser_new_elo = loser_elo + K * (0 - E_loser)  # New ELO score for loser
    return winner_new_elo, loser_new_elo

def estimate_winrate(elo1: float, elo2: float) -> float:
    """Compute expected score for player 1 against player 2."""
    if elo1 < 0 or elo2 < 0:
        raise ValueError("ELO score must be positive.")
    
    expected_winrate = 1 / (1 + 10 ** ((elo2 - elo1) / SPREAD_ELO))  # Expected score for player 1
    return expected_winrate
