# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys


sys.path.insert(0, os.path.abspath('../src'))   
import constants

project = 'Tempico Software'
copyright = '2025,Tausand Electronics'
author = 'Tausand Electronics'
release = constants.VERSION

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']
latex_elements = {
    'preamble': r'''
    \usepackage{hyperref}
    \hypersetup{
        colorlinks=true,
        linkcolor=blue,
        filecolor=magenta,      
        urlcolor=blue,
        pdftitle={Título del Proyecto},
        pdfauthor={Tu Nombre},
        pdfkeywords={palabras clave, del, proyecto},
    }
    ''',
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

