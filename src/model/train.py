import os

import joblib
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
    confusion_matrix,
    average_precision_score,
)

import src.model.prepare_data as prep_data
import src.plot.feature_importance as ft_imp
import src.plot.precision_recall_curve as pr_c
import src.plot.probability_distribution as prob_dist
from src.utils.utils import decorate_console_output


@decorate_console_output("PREPROCESSING THE DATASET")
def prepare_training_data(dataset_path):

    return prep_data.main(dataset_path)


@decorate_console_output("CREATING A DATA PROCESSING PIPELINE")
def create_pipeline(classifier, numerical_columns, categorical_columns):
    
    # Preprocessing for numerical features
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="mean"))
    ])

    # Preprocessing for categorical features
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing", keep_empty_features=True)),
        ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numerical_columns),
        ("cat", categorical_transformer, categorical_columns),
    ], sparse_threshold=1.0)

    return Pipeline(steps=[
        ("preprocessor", preprocessor),
        ('smote', SMOTE(random_state=42)),
        ("classifier", classifier),
    ])


@decorate_console_output("TRAINING THE MACHINE LEARNING MODEL")
def train_model(model, X_train, y_train):

    print(f"Value counts:\n{y_train.value_counts()}")
    return model.fit(X_train, y_train)


@decorate_console_output("PREDICTING ON THE TEST SET")
def test_model(model, X_test, y_test, threshold=0.5):
    
    # Due to dataset bias towards paid-in-full accounts,
    # optionally adjust the probability threshold to catch
    # more default accounts
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred_thresh = (y_proba >= threshold).astype(int)

    roc_auc = roc_auc_score(y_test, y_proba)
    accuracy = accuracy_score(y_test, y_pred_thresh)
    avg_precision = average_precision_score(y_test, y_proba)

    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"ROC AUC Score: {roc_auc:.4f}")
    print(f"PR AUC: {avg_precision:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_thresh))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred_thresh))

    return y_test, y_proba


@decorate_console_output("CREATING DATA VISUALIZATIONS")
def create_visualizations(model, y_test, y_scores):

    ft_imp.plot(model)
    pr_c.plot(y_test, y_scores)
    prob_dist.plot(y_test, y_scores)


@decorate_console_output("SAVING THE TRAINED MODEL")
def save_model(model, features, filepath):

    joblib.dump({
        "model": model,
        "features": features
    }, filepath, compress=3)
    print(f"Model stored in file '{filepath}'")


def main(dataset_path):

    X_train, X_test, y_train, y_test, cat_cols, num_cols = prepare_training_data(dataset_path)

    for col in cat_cols:
        X_train[col] = X_train[col].astype(str)
        X_test[col] = X_test[col].astype(str)

    rf = RandomForestClassifier(
        n_estimators=100,    # number of trees
        max_depth=None,      # allow trees to grow fully
        random_state=42,     # reproducibility
        n_jobs=-1,           # use all CPU cores
        max_features="sqrt",
        class_weight="balanced",
    )

    pipeline = create_pipeline(rf, num_cols, cat_cols)

    train_model(pipeline, X_train, y_train)
    y_test, y_scores = test_model(pipeline, X_test, y_test, threshold=0.3)

    create_visualizations(pipeline, y_test, y_scores)

    os.makedirs("data/models", exist_ok=True)
    save_model(pipeline, X_train.columns.tolist(), "data/models/rf.pkl")


if __name__ == "__main__":

    dataset_path = "data/Loan_status_2007-2020Q3.csv"
    main(dataset_path)
