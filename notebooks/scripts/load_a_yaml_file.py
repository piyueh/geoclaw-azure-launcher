#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
GUI box of loading an existing YAML file.
"""
import os
import sys
import functools
import collections
import ipywidgets as widgets

# make this directory searchable for Python modules
script_dir = os.path.dirname(os.path.abspath(__file__))

if script_dir in sys.path:
    sys.path.remove(script_dir)

sys.path.insert(0, script_dir)

# import common from this "scripts" folder
import common

def load_a_yaml_file_gui():
    """The GUI interface of the tool creating a new YAML."""

    # the largest box
    frame = widgets.VBox(
        layout={
            "width": "69%", "flex": "1 1 auto", "border": "1px solid black",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # select a file path
    select_file = common.dir_or_file_selector_pair(
        "file", "Select a YAML file", "Select a project YAML file",
        "Path to a project YAML file")

    # "load" button
    load_button = widgets.Button(description="Load")
    load_button.layout.margin = "10px 2px 2px 2px"
    load_button.style.button_color = "slategray"
    load_button.style.font_weight = "bold"

    # set children of the largest box
    frame.children = [select_file, load_button]

    # an easier way to access components
    frame.data = {}
    frame.data["yaml_path"] = select_file.children[2]
    frame.data["load"] = load_button

    return frame
