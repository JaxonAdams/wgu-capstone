import seaborn as sns
import matplotlib.pyplot as plt

from src.utils.utils import read_large_csv


def plot(df):

    df_subset = df[[
        "loan_amnt",
        "int_rate",
        "annual_inc",
        "dti",
        "fico_range_low",
        "fico_range_high"
    ]].copy()

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
