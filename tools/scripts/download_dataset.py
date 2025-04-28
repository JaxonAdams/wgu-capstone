import os
import subprocess


def download_kaggle_dataset(dataset, target_folder):

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

    print(f"Dataset ready: {csv_path}")


if __name__ == "__main__":

    dataset = "ethon0426/lending-club-20072020q1"
    target_folder = "./data/"

    download_kaggle_dataset(dataset, target_folder)
