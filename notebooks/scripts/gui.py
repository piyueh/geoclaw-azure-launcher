#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
The GUI for using GeoClaw for HCA analysis purpose.
"""
import os
import sys
import functools
import collections
import ipywidgets
import IPython.display

# make this directory searchable for Python modules
script_dir = os.path.dirname(os.path.abspath(__file__))

if script_dir in sys.path:
    sys.path.remove(script_dir)

sys.path.insert(0, script_dir)

# import common from this "scripts" folder
import common
import load_create_a_yaml_file
import load_create_a_credential_file
import create_geoclaw_cases

def create_status_box():
    """The status box."""

    # box
    status_box = ipywidgets.VBox()
    status_box.layout.flex = "1 1 auto"
    status_box.layout.border = "1.5px solid black"
    status_box.layout.padding = "2px 2px 2px 2px"
    status_box.layout.margin = "2px 2px 2px 2px"

    status_box.data = collections.OrderedDict()
    metadata = collections.OrderedDict([
        ("proj_yaml", "Current project setting:"),
        ("cred_file", "Current Azure credential file:")])

    for k, v in metadata.items():
        status_box.data[k] = ipywidgets.HBox(
            children=[ipywidgets.Label(), ipywidgets.Label()])
        status_box.data[k].layout.width = "100%"
        status_box.data[k].layout.flex = "1 1 auto"
        status_box.data[k].layout.padding = "2px 2px 2px 2px"

        # legend lable
        status_box.data[k].children[0].value = v
        status_box.data[k].children[0].layout.width = "35"
        status_box.data[k].children[0].add_class("bold-face")

        # content
        status_box.data[k].children[1].value = "None"
        status_box.data[k].children[1].layout.flex = "1 1 auto"
        status_box.data[k].children[1].layout.border = "1px solid black"
        status_box.data[k].children[1].add_class("centered-text")

    # setup children
    status_box.children = tuple(status_box.data.values())

    # re-link the key to the real widget
    for k, v in metadata.items():
        status_box.data[k] = status_box.data[k].children[1]

    return status_box

def create_buttons():
    """Create a column of buttons to change the content in the display."""

    button_column = ipywidgets.VBox()
    button_column.layout.width = "25%"
    button_column.layout.flex = "0 0 auto"
    button_column.layout.padding = "2px 2px 2px 2px"
    button_column.layout.align_items = "center"

    button_column.data = collections.OrderedDict()
    metadata = collections.OrderedDict([
        ("load_create_a_yaml_file", "Load/Create a YAML file"),
        ("load_create_a_credential_file", "Load/Create a credential file"),
        ("create_geoclaw_cases", "Create GeoClaw cases"),
        ("create_azure_resources", "Create Azure resources"),
        ("submit_tasks_to_azure", "Submit tasks to Azure"),
        ("monitor_progress", "Monitor progress"),
        ("download_cases", "Download cases"),
        ("delete_azure_resources", "Delete Azure resources")])

    for k, v in metadata.items():
        button_column.data[k] = ipywidgets.Button()
        button_column.data[k].description = v
        button_column.data[k].id = k
        button_column.data[k].layout.width = "95%"

    button_column.children = tuple(button_column.data.values())

    return button_column

def button_actions(button, gui):
    """Callback for buttons' actions."""

    gui.data["display"].children = (gui.data["buttons"], gui.data[button.id])

def set_credential_status(cred_box, status_box):
    """Set the file path to status box."""

    status_box.data["cred_file"].value = cred_box.data["filepath"]

def set_yaml_status(yaml_box, status_box):
    """Set the file path to status box."""

    status_box.data["proj_yaml"].value = yaml_box.data["filepath"]


# ============
# GUI
# ============

# load CSS style
css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
IPython.display.display(IPython.display.HTML(open(css, 'r').read()))

# the top most level of the GUI interface
gui = ipywidgets.VBox()
gui.layout.flex = "1 1 auto"

gui.data = {}
gui.data["status"] = create_status_box()
gui.data["display"] = ipywidgets.HBox()
gui.data["display"].layout.flex = "1 1 auto"
gui.data["display"].layout.border = "1.5px solid black"
gui.data["display"].layout.margin = "2px 2px 2px 2px"
gui.data["display"].layout.padding = "2px 2px 2px 2px"
gui.data["msg"] = ipywidgets.Output()
gui.data["msg"].layout.border = "1.5px solid black"
gui.children = (
    gui.data["status"], gui.data["display"],
    ipywidgets.Label("Output message:"), gui.data["msg"])

# all panels in "display"
gui.data["buttons"] = create_buttons()
gui.data["load_create_a_yaml_file"] = load_create_a_yaml_file.create_tool_gui()
gui.data["load_create_a_credential_file"] = load_create_a_credential_file.create_tool_gui()
gui.data["create_geoclaw_cases"] = \
    create_geoclaw_cases.create_tool_gui(gui.data["load_create_a_yaml_file"])
gui.data["create_azure_resources"] = ipywidgets.VBox()
gui.data["submit_tasks_to_azure"] = ipywidgets.VBox()
gui.data["monitor_progress"] = ipywidgets.VBox()
gui.data["download_cases"] = ipywidgets.VBox()
gui.data["delete_azure_resources"] = ipywidgets.VBox()

# the default content in "display"
gui.data["display"].children = (gui.data["buttons"], gui.data["load_create_a_yaml_file"])

# register the callback of buttons' actions
for button in gui.data["buttons"].children:
    button.on_click(functools.partial(button_actions, gui=gui))

# register output widget to all tools
for key in ["load_create_a_yaml_file", "load_create_a_credential_file", "create_geoclaw_cases"]:
    gui.data[key].data["msg"] = gui.data["msg"]

# register extra callback
gui.data["load_create_a_yaml_file"].data["extracallback"] = \
    functools.partial(
        set_yaml_status, yaml_box=gui.data["load_create_a_yaml_file"],
        status_box=gui.data["status"])

gui.data["load_create_a_credential_file"].data["extracallback"] = \
    functools.partial(
        set_credential_status, cred_box=gui.data["load_create_a_credential_file"],
        status_box=gui.data["status"])

# show the GUI in the notebook
IPython.display.display(gui)
