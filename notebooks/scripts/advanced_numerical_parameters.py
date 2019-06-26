#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Functions related to the section of advanced numerical parameters.
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

def create_advanced_numerical_parameters_box():
    """Create the box for fluid settings."""

    box = widgets.VBox()
    box.data = {}
    children = collections.OrderedDict()

    # advanced numerical parameters: initial dt
    children["initial_dt"] = common.label_boundedfloattext_pair(
        "Initial time step (seconds):", 0, 0, 1e6, 1e-6)
    box.data["initial_dt"] = children["initial_dt"].children[1]

    # advanced numerical parameters: max dt
    children["max_dt"] = common.label_boundedfloattext_pair(
        "Maximum time step (seconds):", 4, 0, 1e6, 1e-6)
    box.data["max_dt"] = children["max_dt"].children[1]

    # advanced numerical parameters: desired cfl
    children["desired_cfl"] = common.label_boundedfloattext_pair(
        "Desired CFL number:", 0.9, 0, 1.0, 1e-3)
    box.data["desired_cfl"] = children["desired_cfl"].children[1]

    # advanced numerical parameters: max cfl
    children["max_cfl"] = common.label_boundedfloattext_pair(
        "Maximum CFL number:", 0.95, 0, 1.0, 1e-3)
    box.data["max_cfl"] = children["max_cfl"].children[1]

    # advanced numerical parameters: total AMR levels
    children["total_AMR_levels"] = common.label_boundedinttext_pair(
        "Total AMR levels:", 2, 2, 10, 1)
    box.data["total_AMR_levels"] = children["total_AMR_levels"].children[1]

    # advanced numerical parameters: AMR refinement ratio
    children["AMR_refinement_ratio"] = common.label_boundedinttext_pair(
        "AMR refinement ratio:", 4, 2, 1024, 1)
    box.data["AMR_refinement_ratio"] = children["AMR_refinement_ratio"].children[1]

    # copy references of widgets to the box
    box.children = tuple(children.values())

    return box
