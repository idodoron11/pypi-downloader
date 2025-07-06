import requests
import os
import subprocess

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
    package = "requests"  # Replace with your desired package
    python_versions = ["3.10", "3.11", "3.12", "3.13"]  # Replace with your desired Python versions
    download_wheel_files(package, python_versions)
