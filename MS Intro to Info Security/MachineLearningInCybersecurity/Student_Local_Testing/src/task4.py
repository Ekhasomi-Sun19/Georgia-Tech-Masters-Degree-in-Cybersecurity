import numpy as np
import pandas as pd
from sklearn.metrics import *
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_selection import RFE

class ModelMetrics:
    def __init__(self, model_type:str,train_metrics:dict,test_metrics:dict,feature_importance_df:pd.DataFrame):
        self.model_type = model_type
        self.train_metrics = train_metrics
        self.test_metrics = test_metrics
        self.feat_imp_df = feature_importance_df
        self.feat_name_col = "Feature"
        self.imp_col = "Importance"
    
    def add_train_metric(self,metric_name:str,metric_val:float):
        self.train_metrics[metric_name] = metric_val

    def add_test_metric(self,metric_name:str,metric_val:float):
        self.test_metrics[metric_name] = metric_val

    def __str__(self): 
        output_str = f"MODEL TYPE: {self.model_type}\n"
        output_str += f"TRAINING METRICS:\n"
        for key in sorted(self.train_metrics):
            output_str += f"  - {key} : {self.train_metrics[key]:.4f}\n"
        output_str += f"TESTING METRICS:\n"
        for key in sorted(self.test_metrics):
            output_str += f"  - {key} : {self.test_metrics[key]:.4f}\n"
        if self.feat_imp_df is not None:
            output_str += f"FEATURE IMPORTANCES:\n"
            for i in self.feat_imp_df.index:
                output_str += f"  - {self.feat_imp_df[self.feat_name_col][i]} : {self.feat_imp_df[self.imp_col][i]:.4f}\n"
        return output_str

def calculate_naive_metrics(train_features:pd.DataFrame, test_features:pd.DataFrame, train_targets:pd.Series, test_targets:pd.Series, naive_assumption:int) -> ModelMetrics:
    train_predictions = [naive_assumption] * len(train_targets)
    test_predictions = [naive_assumption] * len(test_targets)

    train_metrics = {
        "accuracy" : round(accuracy_score(train_targets, train_predictions), 4),
        "recall" : round(recall_score(train_targets, train_predictions), 4),
        "precision" : round(precision_score(train_targets, train_predictions), 4),
        "fscore" : round(f1_score(train_targets, train_predictions), 4)
        }
    test_metrics = {
        "accuracy" : round(accuracy_score(test_targets, test_predictions), 4),
        "recall" : round(recall_score(test_targets, test_predictions), 4),
        "precision" : round(precision_score(test_targets, test_predictions), 4),
        "fscore" : round(f1_score(test_targets, test_predictions), 4)
        }
    naive_metrics = ModelMetrics("Naive",train_metrics,test_metrics,None)
    return naive_metrics



def calculate_logistic_regression_metrics(train_features:pd.DataFrame, test_features:pd.DataFrame, train_targets:pd.Series, test_targets:pd.Series, n_feat_importance:int, logreg_kwargs) -> tuple[ModelMetrics,LogisticRegression]:
    model = LogisticRegression(**logreg_kwargs)
    model.fit(train_features, train_targets)

    train_predictions = model.predict(train_features)
    test_predictions = model.predict(test_features)
    train_probs = model.predict_proba(train_features)[:, 1]
    test_probs = model.predict_proba(test_features)[:, 1]

    def compute_metrics(y_true, y_pred, y_prob):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return {
            "accuracy" : round(accuracy_score(y_true, y_pred), 4),
            "recall" : round(recall_score(y_true, y_pred), 4),
            "precision" : round(precision_score(y_true, y_pred), 4),
            "fscore" : round(f1_score(y_true, y_pred), 4),
            "fpr" : round(fp / (fp + tn), 4),
            "fnr" : round(fn / (fn + tp), 4),
            "roc_auc" : round(roc_auc_score(y_true, y_prob), 4)
            }

    train_metrics = compute_metrics(train_targets, train_predictions, train_probs)
    test_metrics = compute_metrics(test_targets, test_predictions, test_probs)

    rfe_selector = RFE(estimator=LogisticRegression(**logreg_kwargs), n_features_to_select=n_feat_importance)
    rfe_selector.fit(train_features, train_targets)
    selected_features = train_features.columns[rfe_selector.support_]

    reduced_model = LogisticRegression(**logreg_kwargs)
    reduced_model.fit(train_features[selected_features], train_targets)

    log_reg_importance = pd.DataFrame({
        "Feature": selected_features,
        "Importance": reduced_model.coef_[0]
        })
    log_reg_importance = log_reg_importance.reindex(
        log_reg_importance["Importance"].abs().sort_values(ascending=False).index
        )
    log_reg_importance["Importance"] = log_reg_importance["Importance"].round(4)
    log_reg_importance = log_reg_importance.reset_index(drop=True)

    log_reg_metrics = ModelMetrics("Logistic Regression",train_metrics,test_metrics,log_reg_importance)

    return log_reg_metrics,model



