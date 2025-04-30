import seaborn as sns
import matplotlib.pyplot as plt

from src.utils.utils import read_large_csv


def main(dataset_filepath):

    # Load the dataset
    df = read_large_csv(dataset_filepath)

    # Compute average credit score
    df["fico_avg"] = (df["fico_range_low"] + df["fico_range_high"]) / 2

    # Plot distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df["fico_avg"], bins=40, kde=True)
    plt.title("Distribution of Borrower Credit Scores")
    plt.xlabel("FICO Score")
    plt.ylabel("Frequency")
    plt.savefig("data/visualizations/fico_distribution.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":

    main("data/Loan_status_2007-2020Q3.csv")
