# Minimal config just for Aligator
import sys
import os

project = 'Aligator API'
extensions = ['breathe', 'exhale']

breathe_projects = {
    "Aligator": "../../src/stack/aligator/build/doc/xml/",
}
breathe_default_project = "Aligator"

exhale_args = {
    "containmentFolder":     "./api/aligator",
    "rootFileName":          "aligator_root.rst",
    "doxygenStripFromPath":  "../../src/stack/aligator",
    "rootFileTitle":         "Aligator API Reference",
    "createTreeView":        True,
    "exhaleExecutesDoxygen": False,
}
