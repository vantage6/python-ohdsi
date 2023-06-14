import codecs

from setuptools import setup, find_namespace_packages
from pathlib import Path

# get current directory
here = Path(__file__).parent.absolute()
parent_dir = here.parent.absolute()

# get the long description from the README file
with codecs.open(parent_dir / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

# get the version from the parent dir
with open(parent_dir / 'VERSION') as f:
    version = f.read().strip()

# setup the package
setup(
    name='ohdsi-circe',
    version=version,
    description='Python wrapper for the OHDSI R packages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vantage6/python-ohdsi',
    packages=find_namespace_packages(include=['ohdsi.*']),
    python_requires='>=3.10',
    install_requires=[
        'rpy2==3.5.12',
    ],
    extras_require={
        'dev': []
    },
    package_data={
        'ohdsi.circe.data': ['*.json'],
    },
    # entry_points={
    #     'console_scripts': [
    #         'vserver-local=vantage6.server.cli.server:cli_server'
    #     ]
    # }
)
