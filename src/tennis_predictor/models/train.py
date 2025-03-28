"""Train the model."""

import pickle

import pandas as pd
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder

from tennis_predictor.config.columns import COLUMNS_TO_ENCODE, FEATURES
from tennis_predictor.config.data import (
    ENCODER_PATH,
    MEDIAN_PATH,
    MODEL_PATH,
    TRAIN_AUGMENTED_PATH,
)
from tennis_predictor.config.parameters import BEST_HYPER_PARAMETERS
from tennis_predictor.helpers.data import open_df


def make_one_hot_encoding(df):
    """One-hot encode the categorical features."""
    # FIXME: Fit on train and transform on train, dev and test as a model
    # FIXME: Use on df_train[features]
    # FIXME: save model to use on df_dev and df_test
    # Select the columns to encode

    # Initialize the OneHotEncoder
    encoder = OneHotEncoder(
        sparse_output=False, drop="first", handle_unknown="ignore"
    )  # drop='first' to avoid multicollinearity
    # Fit and transform the selected columns
    encoded_columns = encoder.fit_transform(df[COLUMNS_TO_ENCODE])
    # Create a DataFrame with the encoded columns
    encoded_df = pd.DataFrame(
        encoded_columns, columns=encoder.get_feature_names_out(COLUMNS_TO_ENCODE)
    )
    # Concatenate the encoded columns with the original dataframe
    df_ohe = pd.concat([df.drop(COLUMNS_TO_ENCODE, axis=1), encoded_df], axis=1)

    features2 = sorted(set(FEATURES) - set(COLUMNS_TO_ENCODE) | set(encoded_df.columns))
    df_ohe = df_ohe[features2]
    return df_ohe, encoder


def fill_na(df):
    """Fill missing values with the median."""
    # FIXME: Save the median to use on df_dev and df_test
    medians = df.median()
    df = df.fillna(medians)
    return df, medians


def grid_search(X_train, y_train, X_dev, y_dev):
    # Do search grid cross vlaidation
    from sklearn.model_selection import GridSearchCV

    model = GridSearchCV(
        xgb.XGBClassifier(),
        {
            "alpha": [15, 17, 20, 23, 25],
            "max_depth": [4, 5, 6],
            "n_estimators": [80, 90, 100, 110, 120],
        },
        cv=5,
        scoring="neg_log_loss",
        n_jobs=-1,
    )

    model.fit(X_train, y_train)
    print(model.best_params_)
    print(model.best_score_)
    print(model.best_estimator_)
    print(model.cv_results_)
    print(model.score(X_dev, y_dev))

    # Make predictions
    y_pred = model.predict(X_dev)

    # Print classification report
    print(classification_report(y_dev, y_pred))


def train_model(X_train, y_train):
    # Define the XGBoost model
    xgb_model = xgb.XGBClassifier(
        eval_metric="logloss",
        **BEST_HYPER_PARAMETERS,
    )
    # Train the model
    xgb_model.fit(X_train, y_train)
    return xgb_model


if __name__ == "__main__":
    df_train = open_df(TRAIN_AUGMENTED_PATH)
    X_train = df_train[FEATURES]
    y_train = df_train["y"]
    X_train, encoder = make_one_hot_encoding(X_train)
    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)
    X_train, medians = fill_na(X_train)
    with open(MEDIAN_PATH, "wb") as f:
        pickle.dump(medians, f)
    model = train_model(X_train, y_train)
    model.save_model(MODEL_PATH)
