import requests
import os
import subprocess
import argparse

def get_package_versions(package_name):
    """Fetch all available versions of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return list(data['releases'].keys())
    else:
        raise Exception(f"Failed to fetch package info for {package_name}")

def download_wheel_files(package_name, python_versions, download_dir="downloads"):
    """Download specified versions of the package using pip download for each Python interpreter."""
    os.makedirs(download_dir, exist_ok=True)
    versions = get_package_versions(package_name)
    for version in versions:
        for py_ver in python_versions:
            cmd = [
                "pip", "download", f"{package_name}=={version}",
                "--python-version", py_ver.replace(".", ""),
                "--only-binary=:all:",
                "--no-deps",
                "-d", download_dir
            ]
            print(f"Downloading {package_name}=={version} with Python{py_ver}...")
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to download {package_name}=={version} with Python{py_ver}: {e}")
                continue

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download package wheels for specific Python versions.")
    parser.add_argument("package", help="Name of the package to download.")
    parser.add_argument("-p", "--python-versions", nargs='+', required=True,
                        help="List of Python versions, e.g. 3.10 3.11.")
    parser.add_argument("-d", "--download-dir", default="downloads",
                        help="Directory to save downloaded wheels.")
    args = parser.parse_args()
    download_wheel_files(args.package, args.python_versions, args.download_dir)
