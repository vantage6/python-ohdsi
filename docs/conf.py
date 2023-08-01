# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../circe'))
sys.path.insert(0, os.path.abspath('../cohort-generator'))
sys.path.insert(0, os.path.abspath('../database-connector'))
sys.path.insert(0, os.path.abspath('../sqlrender'))
sys.path.insert(0, os.path.abspath('../feature-extraction'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'python-ohdsi'
copyright = '2023, F.C.Martin'
author = (
    'F.C.Martin'
)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon',
              'sphinx_autodoc_typehints', 'sphinx.ext.autosectionlabel',
              'sphinx.ext.intersphinx', 'sphinx_click.ext',
              'sphinxcontrib.plantuml']

napoleon_use_ivar = True

templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

master_doc = 'index'

add_module_names = False

pygments_style = None

numfig = True

plantuml_output_format = 'svg_img'

plantuml = 'java -jar /docs/java/plantuml.jar'
