"""
Command-line interface for pypi_downloader.
"""
import argparse
from .downloader import download_wheel_files


def main():
    parser = argparse.ArgumentParser(description="Download package wheels for specific Python versions.")
    parser.add_argument("package", help="Name of the package to download.")
    parser.add_argument("-p", "--python-versions", nargs='+', required=True,
                        help="List of Python versions, e.g. 3.10 3.11.")
    parser.add_argument("-d", "--download-dir", default="downloads",
                        help="Directory to save downloaded wheels.")
    args = parser.parse_args()
    download_wheel_files(args.package, args.python_versions, args.download_dir)
