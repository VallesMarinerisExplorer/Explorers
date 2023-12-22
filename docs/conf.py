# conf.py

# -- Project information -----------------------------------------------------

project = 'Explorers'
author = 'Alex Horvath'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here
extensions = []

# The name of the main toctree document
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# Theme options are theme-specific and customize the look and feel of a theme
html_theme_options = {}

# Add any paths that contain templates here, relative to this directory
templates_path = ['_templates']

# The suffix(es) of source filenames
source_suffix = ['.rst', '.md']

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder
htmlhelp_basename = 'MyProjectDoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}

# List of LaTeX documents
latex_documents = [
    (master_doc, 'MyProject.tex', 'My Project Documentation',
     'Your Name', 'manual'),
]

# -- Options for manual page output ------------------------------------------

man_pages = [
    (master_doc, 'myproject', 'My Project Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (master_doc, 'MyProject', 'My Project Documentation',
     author, 'MyProject', 'One line description of project.',
     'Miscellaneous'),
]
