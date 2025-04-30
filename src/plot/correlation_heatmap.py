import seaborn as sns
import matplotlib.pyplot as plt

from src.utils.utils import read_large_csv


def clean_percentage_column(series):
    return series.str.strip().str.replace('%', '', regex=False).astype(float)


def main(dataset_filepath):

    # Load the dataset
    df = read_large_csv(dataset_filepath)

    df_subset = df[[
        "loan_amnt",
        "int_rate",
        "annual_inc",
        "dti",
        "fico_range_low",
        "fico_range_high"
    ]].copy()

    # Fix interest rate (percent string to float)
    df_subset["int_rate"] = clean_percentage_column(df_subset["int_rate"])

    # Drop rows with missing values in selected features
    df_subset = df_subset.dropna()

    # Optional: average the FICO range
    df_subset["fico_avg"] = (df_subset["fico_range_low"] + df_subset["fico_range_high"]) / 2
    df_subset.drop(["fico_range_low", "fico_range_high"], axis=1, inplace=True)

    correlation_matrix = df_subset.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap of Loan Features")
    plt.tight_layout()
    plt.savefig("data/visualizations/correlation_heatmap.png", dpi=300)


if __name__ == "__main__":

    main("data/Loan_status_2007-2020Q3.csv")
