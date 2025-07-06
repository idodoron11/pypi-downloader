# pypi-downloader

A tool to download wheel files from PyPI for specified Python versions.

## Installation

# Clone the repository and install dependencies
```bash
git clone https://github.com/yourusername/pypi-downloader.git
cd pypi-downloader
poetry install
```

# (Optional) Install the package into your environment
```bash
poetry run pip install .
```

Or, after publishing to PyPI, simply:
```bash
pip install pypi-downloader
```

## Usage

Once installed, use the `pypi_downloader` command:
```bash
pypi_downloader <package> -p <version1> <version2> ... [-d <download_dir>]
```

### Arguments

- `<package>`: Name of the PyPI package to download.
- `-p, --python-versions`: One or more Python versions (e.g. `3.10 3.11`).
- `-d, --download-dir`: Target directory for wheel files (default: `downloads`).

### Examples

Download wheels for requests on Python 3.10 and 3.11:
```bash
pypi_downloader requests -p 3.10 3.11
```

Specify a custom download directory:
```bash
pypi_downloader numpy -p 3.9 3.10 -d wheels_cache
```
