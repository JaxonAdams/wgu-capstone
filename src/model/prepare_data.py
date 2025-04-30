from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import src.plot.fico_distribution as fico_dist
import src.plot.correlation_heatmap as c_hm
from src.utils.utils import read_large_csv


def drop_unhelpful_columns(df: pd.DataFrame):

    to_drop = [
        "url", "zip_code",
        "hardship_start_date", "hardship_end_date", "payment_plan_start_date",
        "hardship_last_payment_amount", "hardship_amount", "hardship_length", "hardship_dpd",
        "hardship_loan_status", "orig_projected_additional_accrued_interest",
        "debt_settlement_flag_date", "settlement_status", "settlement_date",
        "settlement_amount", "settlement_percentage", "settlement_term",
        "sec_app_earliest_cr_line", "sec_app_mths_since_last_major_derog",
        "id", "emp_title", "title", "pymnt_plan", "next_pymnt_d",
        "delinq_2yrs", "last_pymnt_amnt", "funded_amnt", "funded_amnt_inv",
        "sub_grade", "out_prncp", "out_prncp_inv", "total_pymnt", "total_pymnt_inv",
        "total_rec_prncp", "total_rec_int", "total_rec_late_fee", "recoveries",
        "collection_recovery_fee", "last_credit_pull_d", "last_fico_range_low",
        "last_fico_range_high", "revol_bal_joint", "sec_app_fico_range_low",
        "sec_app_fico_range_high", "sec_app_inq_last_6mths", "sec_app_mort_acc",
        "sec_app_open_acc", "sec_app_revol_util", "sec_app_open_act_il",
        "sec_app_num_rev_accts", "sec_app_chargeoff_within_12_mths",
        "sec_app_collections_12_mths_ex_med", "policy_code", "deferral_term",
        "debt_settlement_flag", "hardship_flag", "hardship_type", "hardship_reason",
        "hardship_status", "hardship_payoff_balance_amount", "installment", "initial_list_status",
        "application_type", "verification_status_joint", "annual_inc_joint", "dti_joint",
    ]

    return df.drop(columns=to_drop, errors="ignore")


def get_feature_types(df: pd.DataFrame, target_col: str):
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if target_col in numerical_cols:
        numerical_cols.remove(target_col)

    return categorical_cols, numerical_cols


def clean_int_rate(df):
    df["int_rate"] = df["int_rate"].str.strip().str.rstrip('%').astype(float)
    return df


def clean_revol_util(df):
    df["revol_util"] = df["revol_util"].str.strip().str.rstrip('%').astype(float)
    return df


def extract_date_features(df):
    date_columns = ["issue_d", "earliest_cr_line", "last_pymnt_d"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", format="%b-%Y")

    df["loan_age_months"] = (datetime.today() - df["issue_d"]).dt.days // 30
    df["earliest_credit_months"] = (datetime.today() - df["earliest_cr_line"]).dt.days // 30

    df["issue_year"] = df["issue_d"].dt.year

    to_drop = ["issue_d", "earliest_cr_line"]
    df.drop(columns=to_drop, errors="ignore")

    return df


def encode_sub_grade(df):
    grade_order = {g+str(i): idx for idx, g in enumerate("ABCDEFG", start=0) for i in range(1, 6)}
    df["sub_grade_encoded"] = df["sub_grade"].map(grade_order)
    return df


def transform_features(df):
    df = clean_revol_util(df)
    df = clean_int_rate(df)
    df = extract_date_features(df)
    df = encode_sub_grade(df)
    
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

    print("Cleaning up certain features...")
    df = transform_features(df)

    print("Generating data visualizations...")
    fico_dist.plot(df)
    c_hm.plot(df)

    print("Splitting features and labels...")
    X = df.drop(columns=[target_col])
    y = df[target_col]

    print("Identifying feature types...")
    categorical_cols, numerical_cols = get_feature_types(X, target_col)

    print("Splitting train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, categorical_cols, numerical_cols


if __name__ == "__main__":

    dataset = "data/Loan_status_2007-2020Q3.csv"
    main(dataset)
