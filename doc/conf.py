# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import subprocess  # <--- ADD THIS LINE
import sys         # <--- You will likely need this too if you don't have it
from sphinx.application import Sphinx
import shutil
from pathlib import Path  # <-- ADD THIS LINE

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Example'
copyright = 'workshop participant'
author = 'workshop participant'
release = '0.1'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
    'breathe',
    'exhale'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

#html_extra_path = [
#    '../src/stack/pinocchio/build/doc/doxygen-html',
#    '../src/stack/aligator/build/doc/doxygen-html',
#]

breathe_projects = {
    "pinocchio": "../src/stack/pinocchio/build/doc/xml",
    "aligator": "../src/stack/aligator/build/doc/xml",
 }

# Optional: Set the default project for directives
breathe_default_project = "aligator"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'breeze'
# html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',  #  Provided by Google in your dashboard
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9', # Or your preferred color
    # Toc options
    'collapse_navigation': False,  # <-- Don't collapse the sidebar
    'sticky_navigation': True,     # <-- Make the sidebar sticky
    'navigation_depth': 5,         # <-- Show up to 4 levels of headings
    'includehidden': True,
    'titles_only': False,
    # breeze theme
    'header_tabs': False
}

# --- EXHALE CONFIGURATION ---
# Setup the exhale extension
exhale_args = {
    # These arguments are required
    "containmentFolder":     "./api",
    "rootFileName":          "library_root.rst",
    "doxygenStripFromPath":  "..",

    # These are the projects Exhale will parse
    #"breathe_projects": breathe_projects,
    # This is the entry point for breathe directives.
    #"breathe_default_project": breathe_default_project,

    # Optional, but recommended configuration items
    "rootFileTitle": "Maestro API Reference",
    "createTreeView": True,

    # Useful for debugging if things go wrong
    # "verboseBuild": True,
}

# Tell sphinx what the primary language being documented is.
primary_domain = 'cpp'

# Tell sphinx what the pygments highlight language should be.
highlight_language = 'cpp'

# -- Manual Exhale Configuration for Multiple Projects ----------------------

def configure_exhale_for_multiproject(app):
    """
    Manually configure Exhale to generate separate documentation trees
    for each project. This function is called before Sphinx reads sources.
    """
    from exhale import configs as exhale_configs

    # First, configure Exhale for Pinocchio
    pinocchio_args = {
        "containmentFolder": "./api/pinocchio",
        "rootFileName": "pinocchio_root.rst",
        "doxygenStripFromPath": "../../src/stack/pinocchio",
        "rootFileTitle": "Pinocchio API",
        "createTreeView": True,
        # Tell Exhale to only process Pinocchio's XML
        "breathe_projects": {
            "Pinocchio": "../src/stack/pinocchio/build/doc/xml/"
        },
        "breathe_default_project": "Pinocchio",
        "exhaleExecutesDoxygen": False,
        "verboseBuild": True,  # Helpful for debugging
    }

    # Configure and generate Pinocchio documentation
    import exhale
    exhale.configs._exhale_args = pinocchio_args
    exhale.environment.apply_sphinx_configurations(app)
    exhale.generate()

    # Now configure Exhale for Aligator
    aligator_args = {
        "containmentFolder": "./api/aligator",
        "rootFileName": "aligator_root.rst",
        "doxygenStripFromPath": "../../src/stack/aligator",
        "rootFileTitle": "Aligator API",
        "createTreeView": True,
        # Tell Exhale to only process Aligator's XML
        "breathe_projects": {
            "Aligator": "../src/stack/aligator/build/doc/xml/"
        },
        "breathe_default_project": "Aligator",
        "exhaleExecutesDoxygen": False,
        "verboseBuild": True,
    }

    # Configure and generate Aligator documentation
    exhale.configs._exhale_args = aligator_args
    exhale.generate()

    print("Successfully generated separate API documentation for Pinocchio and Aligator")


