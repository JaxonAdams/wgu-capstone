import os

import pandas as pd
from ydata_profiling import ProfileReport


def profile(data_file, output_file):
    if not os.path.exists(data_file):
        print(f"Dataset not found at {data_file}. Please run the download script before profiling.")
        return
    
    print(f"Loading {data_file} ...")
    df = pd.read_csv(data_file, nrows=10000)

    print(f"Generating profile report ...")
    profile = ProfileReport(df, title="LendingClub Dataset Report", explorative=True)

    print(f"Saving report to {output_file} ...")
    profile.to_file(output_file)

    print("Profile generated. Open the HTML file to view the report.")


if __name__ == "__main__":

    data_file = "data/Loan_status_2007-2020Q3.csv"
    output_file = "data/lendingclub_profile_report.html"

    profile(data_file, output_file)
