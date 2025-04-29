import os

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

import src.model.prepare_data as prep_data
from src.utils.utils import decorate_console_output


@decorate_console_output("PREPROCESSING DATASET")
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
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numerical_columns),
        ("cat", categorical_transformer, categorical_columns),
    ], sparse_threshold=1.0)

    return Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])


@decorate_console_output("TRAINING THE MACHINE LEARNING MODEL")
def train_model(model, X_train, y_train):

    return model.fit(X_train, y_train)


@decorate_console_output("PREDICTING ON THE TEST SET")
def test_model(model, X_test, y_test):
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


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
        max_features="sqrt"
    )

    pipeline = create_pipeline(rf, num_cols, cat_cols)

    train_model(pipeline, X_train, y_train)
    test_model(pipeline, X_test, y_test)

    os.makedirs("data/models", exist_ok=True)
    save_model(pipeline, X_train.columns.tolist(), "data/models/rf.pkl")


if __name__ == "__main__":

    dataset_path = "data/Loan_status_2007-2020Q3.csv"
    main(dataset_path)