def organize_api_by_namespace(app: Sphinx, exception):
    """
    Post-process the generated API files to organize them into subdirectories
    based on their namespace or content.
    """
    if exception:
        return

    api_dir = Path(app.srcdir) / 'api'

    if not api_dir.exists():
        print("WARNING: API directory does not exist, skipping organization")
        return

    # Create subdirectories for each project
    pinocchio_dir = api_dir / 'pinocchio'
    aligator_dir = api_dir / 'aligator'
    pinocchio_dir.mkdir(exist_ok=True)
    aligator_dir.mkdir(exist_ok=True)

    # Move files based on their namespace
    moved_count = {'pinocchio': 0, 'aligator': 0}

    for rst_file in api_dir.glob('*.rst'):
        # Skip the root file and any index files
        if rst_file.name in ['library_root.rst', 'index.rst']:
            continue

        # Read the file to determine which project it belongs to
        try:
            content = rst_file.read_text(encoding='utf-8')

            # Check for namespace indicators
            if 'namespacepinocchio' in rst_file.name or 'namespace_pinocchio' in rst_file.name or 'pinocchio::' in content:
                # Move to pinocchio subdirectory
                dest = pinocchio_dir / rst_file.name
                shutil.move(str(rst_file), str(dest))
                moved_count['pinocchio'] += 1

            elif 'namespacealigator' in rst_file.name or 'namespace_aligator' in rst_file.name or 'aligator::' in content:
                # Move to aligator subdirectory
                dest = aligator_dir / rst_file.name
                shutil.move(str(rst_file), str(dest))
                moved_count['aligator'] += 1

        except Exception as e:
            print(f"WARNING: Could not process {rst_file}: {e}")

    # Update the root file to point to the new locations
    update_root_file_references(api_dir / 'library_root.rst', moved_count)

    print(f"API organization complete: {moved_count['pinocchio']} files -> pinocchio/, "
          f"{moved_count['aligator']} files -> aligator/")



def update_root_file_references(root_file_path, moved_count):
    """
    Update the library_root.rst file to reflect the new file organization.
    """
    if not root_file_path.exists():
        return

    try:
        content = root_file_path.read_text(encoding='utf-8')

        # Update references to moved files
        # This is a simple approach - you might need to adjust based on your specific structure
        content = content.replace('namespace_pinocchio', 'pinocchio/namespace_pinocchio')
        content = content.replace('namespace_aligator', 'aligator/namespace_aligator')
        content = content.replace('classpinocchio_', 'pinocchio/classpinocchio_')
        content = content.replace('classaligator_', 'aligator/classaligator_')
        content = content.replace('structpinocchio_', 'pinocchio/structpinocchio_')
        content = content.replace('structaligator_', 'aligator/structaligator_')

        root_file_path.write_text(content, encoding='utf-8')
        print(f"Updated root file references: {root_file_path}")

    except Exception as e:
        print(f"WARNING: Could not update root file: {e}")


# --- CUSTOM BUILD STEP TO CLEAN DOXYGEN XML ---

def run_xml_cleaner(app: Sphinx, config):
    """
    Hook to run our XML cleaning script before Breathe processes the files.
    """
    # Path to the cleaning script, relative to conf.py
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'doc/clean_doxygen_xml.py'))

    if not os.path.exists(script_path):
        print("WARNING: XML cleaning script not found at:", script_path)
        return

    # Get the XML output directories from Breathe's config
    breathe_xml_dirs = app.config.breathe_projects.values()

    for xml_dir in breathe_xml_dirs:
        # The path in breathe_projects is relative to conf.py
        abs_xml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), xml_dir))
        index_xml_path = os.path.join(abs_xml_dir, 'index.xml')

        # Run the cleaning script on the index.xml file
        # We use sys.executable to ensure we're using the same python interpreter
        # that is running Sphinx.
        subprocess.run([sys.executable, script_path, index_xml_path], check=True)


def setup(app: Sphinx):
    """
    Register our custom function with a Sphinx event.
    'config-inited' is a good event because it runs early.
    """
    app.connect('config-inited', run_xml_cleaner)

    # Then generate the API documentation
#    app.connect('builder-inited', configure_exhale_for_multiproject)

    # Organize files after build is complete
    app.connect('build-finished', organize_api_by_namespace)
