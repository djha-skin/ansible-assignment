# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'UltraDNS Timing Statistics'
copyright = '2026, Daniel Haskin'
author = 'Daniel Haskin'

release = '1.0.0'
version = '1.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for HTMLHelp output

htmlhelp_basename = 'ultradns_timing_statsdoc'

# -- Options for LaTeX output

latex_elements = {}

latex_documents = [
    (
        'index',
        'ultradns_timing_stats.tex',
        'UltraDNS Timing Statistics Documentation',
        'Daniel Haskin',
        'manual',
    ),
]

# -- Options for manual page output

man_pages = [
    (
        'index',
        'ultradns_timing_stats',
        'UltraDNS Timing Statistics Documentation',
        [author],
        1,
    )
]

# -- Options for Texinfo output

texinfo_documents = [
    (
        'index',
        'ultradns_timing_stats',
        'UltraDNS Timing Statistics Documentation',
        author,
        'ultradns_timing_stats',
        'One line description of project.',
        'Miscellaneous',
    ),
]
