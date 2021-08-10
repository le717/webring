from pathlib import Path
from sys import argv
from toml import loads


def get_package(package_info: dict) -> str:
    """Construct the package name and exact version to install."""
    package_tag = f"{package_info['name']}=={package_info['version']}"

    # If the package is from a local file, use the file path
    source = package_info.setdefault("source", {})
    if source.get("type") == "file":
        # Trim off the app root path
        package_tag = package_info["source"]["url"]
        package_tag = package_tag[package_tag.find("/") + 1 :]  # skipcq: FLK-E203

    # If the package is from a URL use the URL
    elif source.get("type") == "url":
        package_tag = package_info["source"]["url"]

    return package_tag


def filter_packages(packages: list, key: str) -> list:
    """Filter out packages based on the given category."""
    return [p for p in packages if p["category"] == key]


# Does the user want to include the dev packages?
try:
    get_dev_packages = argv[1].lower() == "--dev"
except IndexError:
    get_dev_packages = False

# Load the lock file contents and get the respective package for each category
poetry_lock = loads((Path() / "poetry.lock").read_text())
all_packages = filter_packages(poetry_lock["package"], "main")

# Write the dev packages if requested
if get_dev_packages:
    all_packages += filter_packages(poetry_lock["package"], "dev")

# Open the requirements file for writing
with open("requirements.txt", "wt") as f:
    # Write all the requested packages
    for package in all_packages:
        f.write(f"{get_package(package)}\n")
