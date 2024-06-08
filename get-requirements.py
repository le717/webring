from collections.abc import Iterable
from pathlib import Path
from sys import argv
from tomllib import loads


def get_package(package_info: dict) -> str:
    """Construct the package name and exact version to install."""
    package_tag = f"{package_info['name']}=={package_info['version']}"

    # The package is a local file
    source = package_info.setdefault("source", {})
    if source.get("type") == "file":
        # Trim off the app root path
        package_tag = package_info["source"]["url"]
        package_tag = package_tag[package_tag.find("/") + 1 :]

    # The package is from a URL
    elif source.get("type") == "url":
        package_tag = package_info["source"]["url"]

    # The package is from a git repo revision
    elif source.get("type") == "git":
        git_hash = package_info["source"]["resolved_reference"]
        git_repo_archive = package_info["source"]["url"].replace(".git", "/archive")
        package_tag = f"{git_repo_archive}/{git_hash}.zip"

    return package_tag


def filter_packages(packages: list, dev_pkgs: Iterable[str]) -> list:
    """Filter out packages based on the given category."""
    return [p for p in packages if p["name"] not in dev_pkgs]


# Does the user want to include the dev packages?
try:
    get_dev_packages = argv[1].lower() == "--dev"
except IndexError:
    get_dev_packages = False

# Load the pyproject and poetry lock file contents
pyproject_toml = loads((Path() / "pyproject.toml").read_text())
poetry_lock = loads((Path() / "poetry.lock").read_text())

# Resolve the dev packages, if there are any used in this project
dev_packages = (
    pyproject_toml["tool"]["poetry"]["group"].get("dev", {}).get("dependencies", {}).keys()
)

# This might seem backwards, but if we want to install the dev packages,
# we clear the list of dev packages so every package listed gets installed
if get_dev_packages:
    dev_packages = []

# Work out all of the requirements, and generate a simple requirements.txt file
all_packages = filter_packages(poetry_lock["package"], dev_packages)
with Path("requirements.txt").open("w") as f:
    # Write all the requested packages
    for package in all_packages:
        f.write(f"{get_package(package)}\n")
