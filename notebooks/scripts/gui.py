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
import ipywidgets as widgets
import IPython.display

# make this directory searchable for Python modules
script_dir = os.path.dirname(os.path.abspath(__file__))

if script_dir in sys.path:
    sys.path.remove(script_dir)

sys.path.insert(0, script_dir)

# import common from this "scripts" folder
import common
import load_create_a_yaml_file

def create_status_box():
    """The status box."""

    # the indicator of current project YAML file
    proj_yaml_box = widgets.HBox(children=[widgets.Label(), widgets.Label()])
    proj_yaml_box.layout.width = "100%"
    proj_yaml_box.layout.flex = "1 1 auto"
    proj_yaml_box.layout.padding = "2px 2px 2px 2px"

    # legend lable
    proj_yaml_box.children[0].value = "Current project setting:"
    proj_yaml_box.children[0].layout.width = "35"
    proj_yaml_box.children[0].add_class("bold-face")

    # content
    proj_yaml_box.children[1].value = "None"
    proj_yaml_box.children[1].layout.flex = "1 1 auto"
    proj_yaml_box.children[1].layout.border = "1px solid black"
    proj_yaml_box.children[1].add_class("centered-text")


    # the indicator of the credential file being used
    cred_file_box = widgets.HBox(children=[widgets.Label(), widgets.Label()])
    cred_file_box.layout = {"width": "100%", "flex": "1 1 auto"}
    cred_file_box.layout.padding = "2px 2px 2px 2px"

    # legend lable
    cred_file_box.children[0].value = "Current Azure credential file:"
    cred_file_box.children[0].layout.width = "35"
    cred_file_box.children[0].add_class("bold-face")

    # content
    cred_file_box.children[1].value = "None"
    cred_file_box.children[1].layout.flex = "1 1 auto"
    cred_file_box.children[1].layout.border = "1px solid black"
    cred_file_box.children[1].add_class("centered-text")

    # final box
    current_status_box = widgets.VBox([proj_yaml_box, cred_file_box])
    current_status_box.layout.flex = "1 1 auto"
    current_status_box.layout.border = "1.5px solid black"

    # add direct access to status display widgets
    current_status_box.current_yaml = proj_yaml_box.children[1]
    current_status_box.current_cred = cred_file_box.children[1]
    current_status_box.layout.padding = "2px 2px 2px 2px"
    current_status_box.layout.margin = "2px 2px 2px 2px"

    # easy access
    current_status_box.data = {
        "proj_yaml": proj_yaml_box.children[1],
        "cred_file": cred_file_box.children[1]}

    return current_status_box

def create_buttons():
    """Create a column of buttons to change the content in the display."""

    button_column = widgets.VBox()
    button_column.layout.width = "25%"
    button_column.layout.flex = "0 1 auto"
    button_column.layout.padding = "2px 2px 2px 2px"
    button_column.layout.align_items = "center"

    buttons = []
    button_column.data = {}

    # load or create a new YAML file
    button_column.data["load_create_a_yaml_file"] = widgets.Button()
    button_column.data["load_create_a_yaml_file"].description = "Load/Create a YAML file"
    button_column.data["load_create_a_yaml_file"].id = "load_create_a_yaml_file"
    buttons.append(button_column.data["load_create_a_yaml_file"])

    # create a new credential file
    button_column.data["create_a_new_credential"] = widgets.Button()
    button_column.data["create_a_new_credential"].description = "Create a new credential file"
    button_column.data["create_a_new_credential"].id = "create_a_new_credential"
    buttons.append(button_column.data["create_a_new_credential"])

    # create Azure resources
    button_column.data["create_azure_resources"] = widgets.Button()
    button_column.data["create_azure_resources"].description = "Create Azure resources"
    button_column.data["create_azure_resources"].id = "create_azure_resources"
    buttons.append(button_column.data["create_azure_resources"])

    # submit jobs
    button_column.data["submit_tasks_to_azure"] = widgets.Button()
    button_column.data["submit_tasks_to_azure"].description = "Submit tasks to Azure"
    button_column.data["submit_tasks_to_azure"].id = "submit_tasks_to_azure"
    buttons.append(button_column.data["submit_tasks_to_azure"])

    # submit jobs
    button_column.data["monitor_progress"] = widgets.Button()
    button_column.data["monitor_progress"].description = "Monitor progress"
    button_column.data["monitor_progress"].id = "monitor_progress"
    buttons.append(button_column.data["monitor_progress"])

    # download cases
    button_column.data["download_cases"] = widgets.Button()
    button_column.data["download_cases"].description = "Download cases"
    button_column.data["download_cases"].id = "download_cases"
    buttons.append(button_column.data["download_cases"])

    # delete Azure resources
    button_column.data["delete_azure_resources"] = widgets.Button()
    button_column.data["delete_azure_resources"].description = "Delete Azure resources"
    button_column.data["delete_azure_resources"].id = "delete_azure_resources"
    buttons.append(button_column.data["delete_azure_resources"])

    # add buttons to the column box
    button_column.children = buttons

    # change the width of all buttons
    for child in button_column.children:
        child.layout.width = "95%"

    return button_column

def button_actions(button, gui):
    """Callback for buttons' actions."""

    gui.data["display"].children = (gui.data["buttons"], gui.data[button.id])


# ============
# GUI
# ============

# load CSS style
css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
IPython.display.display(IPython.display.HTML(open(css, 'r').read()))

# the top most level of the GUI interface
gui = widgets.VBox()
gui.layout.flex = "1 1 auto"

gui.data = {}
gui.data["status"] = create_status_box()
gui.data["display"] = widgets.HBox()
gui.data["display"].layout.flex = "1 1 auto"
gui.data["display"].layout.border = "1.5px solid black"
gui.data["display"].layout.margin = "2px 2px 2px 2px"
gui.data["display"].layout.padding = "2px 2px 2px 2px"
gui.children = (gui.data["status"], gui.data["display"])

# options in "display"
gui.data["buttons"] = create_buttons()
gui.data["load_create_a_yaml_file"] = load_create_a_yaml_file.create_tool_gui()
gui.data["create_a_new_credential"] = widgets.VBox()
gui.data["create_azure_resources"] = widgets.VBox()
gui.data["submit_tasks_to_azure"] = widgets.VBox()
gui.data["monitor_progress"] = widgets.VBox()
gui.data["download_cases"] = widgets.VBox()
gui.data["delete_azure_resources"] = widgets.VBox()

# the default content in "display"
gui.data["display"].children = (gui.data["buttons"], gui.data["load_create_a_yaml_file"])

# register the callback of buttons' actions
for button in gui.data["buttons"].children:
    button.on_click(functools.partial(button_actions, gui=gui))

# show the GUI in the notebook
IPython.display.display(gui)
