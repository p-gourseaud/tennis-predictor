from dataclasses import dataclass


@dataclass
class BestHyperParameters:
    """
    Parameters for the tennis predictor model.
    """

    # Model parameters
    alpha: int = 17
    max_depth: int = 4
    n_estimators: int = 100
