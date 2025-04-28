import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import src.model.prepare_data as prep_data
from src.utils.utils import decorate_console_output


@decorate_console_output("PREPROCESSING DATASET")
def prepare_training_data(dataset_path):

    return prep_data.main(dataset_path)


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
def save_model(model, filepath):

    joblib.dump(model, filepath)
    print(f"Model stored in file '{filepath}'")


def main(dataset_path):

    X_train, X_test, y_train, y_test = prepare_training_data(dataset_path)

    rf = RandomForestClassifier(
        n_estimators=100,  # number of trees
        max_depth=None,    # allow trees to grow fully
        random_state=42,   # reproducibility
        n_jobs=-1,         # use all CPU cores
    )

    train_model(rf, X_train, y_train)
    test_model(rf, X_test, y_test)
    save_model(rf, "data/rf.pkl")


if __name__ == "__main__":

    dataset_path = "data/Loan_status_2007-2020Q3.csv"
    main(dataset_path)
