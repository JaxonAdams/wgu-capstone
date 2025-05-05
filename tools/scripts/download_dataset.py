import os
import argparse
import subprocess

import pandas as pd

from src.utils.utils import read_large_csv


def sample_and_overwrite(file_path: str, sample_fraction: float = 0.05, seed: int = 42):
    
    print("Loading dataset...")
    df = read_large_csv(file_path)

    print(f"Sampling {sample_fraction * 100}% of the dataset...")
    sampled_df = df.sample(frac=sample_fraction, random_state=seed)

    print("Overwriting the original file with the sampled data...")
    sampled_df.to_csv(file_path, index=False)
    print("Done! File overwritten with sampled data.")


def download_kaggle_dataset(dataset, target_folder):

    parser = argparse.ArgumentParser(description="Optionally sample and overwrite a large CSV.")
    parser.add_argument("--sample", action="store_true", help="Sample and overwrite the CSV file.")
    parser.add_argument("--fraction", type=float, default=0.05, help="Fraction of rows to sample (default 0.05).")

    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(target_folder, exist_ok=True)

    # Use Kaggle CLI to download
    print(f"Downloading {dataset} to {target_folder} ...")
    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", dataset, "-p", target_folder, "--unzip"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Download failed:")
        print(result.stderr)
        return
    
    print("Download complete.")

    files = os.listdir(target_folder)
    gzip_files = [f for f in files if f.endswith('.gzip')]

    if not gzip_files:
        print("Warning: No .gzip file found after download.")
        return
    
    gzip_file = gzip_files[0]
    gzip_path = os.path.join(target_folder, gzip_file)
    
    csv_file = gzip_file.replace('.gzip', '.csv')
    csv_path = os.path.join(target_folder, csv_file)

    os.rename(gzip_path, csv_path)

    if args.sample:
        sample_and_overwrite(csv_path, args.fraction)
    else:
        print("No sampling performed. Use --sample to enable sampling.")

    print(f"Dataset ready: {csv_path}")


if __name__ == "__main__":

    dataset = "ethon0426/lending-club-20072020q1"
    target_folder = "./data/"

    download_kaggle_dataset(dataset, target_folder)
