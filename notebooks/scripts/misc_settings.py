#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Functions related to miscellaneous settings.
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

def create_misc_setting_box():
    """Create the box for misc settings."""

    box = widgets.VBox()
    box.data = {}
    children = collections.OrderedDict()

    # misc: local folder
    children["local_folder"] = widgets.HBox([
        widgets.Label("Local folder:", layout={"flex": "1 1 35%"}),
        widgets.VBox([
            widgets.Checkbox(
                description="Force creation even if a folder already exists",
                value=True, indent=False, layout={"flex": "1 1 60%"})
        ], layout={
            "flex": "1 1 65%", "border": "0.5px solid grey",
            "padding": "1px 1px 5px 5px"})
    ], layout={"margin": "2px 2px 2px 2px"})
    box.data["local_folder"] = {}
    box.data["local_folder"]["force_creation"] = children["local_folder"].children[1].children[0]

    # misc: submission to cloud
    children["submission_to_cloud"] = widgets.HBox([
        widgets.Label("Submission to cloud:", layout={"flex": "1 1 35%"}),
        widgets.VBox([
            widgets.Checkbox(
                description="Skip submission if a case is not found locally",
                value=False, indent=False, layout={"flex": "1 1 60%"}),
            widgets.Checkbox(
                description="Skip submission if a case already exists on cloud",
                value=True, indent=False, layout={"flex": "1 1 60%"}),
        ], layout={
            "flex": "1 1 65%", "border": "0.5px solid grey",
            "padding": "1px 1px 5px 5px"})
    ], layout={"margin": "2px 2px 2px 2px"})
    box.data["submission_to_cloud"] = {}
    box.data["submission_to_cloud"]["skip_if_not_found_on_local"] = \
        children["submission_to_cloud"].children[1].children[0]
    box.data["submission_to_cloud"]["skip_if_exist_on_remote"] = \
        children["submission_to_cloud"].children[1].children[1]

    # misc: downloading
    children["downloading"] = widgets.HBox([
        widgets.Label("Downloading:", layout={"flex": "1 1 35%"}),
        widgets.VBox([
            widgets.Checkbox(
                description="Use sync mode",
                value=True, indent=False, layout={"flex": "1 1 60%"}),
            widgets.Checkbox(
                description="Skip GeoClaw raw data when downloading",
                value=True, indent=False, layout={"flex": "1 1 60%"}),
            widgets.Checkbox(
                description="Skip raster files when downloading",
                value=True, indent=False, layout={"flex": "1 1 60%"}),
        ], layout={
            "flex": "1 1 65%", "border": "0.5px solid grey",
            "padding": "1px 1px 5px 5px"})
    ], layout={"margin": "2px 2px 2px 2px"})
    box.data["downloading"] = {}
    box.data["downloading"]["sync_mode"] = \
        children["downloading"].children[1].children[0]
    box.data["downloading"]["skip_raw_data"] = \
        children["downloading"].children[1].children[1]
    box.data["downloading"]["skip_rasters"] = \
        children["downloading"].children[1].children[2]

    # copy references of widgets to the box
    box.children = tuple(children.values())

    return box
