#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Functions related to fluid and Darcy-Weisbach settings.
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

def create_fluid_setting_box():
    """Create the box for fluid settings."""

    box = widgets.VBox()
    box.data = {}
    children = collections.OrderedDict()

    # fluid setting: ref dynamic viscosity
    children["ref_dynamic_viscosity"] = common.label_boundedfloattext_pair(
        "Ref. dynamic viscosity (cP):", 332, 0, 1e6, 0.01)
    box.data["ref_dynamic_viscosity"] = children["ref_dynamic_viscosity"].children[1]

    # fluid setting: ref temperature
    children["ref_temperature"] = common.label_boundedfloattext_pair(
        "Ref. temperature (Celsius):", 15, 0, 1e6, 0.1)
    box.data["ref_temperature"] = children["ref_temperature"].children[1]

    # fluid setting: ambient temperature
    children["ambient_temperature"] = common.label_boundedfloattext_pair(
        "Ambient temperature (Celsius):", 25, 0, 1e6, 0.1)
    box.data["ambient_temperature"] = children["ambient_temperature"].children[1]

    # fluid setting: density
    children["density"] = common.label_boundedfloattext_pair(
        "Density (m^3/kg):", 15, 0, 1e6, 0.1)
    box.data["density"] = children["density"].children[1]

    # fluid setting: evaporation
    children["evaporation"] = widgets.HBox([
        widgets.Label("Evaporation model:", layout={"flex": "1 1 35%"}),
        widgets.VBox([
            widgets.Dropdown(
                description="model:", value="Fingas1996 Log Law",
                options=["None", "Fingas1996 Log Law", "Fingas1996 SQRT Law"],
                style={"description_width": "initial"}),
            widgets.HBox([
                widgets.BoundedFloatText(
                    description="C1:", value=1.38, min=0., max=1e6, step=1e-3,
                    style={"description_width": "initial"}),
                widgets.BoundedFloatText(
                    description="C2:", value=0.045, min=0., max=1e6, step=1e-3,
                    style={"description_width": "initial"})])
        ], layout={
            "flex": "1 1 65%", "border": "0.5px solid gray",
            "padding": "1px 1px 5px 10px"})
    ])
    box.data["evaporation"] = {}
    box.data["evaporation"]["model"] = children["evaporation"].children[1].children[0]
    box.data["evaporation"]["coefficients"] = children["evaporation"].children[1].children[1]

    # register callback
    box.data["evaporation"]["model"].observe(
        functools.partial(
            evap_model_observer_callback,
            coeff_box=box.data["evaporation"]["coefficients"]),
        names="value")

    # copy references of widgets to the box
    box.children = tuple(children.values())

    return box

def create_darcy_weisbach_setting_box():
    """Create the box for Darcy-Weisbach settings."""

    box = widgets.VBox()
    box.data = {}
    children = collections.OrderedDict()

    # darcy-weisbach settings: coefficient model
    children["coefficient_model"] = common.label_dropdown_pair(
        "Coefficient model:", "Three-regime model", ["None", "Three-regime model"])
    box.data["coefficient_model"] = children["coefficient_model"].children[1]

    # darcy-weisbach settings: surface roughness
    children["surface_roughness"] = common.label_boundedfloattext_pair(
        "Surface roughness (m):", 0.1, 0., 1e6, 0.01)
    box.data["surface_roughness"] = children["surface_roughness"].children[1]

    # copy references of widgets to the box
    box.children = tuple(children.values())

    return box

def evap_model_observer_callback(change, coeff_box):
    """Callback function for evaporation model options."""

    if change["new"] == "None":
        coeff_box.children=[]
    else:
        coeff_box.children=[
            widgets.BoundedFloatText(
                description="C1:", value=1.38, min=0., max=1e6, step=1e-3,
                style={"description_width": "initial"}),
            widgets.BoundedFloatText(
                description="C2:", value=0.045, min=0., max=1e6, step=1e-3,
                style={"description_width": "initial"})
        ]
