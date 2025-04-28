import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer


def read_large_csv(path, chunk_size=100_000):
    
    chunks = []
    for chunk in pd.read_csv(path, low_memory=False, chunksize=chunk_size):
        chunks.append(chunk)
    
    df = pd.concat(chunks, ignore_index=True)
    return df


def drop_unhelpful_columns(df: pd.DataFrame):

    to_drop = [
        # free text / IDs
        "id", "member_id", "url", "desc",
        "emp_title", "title",

        # data that could be risky to use
        "zip_code",

        # dates
        "earliest_cr_line", "issue_d", "last_credit_pull_d",
        "last_pmnt_d", "next_pmnt_d", "hardship_start_date",
        "hardship_end_date", "payment_plan_start_date",
    ]

    return df.drop(columns=to_drop, errors="ignore")


def categorical_and_numerical_columns(df: pd.DataFrame, target_col: str):

    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Remove the target from features
    numerical_cols.remove(target_col)

    return categorical_cols, numerical_cols


def handle_missing_values(df: pd.DataFrame, categorical_cols, numerical_cols: list):

    num_imputer = SimpleImputer(strategy="median")
    cat_imputer = SimpleImputer(strategy="constant", fill_value="missing", keep_empty_features=True)

    df[numerical_cols] = num_imputer.fit_transform(df[numerical_cols])
    df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

    return df


def encode_categorical_variables(df: pd.DataFrame, categorical_cols: list):

    encoder = LabelEncoder()
    for col in categorical_cols:
        df[col] = encoder.fit_transform(df[col])

    return df


def main(dataset_path: str):

    print("Reading dataset...")
    df = read_large_csv(dataset_path)

    print("Removing unhelpful columns...")
    df = drop_unhelpful_columns(df)

    print("Defining target variable...")
    target_col = "loan_status"
    df = df[df[target_col].isin(["Fully Paid", "Charged Off"])]
    df[target_col] = df[target_col].map({"Fully Paid": 0, "Charged Off": 1})

    cat_col, num_col = categorical_and_numerical_columns(df, target_col)

    print("Handling missing values...")
    df = handle_missing_values(df, cat_col, num_col)

    print("Encoding categorical variables...")
    df = encode_categorical_variables(df, cat_col)

    print("Splitting into training and testing data...")
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":

    dataset = "data/Loan_status_2007-2020Q3.csv"
    main(dataset)
