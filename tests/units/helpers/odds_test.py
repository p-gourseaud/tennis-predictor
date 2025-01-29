import pandas as pd
from pandas.testing import assert_frame_equal

from tennis_predictor.helpers.odds import _abbreviate_name, make_shortname


def test_abbreviate():
    assert _abbreviate_name("Danilo") == "D."
    assert _abbreviate_name("Danilo", n_chars=2) == "Da."
    assert _abbreviate_name("Lee Sin") == "L.S."


def test_make_shortname():
    df_input = pd.DataFrame(
        [
            [1, "Danilo", "Acosta"],
            [2, "Dario", "Acosta"],
            [3, "Diego", "Acosta"],
            [4, "Abdul", "Ahmed"],
            [5, "Jose", "Antelo"],
            [6, "Jose", "Antelo"],
            [7, "Seoung Hun", "Lee"],
            [8, "J M", "del Potro"],
        ],
        columns=["id", "firstName", "lastName"],
    )
    df_output = pd.DataFrame(
        [
            [1, "Danilo", "Acosta", "Acosta Dan."],
            [2, "Dario", "Acosta", "Acosta Dar."],
            [3, "Diego", "Acosta", "Acosta Di."],
            [4, "Abdul", "Ahmed", "Ahmed A."],
            [5, "Jose", "Antelo", "Antelo Jose."],  # Same long shortname for same name
            [6, "Jose", "Antelo", "Antelo Jose."],  # Same long shortname for same name
            [7, "Seoung Hun", "Lee", "Lee S.H."],
            [8, "J M", "del Potro", "Del Potro J.M."],  # Titled name with particule
        ],
        columns=["id", "firstName", "lastName", "shortName"],
    )
    df_result = make_shortname(df_input)
    assert_frame_equal(df_result, df_output)
