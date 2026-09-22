import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

def document_hyperparameter_tuning_clamp(train_df,test_df):
    features = train_df.drop(columns=["label"]).dropna(axis=1, how="all")
    target = train_df["label"]
    
    param_dist = {
        "n_estimators": [100, 200, 300, 500],
        "max_depth": [None, 5, 10, 15, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    }
    
    search = RandomizedSearchCV(
        RandomForestClassifier(random_state=42, class_weight="balanced"),
        param_distributions=param_dist,
        n_iter=30,
        scoring="roc_auc",
        cv=5,
        random_state=42,
        n_jobs=-1
    )
    search.fit(features, target)
    hyperparameters = search.best_params_

    return hyperparameters


def train_model_return_scores_clamp(train_df, test_df) -> pd.DataFrame:
    features = train_df.drop(columns=["label"]).dropna(axis=1, how="all")
    target = train_df["label"]
    test_features = test_df[features.columns]

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features="sqrt",
        random_state=42,
        class_weight="balanced"
    )
    model.fit(features, target)
    test_probs = model.predict_proba(test_features)[:, 1]
    test_scores = pd.DataFrame({
        "index": test_df.index,
        "prob_label_1": test_probs
    })
    return test_scores


def document_hyperparameter_tuning_unsw(train_df,test_df):
    features = train_df.drop(columns=["label"])
    target = train_df["label"]

    param_dist = {
        "n_estimators": [100, 200, 300, 500],
        "max_depth": [None, 5, 10, 15, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    }

    search = RandomizedSearchCV(
        RandomForestClassifier(random_state=42),
        param_distributions=param_dist,
        n_iter=30,
        scoring="roc_auc",
        cv=5,
        random_state=42,
        n_jobs=-1
    )
    search.fit(features, target)
    hyperparameters = search.best_params_

    return hyperparameters

def train_model_return_scores_unsw(train_df,test_df) -> pd.DataFrame:
    features = train_df.drop(columns=["label"])
    target = train_df["label"]
    test_features = test_df[features.columns]

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="log2",
        random_state=42
    )
    model.fit(features, target)
    test_probs = model.predict_proba(test_features)[:, 1]
    test_scores = pd.DataFrame({
        "index": test_df.index,
        "prob_label_1": test_probs
    })
    return test_scores

def document_hyperparameter_tuning_phiusiil(train_df,test_df):
    features = extract_url_features(train_df["URL"])
    target = train_df["label"]

    param_dist = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
        "min_samples_leaf": [1, 2, 4],
    }

    search = RandomizedSearchCV(
        RandomForestClassifier(random_state=42, n_jobs=-1),
        param_distributions=param_dist,
        n_iter=10,
        scoring="roc_auc",
        cv=3,
        random_state=42
    )
    search.fit(features, target)
    hyperparameters = search.best_params_

    return hyperparameters

def train_model_return_scores_phiusiil(train_df, test_df) -> pd.DataFrame:
    train_features = extract_url_features(train_df["URL"])
    target = train_df["label"]
    test_features = extract_url_features(test_df["URL"])

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    model.fit(train_features, target)
    test_probs = model.predict_proba(test_features)[:, 1]
    test_scores = pd.DataFrame({
        "index": test_df.index,
        "prob_label_1": test_probs
    })
    return test_scores

