#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Functions for the box of basic settings.
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

def create_basic_setting_box():
    """Create the box of basic settings."""

    box = widgets.VBox()
    box.data = {}
    children = collections.OrderedDict()

    # basic settings: working directory
    children["wd"] = common.dir_or_file_selector_pair(
        "dir", "Working directory:", "Select a working directory",
        "Working directory")
    box.data["wd"] = children["wd"].children[2]

    # basic settings: rupture points
    children["rupture_points"] = common.dir_or_file_selector_pair(
        "file", "Rupture point shapefile:", "Select a shapefile",
        "Shapefile for rupture points")
    box.data["rupture_points"] = children["rupture_points"].children[2]

    # basic settings: leak profile
    children["leak_profile"] = common.label_table_input_pair(
        "Leak profile:", "Number of stages",
        ["Stage end time (sec)", "Stage leak rate (m^3/sec)"],
        [widgets.BoundedIntText, widgets.BoundedFloatText],
        [{"value": 1, "min": 1, "max": 999999, "step": 1},
         {"value": 0, "min": 0, "max": 999999, "step": 0.01}])
    box.data["leak_profile"] = children["leak_profile"].children[1].children[1]

    # basic settings: simulation time
    children["simulation_time"] = common.label_boundedinttext_pair(
        "Simulation time (minutes):", 480, 0, 999999, 1)
    box.data["simulation_time"] = children["simulation_time"].children[1]

    # basic settings: output time spacing
    children["output_time_spacing"] = common.label_boundedinttext_pair(
        "Output time spacing (minutes):", 2, 0, 999999, 1)
    box.data["output_time_spacing"] = children["output_time_spacing"].children[1]

    # basic settings: topography provider
    children["topography_provider"] = common.label_dropdown_pair(
        "Topography provider:", "from 3DEP server",
        ["from 3DEP server", "local file"])
    box.data["topography_provider"] = children["topography_provider"].children[1]

    # basic setings: topography file selector
    children["topography_selector"] = common.dir_or_file_selector_pair(
        "file", "Topography DEM:", "Select topography DEM file",
        "Topography DEM file")
    children["topography_selector"].layout.visibility = "hidden"
    children["topography_selector"].children[1].disabled = True
    children["topography_selector"].children[2].disabled = True
    box.data["topography_selector"] = children["topography_selector"].children[2]

    # basic settings: hydrological provider
    children["hydrologic_provider"] = common.label_dropdown_pair(
        "Hydrology provider:", "from NHD server",
        ["from NHD server", "local files"])
    box.data["hydrologic_provider"] = children["hydrologic_provider"].children[1]

    # basic settings: hydrological selector
    children["hydrologic_selector"] = common.dir_or_file_selector_pair(
        "file", "Hydrologic files:", "Select hydrologic files",
        "Hydrologic files", True)
    children["hydrologic_selector"].layout.visibility = "hidden"
    children["hydrologic_selector"].children[1].disabled = True
    children["hydrologic_selector"].children[2].disabled = True
    box.data["hydrologic_selector"] = children["hydrologic_selector"].children[2]

    # basic settings: use topo res as grid res
    children["use_topo_res_as_grid_res"] = widgets.Checkbox(
        value=False, indent=False,
        layout={"visibility": "hidden", "width": "1 1 90%"},
        description="Use topography DEM resolution as the resolution of " +
                    "the computational grid")
    box.data["use_topo_res_as_grid_res"] = children["use_topo_res_as_grid_res"]

    # basic settings: finest grid resolutions
    children["finest_grid_resolutions"] = widgets.HBox([
        widgets.Label("Finest grid resolutions (m):", layout={"flex": "1 1 35%"}),
        widgets.BoundedFloatText(
            description="x:", value=1.0, min=1e-6, max=1e6, step=0.01,
            style={"description_width": "initial"}, layout={"flex": "1 1 25%"}),
        widgets.BoundedFloatText(
            description="y:", value=1.0, min=1e-6, max=1e6, step=0.01,
            style={"description_width": "initial"}, layout={"flex": "1 1 25%"})])
    box.data["finest_grid_resolutions"] = {}
    box.data["finest_grid_resolutions"]["x"] = children["finest_grid_resolutions"].children[1].value
    box.data["finest_grid_resolutions"]["y"] = children["finest_grid_resolutions"].children[2].value

    # basic settings: relative computational domain
    children["relative_computational_domain"] = widgets.HBox([
        widgets.Label("Relative computational domain (m):", layout={"flex": "1 1 35%"}),
        widgets.VBox([
            widgets.BoundedFloatText(
                description="top (north):", value=1000.0, min=0.1, max=1e6, step=0.1,
                style={"description_width": "initial"}, layout={"flex": "1 1 90%"}),
            widgets.BoundedFloatText(
                description="bottom (south):", value=1000.0, min=0.1, max=1e6, step=0.1,
                style={"description_width": "initial"}, layout={"flex": "1 1 90%"}),
            widgets.BoundedFloatText(
                description="left (west):", value=1000.0, min=0.1, max=1e6, step=0.1,
                style={"description_width": "initial"}, layout={"flex": "1 1 90%"}),
            widgets.BoundedFloatText(
                description="right (east):", value=1000.0, min=0.1, max=1e6, step=0.1,
                style={"description_width": "initial"}, layout={"flex": "1 1 90%"})
        ], layout={"flex": "1 1 50%"})])
    box.data["relative_computational_domain"] = {}
    for i, key in enumerate(["top", "bottom", "left", "right"]):
        box.data["relative_computational_domain"][key] = \
            children["relative_computational_domain"].children[1].children[i]

    # register callback functions
    children["topography_provider"].children[1].observe(
        functools.partial(
            topo_observer_callback, selector=children["topography_selector"],
            checkbox=children["use_topo_res_as_grid_res"]),
        names="value")

    children["hydrologic_provider"].children[1].observe(
        functools.partial(
            topo_hydro_observer_callback, selector=children["hydrologic_selector"]),
        names="value")

    children["use_topo_res_as_grid_res"].observe(
        functools.partial(
            topo_res_checkbox_observer_callback,
            res_box=children["finest_grid_resolutions"]),
        names="value")

    # copy references of widgets to the box
    box.children = tuple(children.values())

    return box

def topo_observer_callback(change, selector, checkbox):
    """Callback function specifically for the topography section."""

    topo_hydro_observer_callback(change, selector)

    if change["new"] == "local file":
        checkbox.layout.visibility = "visible"
        checkbox.value = True
    else:
        checkbox.layout.visibility = "hidden"
        checkbox.value = False

def topo_hydro_observer_callback(change, selector):
    """Callback event when changing the way to provide topo/hydro files"""

    if change["new"] in ["local file", "local files"]:
        selector.layout.visibility = "visible"
        selector.children[1].disabled = False
        selector.children[2].disabled = False
    else:
        selector.layout.visibility = "hidden"
        selector.children[1].disabled = True
        selector.children[2].disabled = True

def topo_res_checkbox_observer_callback(change, res_box):
    """Callback function for the checkbox of using topo resolution."""

    if change["new"]:
        res_box.layout.visibility = "hidden"
    else:
        res_box.layout.visibility = "visible"