def calculate_decision_tree_metrics(train_features: pd.DataFrame, test_features: pd.DataFrame, train_targets: pd.Series, test_targets: pd.Series, n_feat_importance:int, dt_kwargs) -> tuple[ModelMetrics, DecisionTreeClassifier]:
    model = DecisionTreeClassifier(**dt_kwargs)
    model.fit(train_features, train_targets)

    train_predictions = model.predict(train_features)
    test_predictions = model.predict(test_features)
    train_probs = model.predict_proba(train_features)[:, 1]
    test_probs = model.predict_proba(test_features)[:, 1]

    def compute_metrics(y_true, y_pred, y_prob):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return {
            "accuracy" : round(accuracy_score(y_true, y_pred), 4),
            "recall" : round(recall_score(y_true, y_pred), 4),
            "precision" : round(precision_score(y_true, y_pred), 4),
            "fscore" : round(f1_score(y_true, y_pred), 4),
            "fpr" : round(fp / (fp + tn), 4),
            "fnr" : round(fn / (fn + tp), 4),
            "roc_auc" : round(roc_auc_score(y_true, y_prob), 4)
            }

    train_metrics = compute_metrics(train_targets, train_predictions, train_probs)
    test_metrics = compute_metrics(test_targets, test_predictions, test_probs)

    dt_importance = pd.DataFrame({
        "Feature": train_features.columns,
        "Importance": model.feature_importances_
        })
    dt_importance = dt_importance.sort_values(by="Importance", ascending=False).head(n_feat_importance)
    dt_importance["Importance"] = dt_importance["Importance"].round(4)
    dt_importance = dt_importance.reset_index(drop=True)

    dt_metrics = ModelMetrics("Decision Tree", train_metrics, test_metrics, dt_importance)

    return dt_metrics,model


def calculate_gradient_boosting_metrics(train_features:pd.DataFrame, test_features:pd.DataFrame, train_targets:pd.Series, test_targets:pd.Series, n_feat_importance: int, gb_kwargs) -> tuple[ModelMetrics,GradientBoostingClassifier]:
    model = GradientBoostingClassifier(**gb_kwargs)
    model.fit(train_features, train_targets)

    train_predictions = model.predict(train_features)
    test_predictions = model.predict(test_features)
    train_probs = model.predict_proba(train_features)[:, 1]
    test_probs = model.predict_proba(test_features)[:, 1]

    def compute_metrics(y_true, y_pred, y_prob):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return {
            "accuracy" : round(accuracy_score(y_true, y_pred), 4),
            "recall" : round(recall_score(y_true, y_pred), 4),
            "precision" : round(precision_score(y_true, y_pred), 4),
            "fscore" : round(f1_score(y_true, y_pred), 4),
            "fpr" : round(fp / (fp + tn), 4),
            "fnr" : round(fn / (fn + tp), 4),
            "roc_auc" : round(roc_auc_score(y_true, y_prob), 4)
            }

    train_metrics = compute_metrics(train_targets, train_predictions, train_probs)
    test_metrics = compute_metrics(test_targets, test_predictions, test_probs)

    gb_importance = pd.DataFrame({
        "Feature": train_features.columns,
        "Importance": model.feature_importances_
        })
    gb_importance = gb_importance.sort_values(by="Importance", ascending=False).head(n_feat_importance)
    gb_importance["Importance"] = gb_importance["Importance"].round(4)
    gb_importance = gb_importance.reset_index(drop=True)

    gb_metrics = ModelMetrics("Gradient Boosting",train_metrics,test_metrics,gb_importance)

    return gb_metrics,model

