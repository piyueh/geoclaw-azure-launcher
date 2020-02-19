#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Create Resources on Azure.
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

def create_tool_gui(yaml_gui):
    """GUI of the tool creating GeoClaw case folders."""

    # the largest box
    frame = ipywidgets.VBox(
        layout={
            "flex": "1 1 auto", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # standard layou
    layout1 = {"width": "25%"}
    layout2 = {"width": "75%"}

    # box for pool information
    pool_box = ipywidgets.VBox(
        children=[
            ipywidgets.HBox([
                ipywidgets.Label("Batch pool name:", layout=layout1),
                ipywidgets.Text("landspill-azure-pool", layout=layout2, disabled=True)
            ], layout={"width": "100%"}),
        ],
        layout={
            "width": "100%", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center", "margin": "2px 2px 2px 2px"}
    )

    # box for job information
    job_box = ipywidgets.VBox(
        children=[
            ipywidgets.HBox([
                ipywidgets.Label("Batch job name:", layout=layout1),
                ipywidgets.Text("landspill-azure-job", layout=layout2, disabled=True)
            ], layout={"width": "100%"}),
        ],
        layout={
            "width": "100%", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center", "margin": "2px 2px 2px 2px"}
    )

    # box for container information
    container_box = ipywidgets.VBox(
        children=[
            ipywidgets.HBox([
                ipywidgets.Label("Storage container:", layout=layout1),
                ipywidgets.Text("landspill-azure-container", layout=layout2, disabled=True)
            ], layout={"width": "100%"})
        ],
        layout={
            "width": "100%", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center", "margin": "2px 2px 2px 2px"}
    )

    # add children to frame
    frame.children = (pool_box, job_box, container_box)

    # quick access
    frame.data = collections.OrderedDict()
    frame.data["yaml_gui_ref"] = yaml_gui
    frame.data["msg"] = None

    return frame
