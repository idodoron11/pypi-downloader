"""
Download and retrieve package wheel files from PyPI.
"""
import os
import subprocess
import requests
import asyncio


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
    """Download wheels concurrently across package versions."""
    asyncio.run(_download_all_versions(package_name, python_versions, download_dir))


async def _download_all_versions(package_name, python_versions, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    versions = get_package_versions(package_name)

    # Limit to 5 concurrent version downloads
    semaphore = asyncio.Semaphore(5)

    async def sem_download(version):
        async with semaphore:
            await download_version(version)

    async def download_version(version):
        for py_ver in python_versions:
            cmd = [
                "pip", "download", f"{package_name}=={version}",
                "--python-version", py_ver.replace(".", ""),
                "--only-binary=:all:",
                "--no-deps",
                "-d", download_dir
            ]
            print(f"Downloading {package_name}=={version} with Python{py_ver}...")
            proc = await asyncio.create_subprocess_exec(*cmd)
            ret = await proc.wait()
            if ret != 0:
                print(f"Failed to download {package_name}=={version} with Python{py_ver}")

    # Schedule tasks with concurrency limit
    tasks = [asyncio.create_task(sem_download(v)) for v in versions]
    await asyncio.gather(*tasks)
