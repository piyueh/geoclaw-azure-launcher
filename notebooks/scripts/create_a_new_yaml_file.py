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

def create_a_new_yaml_file_gui():
    """The GUI interface of the tool creating a new YAML."""

    # the largest box
    frame = widgets.VBox(
        layout={"width": "69%", "flex": "1 1 auto", "border": "1px solid black",
            "padding": "2px 2px 2px 2px", "align_items": "flex-start"})

    # a button to import existing YAML file for later modification
    import_button = widgets.Button(
        description="Import", layout={"padding": "2px 2px 2px 2px"})

    # a button to save existing YAML settings
    save_as_button = widgets.Button(
        description="Save as", layout={"padding": "2px 2px 2px 2px"})

    # the setting section is an accordion
    setting_section = widgets.Accordion(
        layout={"width": "100%", "flex": "1 1 auto", "border": "1px solid black",
            "padding": "2px 2px 2px 2px", "align_items": "stretch"})

    # set children of the largest box
    frame.children = [widgets.HBox([import_button, save_as_button]), setting_section]

    # an easier way to access components
    frame.data = {}
    frame.data["import"] = import_button
    frame.data["save_as"] = save_as_button
    frame.data["settings"] = setting_section

    # =============================
    # now setup the setting_section
    #==============================

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
    setting_section.set_title(0, "Project metadata")
    setting_section.set_title(1, "Basic settings")
    setting_section.set_title(2, "Fluid settings")
    setting_section.set_title(3, "Darcy-Weisbach settings")
    setting_section.set_title(4, "Miscellaneous")
    setting_section.set_title(5, "Advanced numerical parameters")

    # an easier way to access data
    setting_section.data = {}
    setting_section.data["project_metadata"] = proj_meta
    setting_section.data["basic_settings"] = basic
    setting_section.data["fluid_settings"] = fluid
    setting_section.data["darcy_weisbach_settings"] = darcy_weisbach
    setting_section.data["misc_settings"] = misc
    setting_section.data["advanced_numerical_parameters"] = advanced

    return frame
