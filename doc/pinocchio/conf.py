# Minimal config just for Pinocchio
import sys
import os

import subprocess
from sphinx.application import Sphinx
import shutil


project = 'Pinocchio API'
extensions = ['breathe', 'exhale']

breathe_projects = {
    "Pinocchio": "../../src/stack/pinocchio/build/doc/xml/",
}
breathe_default_project = "Pinocchio"

exhale_args = {
    "containmentFolder":     "./api/pinocchio",
    "rootFileName":          "pinocchio_root.rst",
    "doxygenStripFromPath":  "../../src/stack/pinocchio",
    "rootFileTitle":         "Pinocchio API Reference",
    "createTreeView":        True,
    "exhaleExecutesDoxygen": False,
}
