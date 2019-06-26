#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
GUI box of creating a new YAML file.
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
import basic_settings
import fluid_darcy_weisbach_settings
import misc_settings
import advanced_numerical_parameters

def load_a_yaml_file_box():
    """The GUI interface for loading a YAML file."""

    # the largest box
    frame = widgets.VBox(
        layout={
            "width": "100%", "flex": "1 1 auto", "border": "1px solid gray",
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

def create_a_new_yaml_file_box():
    """The GUI interface for creating a new YAML file."""

    # the largest box
    frame = widgets.VBox(
        layout={
            "width": "100%", "flex": "1 1 auto", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # the setting section is an accordion
    setting_section = widgets.Accordion(
        layout={"width": "100%", "flex": "1 1 auto",
            "padding": "2px 2px 2px 2px", "align_items": "stretch"})

    # =============================
    # now setup the setting_section
    # =============================

    # project metadata
    proj_meta = widgets.VBox([
        common.label_text_pair("Project name:", "Project name"),
        common.label_text_pair("Timestamp:", "Auto-set when saved")])

    proj_meta.data = {
        "proj_name": proj_meta.children[0].children[1],
        "timestamp": proj_meta.children[1].children[1]}

    proj_meta.data["timestamp"].disabled = True

    # basic settings
    basic = basic_settings.create_basic_setting_box()

    # fluid settings
    fluid = fluid_darcy_weisbach_settings.create_fluid_setting_box()

    # Darcy-Weisbach settings
    darcy_weisbach = fluid_darcy_weisbach_settings.create_darcy_weisbach_setting_box()

    # misc
    misc = misc_settings.create_misc_setting_box()

    # advanced numerical parameters
    advanced = advanced_numerical_parameters.create_advanced_numerical_parameters_box()

    # final organizing
    setting_section.children = [proj_meta, basic, fluid, darcy_weisbach, misc, advanced]
    setting_section.selected_index = None
    setting_section.set_title(0, "Project metadata")
    setting_section.set_title(1, "Basic settings")
    setting_section.set_title(2, "Fluid settings")
    setting_section.set_title(3, "Darcy-Weisbach settings")
    setting_section.set_title(4, "Miscellaneous")
    setting_section.set_title(5, "Advanced numerical parameters")

    # a button to save existing YAML settings
    save_as_button = widgets.Button(
        description="Save as", layout={"padding": "2px 2px 2px 2px"})

    save_as_button.layout.margin = "10px 2px 2px 2px"
    save_as_button.style.button_color = "slategray"
    save_as_button.style.font_weight = "bold"

    # set children of the largest box
    frame.children = (setting_section, save_as_button)

    # an easier way to access data
    frame.data = {}
    frame.data["save_as"] = save_as_button
    frame.data["settings"] = setting_section
    frame.data["project_metadata"] = proj_meta
    frame.data["basic_settings"] = basic
    frame.data["fluid_settings"] = fluid
    frame.data["darcy_weisbach_settings"] = darcy_weisbach
    frame.data["misc_settings"] = misc
    frame.data["advanced_numerical_parameters"] = advanced

    return frame

def create_tool_gui():
    """Create the GUI for the tool "Load/Create a YAML"."""

    # a label as the title of loading
    label_load = widgets.Label(value="Load a YAML file")
    label_load.add_class("bold-face")

    # the largest box
    frame = widgets.VBox(
        layout={
            "flex": "1 1 auto", "border": "1px solid black",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # the section of loading a YAML
    load_section = load_a_yaml_file_box()

    # a label between two sections
    label_or = widgets.Label(value="or create a new one")
    label_or.add_class("bold-face")

    # the section of creating a new YAML
    create_section = create_a_new_yaml_file_box()

    # finish the frame
    frame.children = (label_load, load_section, label_or, create_section)

    return frame
