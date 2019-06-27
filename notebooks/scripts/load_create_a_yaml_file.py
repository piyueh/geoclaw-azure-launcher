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
import ipywidgets

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
    frame = ipywidgets.VBox(
        layout={
            "width": "100%", "flex": "1 1 auto", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # select a file path
    select_file = common.dir_or_file_selector_pair(
        "file", "Select a YAML file", "Select a project YAML file",
        "Path to a project YAML file")

    # "load" button
    load_button = ipywidgets.Button(description="Load")
    load_button.layout.margin = "10px 2px 2px 2px"
    load_button.style.button_color = "slategray"
    load_button.style.font_weight = "bold"

    # set children of the largest box
    frame.children = [select_file, load_button]

    # an easier way to access components
    frame.data = {}
    frame.data["yamlpath"] = select_file.children[2]
    frame.data["load"] = load_button

    return frame

def create_a_new_yaml_file_box():
    """The GUI interface for creating a new YAML file."""

    # the largest box
    frame = ipywidgets.VBox(
        layout={
            "width": "100%", "flex": "1 1 auto", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # the setting section is an accordion
    setting_section = ipywidgets.Accordion(
        layout={"width": "100%", "flex": "1 1 auto",
            "padding": "2px 2px 2px 2px", "align_items": "stretch"})

    # =============================
    # now setup the setting_section
    # =============================

    # project metadata
    proj_meta = ipywidgets.VBox([
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
    save_as_button = ipywidgets.Button(
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
    label_load = ipywidgets.Label(value="Load a YAML file")
    label_load.add_class("bold-face")

    # the largest box
    frame = ipywidgets.VBox(
        layout={
            "flex": "1 1 auto", "border": "1px solid black",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # the section of loading a YAML
    load_section = load_a_yaml_file_box()

    # a label between two sections
    label_or = ipywidgets.Label(value="or create a new one")
    label_or.add_class("bold-face")

    # the section of creating a new YAML
    create_section = create_a_new_yaml_file_box()

    # finish the frame
    frame.children = (label_load, load_section, label_or, create_section)

    # easy access
    frame.data = {}
    frame.data["load"] = load_section
    frame.data["create"] = create_section
    frame.data["filepath"] = None
    frame.data["yaml"] = None
    frame.data["msg"] = None
    frame.data["extracallback"] = None

    # register on-click events
    load_section.data["load"].on_click(functools.partial(
        common.on_click_wrapper, gui=frame, true_event=load_event))

    return frame

def load_event(gui):
    """Load an existing project YAML."""
    import yaml

    # make sure the correct object is passed in
    assert "load" in gui.data.keys()
    assert "create" in gui.data.keys()
    assert "filepath" in gui.data.keys()
    assert "yaml" in gui.data.keys()

    # update filepath
    gui.data["filepath"] = gui.data["load"].data["yamlpath"].value

    # open and read yaml
    with open(gui.data["filepath"], "r") as f:
        gui.data["yaml"] = yaml.load(f, Loader=yaml.SafeLoader)

    # update possible relative paths to absolute paths
    gui.data["yaml"] = common.convert_to_abspath(gui.data["filepath"], gui.data["yaml"])

    # update information in GUI with the YAML data
    translate_yaml_to_gui(gui.data["yaml"], gui.data["create"])

def translate_yaml_to_gui(yamldata, gui):
    """Translate YAML dict to GUI."""

    # meta data
    cgui = gui.data["project_metadata"].data
    cyaml = yamldata["project metadata"]
    cgui["proj_name"].value = cyaml["name"]
    cgui["timestamp"].value = cyaml["timestamp"].strftime("%Y-%m-%dT%H:%M:%S%z")

    # basic settings
    cgui = gui.data["basic_settings"].data
    cyaml = yamldata["basic settings"]
    cgui["wd"].value = cyaml["working directory"]
    cgui["rupture_points"].value = cyaml["rupture points"]
    cgui["n_leak_profile"].value = len(cyaml["leak profile"])
    for i, data in enumerate(cyaml["leak profile"]):
        cgui["leak_profile"].children[i+1].children[0].value = data["end time"]
        cgui["leak_profile"].children[i+1].children[1].value = data["rate"]
    cgui["simulation_time"].value = cyaml["simulation time"]
    cgui["output_time_spacing"].value = cyaml["output time spacing"]

    if cyaml["topography file"] == "from 3DEP server":
        cgui["topography_provider"].value = cyaml["topography file"]
    else:
        cgui["topography_provider"].value = "local file"
        cgui["topography_selector"].value = cyaml["topography file"]

    if cyaml["hydrologic files"] == "from NHD server":
        cgui["hydrologic_provider"].value = cyaml["hydrologic files"]
    else:
        cgui["hydrologic_provider"].value = "local files"
        temp = ""
        for i in cyaml["hydrologic files"]:
            temp += ";{}".format(i)
        cgui["hydrologic_selector"].value = temp.lstrip(";")

    if cyaml["use topo res as grid res"]:
        cgui["use_topo_res_as_grid_res"].value = cyaml["use topo res as grid res"]

    if cyaml["finest grid resolutions"]:
        cgui["finest_grid_resolutions"]["x"].value = cyaml["finest grid resolutions"]["x"]
        cgui["finest_grid_resolutions"]["y"].value = cyaml["finest grid resolutions"]["y"]

    for key in ["top", "bottom", "left", "right"]:
        cgui["relative_computational_domain"][key].value = \
            cyaml["relative computational domain"][key]

    # fluid settings
    cgui = gui.data["fluid_settings"].data
    cyaml = yamldata["fluid settings"]
    cgui["ref_dynamic_viscosity"].value = cyaml["ref dynamic viscosity"]
    cgui["ref_temperature"].value = cyaml["ref temperature"]
    cgui["ambient_temperature"].value = cyaml["ambient temperature"]
    cgui["density"].value = cyaml["density"]
    cgui["evaporation"]["model"].value = cyaml["evaporation model"]["model"]

    if cyaml["evaporation model"]["coefficients"]:
        cgui["evaporation"]["coefficients"].children[0].value = \
            cyaml["evaporation model"]["coefficients"][0]
        cgui["evaporation"]["coefficients"].children[1].value = \
            cyaml["evaporation model"]["coefficients"][1]

    # darcy-weisbach settings
    cgui = gui.data["darcy_weisbach_settings"].data
    cyaml = yamldata["darcy-weisbach settings"]
    cgui["coefficient_model"].value = cyaml["coefficient model"]
    cgui["surface_roughness"].value = cyaml["surface roughness"]

    # misc settings
    cgui = gui.data["misc_settings"].data
    cyaml = yamldata["misc settings"]
    cgui["local_folder"]["force_creation"].value = cyaml["local folder"]["force creation"]
    cgui["submission_to_cloud"]["skip_if_not_found_on_local"].value = \
        cyaml["submission to cloud"]["skip if not found on local"]
    cgui["submission_to_cloud"]["skip_if_exist_on_remote"].value = \
        cyaml["submission to cloud"]["skip if exist on remote"]
    cgui["downloading"]["sync_mode"].value = cyaml["downloading"]["sync mode"]
    cgui["downloading"]["skip_raw_data"].value = cyaml["downloading"]["skip raw data"]
    cgui["downloading"]["skip_rasters"].value = cyaml["downloading"]["skip rasters"]

    # advanced_numerical_parameters
    cgui = gui.data["advanced_numerical_parameters"].data
    cyaml = yamldata["advanced numerical parameters"]
    cgui["initial_dt"].value = cyaml["initial dt"]
    cgui["max_dt"].value = cyaml["max dt"]
    cgui["desired_cfl"].value = cyaml["desired cfl"]
    cgui["max_cfl"].value = cyaml["max cfl"]
    cgui["total_AMR_levels"].value = cyaml["total AMR levels"]
    cgui["AMR_refinement_ratio"].value = cyaml["AMR refinement ratio"]

    # open the project metadata page of the GUI
    gui.data["settings"].selected_index = 0
