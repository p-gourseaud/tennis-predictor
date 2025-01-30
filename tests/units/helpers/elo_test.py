import pytest

from tennis_predictor.helpers.elo import estimate_winrate, update_elo


def test_update_elo():
    elo1 = 1500
    elo2 = 1500
    elo1_new, elo2_new = update_elo(elo1, elo2, 0, 0)
    assert elo1_new == pytest.approx(1565.6, 0.01)
    assert elo2_new == pytest.approx(1434.3, 0.01)

    elo1 = 1500
    elo2 = 1500
    elo1_new, elo2_new = update_elo(elo1, elo2, 1000, 1000)
    assert elo1_new == pytest.approx(1507.9, 0.01)
    assert elo2_new == pytest.approx(1492.1, 0.01)


def test_compute_expected_winrate():
    elo1 = 1500
    elo2 = 1600
    E_winrate = estimate_winrate(elo1, elo2)
    assert E_winrate == pytest.approx(0.36, 0.01)
