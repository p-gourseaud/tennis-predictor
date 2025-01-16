import pytest

from tennis_predictor.helpers.elo import update_elo

def test_update_elo():
    elo1 = 1500
    elo2 = 1500
    elo1_new, elo2_new = update_elo(elo1, elo2)
    assert elo1_new == 1516
    assert elo2_new == 1484
