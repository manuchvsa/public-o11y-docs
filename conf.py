# -*- coding: utf-8 -*-
#
# Splunk Observability Cloud documentation build configuration file,
# initial version created by sphinx-quickstart on Mon Apr 11 14:35:43 2016.
# 
# Version history:
#
# Modified by fferribenedetti 2021-07-05
# Modified by jmalin 2022-09-22: Cleanup for use in GitHub documentation system
#
# Hack: Add a line to force a commit/push

# -- General configuration ------------------------------------------------

#
# Add modules that support adding local modules 
import sys
import os

# Add the private-o11y-docs/_ext directory to sys.path, so that Sphinx can find extensions ins _ext.
sys.path.insert(0, os.path.join(os.path.abspath('.'), '_ext'))

from assetminify import final_conf_includes


# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx_copybutton',
    'toggle',
    'newpage',
    'github',
    'myst_parser',
    'sphinx_tabs.tabs',
    'olly_on_git_hub'
]
olly_on_github_repo = 'splunk/public-o11y-docs'
olly_on_github_branch = 'main'
sphinx_tabs_disable_tab_closing = True

# Set myst_parser to automatically generate labels for h1, h2, and h3 headings
myst_heading_anchors = 3

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
# source_suffix = '.rst'
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
# Update the copyright date annually -- Barbara Snyder
project = 'Splunk'
copyright = '2022 Splunk, Inc'
author = 'Splunk'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx.
#
# This is also used if you do content translation via gettext catalogs.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'venv/lib/*/site-packages', 'Thumbs.db', '.DS_Store','z_cheat-sheets', 'README.md', 'CONTRIBUTING.md', '.github/pull_request_template.md', 'gdi/couchdb/couchdb.md', 'apm/find-root-cause.rst']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
html_title = 'Splunk Observability Cloud documentation'

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
#       'searchbox.html',
        'about.html',
        'fulltoc.html',
        'relations.html',
    ]
}

html_theme_options = {
    'logo_name': True,
    'github_button': False,
}

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_copy_empty_lines = False
copybutton_line_continuation_character = "\\"

# Add permalinks; trying to determine how to change
# "Permalink to this headline" but so far, no success --barbara snyder
# See also signalfx-includes.css and signalfx-alabaster.css
# (search for permalink or headerlink)

html_permalinks_icon = u'  🔗'

# Output file base name for HTML help builder.
htmlhelp_basename = 'Splunkdoc'

# /* ROLES: Usage is :role:NO SPACE `text` */
# /* e.g. this is :not-ok:`red` */
# Font for roles is set in signalfx-includes.css. Search for span.strong to find how to define them.

rst_prolog = """
.. role:: not-ok
.. role:: ok
.. role:: note
.. role:: strong
.. role:: title
.. role:: monospace
.. role:: strike

.. |more| raw:: html

   ⋯

.. |verticaldots| raw:: html

   ⋮

.. |br| raw:: html

   <br />

.. |hr| raw:: html

   <hr />

"""

# An RST epilog to add variable names for feature text replacement, and non-breaking space.
#

rst_epilog = """
.. |ms| replace:: Metrics Sidebar
.. |mtab| replace:: Muting Rules tab
.. |sn| replace:: ServiceNow
.. |sv| replace:: secondary visualization
.. |openmenu| replace:: Open the Detector
   menu by clicking the bell icon at the top right corner of a chart.

.. |nbsp| unicode:: 0xA0
      :trim:

.. |hyph| unicode:: 0x2011
      :trim:

"""



def on_page_context(app, pagename, templatename, context, doctree):
    """
    This injects the ``get_local_toc`` function into the document.

    The logic around the builder is because the JSON and other HTML builders,
    they will error because we've added a Python function into the context.
    So we have to make sure we're only putting this into HTML builders,
    and ones that don't serialize the context.
    """
    if getattr(app.builder, 'implementation', None) or app.builder.format != 'html':
        return
    context['get_local_toc'] = app.builder._get_local_toctree


def determine_local_toc(app, pagename, templatename, context, doctree):
    """
    This code determines the set of documents that get a local TOC in the sidebar.

    Any new books can be added to the ``books`` list here,
    and they will be given the proper local TOC sidebar.

    The actual implementation is in ``_templates/fulltoc.html``,
    where we show the proper toc depending on the ``show_local_toc`` variable here.
    """
#     books = ['monitor-alert', 'admin-guide', 'analytics-docs']
# If you add a book here, check to see if you need to remove maxdepth in the index.rst for the doc
# NEVER MIND: books function no longer used 10/2018
    books = []
    localtoc = False
    for book in books:
        if pagename.startswith(book):
            localtoc = True
            break
    context['show_local_toc'] = localtoc


def setup(app):
    # don't include any js or css file here or any other .py files , instead use only _ext/assetminify.py file 
    app.add_css_file('main.min.css')
    app.add_js_file('main.min.js')
    massets = final_conf_includes
    for asstname in massets:
        if asstname.endswith('.js'):
            app.add_js_file(asstname)
        if asstname.endswith('.css'):
            app.add_css_file(asstname)
            
    app.connect('html-page-context', on_page_context)
    app.connect('html-page-context', determine_local_toc)

# Removed from above
#   app.add_stylesheet('signalfx-fonts.css')

html_baseurl = "https://docs.splunk.com/Observability/"
