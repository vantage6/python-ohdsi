import codecs
from pathlib import Path

from setuptools import find_namespace_packages, setup

# get current directory
here = Path(__file__).absolute()
# get the long description from the README file
with codecs.open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

# get the version from the parent dir
# with open(here / "VERSION") as f:
#     version = f.read().strip()

# setup the package
setup(
    name="ohdsi-circe",
    # version=version,
    description="Python wrapper for the OHDSI Circe R package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vantage6/python-ohdsi",
    packages=find_namespace_packages(include=["ohdsi.*"]),
    python_requires=">=3.13",
    install_requires=[
        "rpy2==3.5.12",
    ],
    extras_require={"dev": []},
    package_data={
        "ohdsi.circe.data": ["*.json"],
    },
)
