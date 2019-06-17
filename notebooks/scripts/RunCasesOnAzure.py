#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Underlying script to create widgets for RunCasesOnAzure.
"""
import os
import sys
import functools
import ipywidgets
import IPython.display

# make this directory searchable for Python modules
script_dir = os.path.dirname(os.path.abspath(__file__))

if script_dir in sys.path:
    sys.path.remove(script_dir)

sys.path.insert(0, script_dir)

# import common from this "scripts" folder
import common


def encrypted_file_credential_box():
    """A box container for encrypted file credential.
    """

    file_selector_box = common.dir_or_file_selector_pair(
        "file", "Encrypted file path",
        "Clicl to select the encrypted file of Azure credential.",
        "The path to the encrypted file of Azure credential.")

    passcode_box = common.label_password_pair("Passcode", "Passcode")

    return ipywidgets.VBox(
        children=[file_selector_box, passcode_box],
        layout={"width": "100%", "flex": "1 1 auto"})

def credential_provider_box():
    """A box asking for Azure credential.
    """
    from NewEncryptedAzureCredential import azure_credential_request_box

    credential_option_box = common.label_dropdown_pair(
        "Provide Azure credential by", "Encrypted file",
        ["Manual input", "Encrypted file"])

    manual_input_box = azure_credential_request_box()
    encrypted_file_box = encrypted_file_credential_box()

    accordion = ipywidgets.Accordion(
        children=[manual_input_box, encrypted_file_box],
        layout={"flex": "1, 1, 90%"})

    accordion.real_widgets = {
        "manual": {
            "batch_name": manual_input_box.children[0].children[1],
            "batch_key": manual_input_box.children[1].children[1],
            "batch_url": manual_input_box.children[2].children[1],
            "storage_name": manual_input_box.children[3].children[1],
            "storage_key": manual_input_box.children[4].children[1]},
        "file": {
            "filepath_button": encrypted_file_box.children[0].children[1],
            "filepath_text": encrypted_file_box.children[0].children[2],
            "passcode": encrypted_file_box.children[1].children[1]}}

    credential_option_change_event({"new": "Encrypted file"}, accordion)

    credential_option_box.children[1].observe(functools.partial(
        credential_option_change_event, accordion=accordion), names="value")

    return ipywidgets.VBox(
        children=[credential_option_box, accordion],
        layout={"width": "100%", "flex": "1 1 auto"})


def display_gui():
    """Display the GUI interface of this tool.
    """

    # load CSS style
    css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    IPython.display.display(IPython.display.HTML(open(css, 'r').read()))

    # create and assemble widgets
    yaml_selector_box = common.dir_or_file_selector_pair(
        "file", "Project YAML file",
        "Clicl to select the YAML file of the project.",
        "The path to the project YAML file.")

    max_vm_nodes_box = common.label_boundedinttext_pair(
        "Max. allowed number of computing nodes", 2, 1, None, 1)

    node_type_box = common.label_dropdown_pair(
        "Type of computing nodes", "STANDARD_H8",
        ["STANDARD_A1_V2", "STANDARD_H8", "STANDARD_H16"])

    credential_option_box = credential_provider_box()

    ignore_exist_chk_box = ipywidgets.Checkbox(
        value=True, indent=False,
        layout={"width": "90%", "flex": "1 1 auto", "align-self": "left"},
        description="Do not re-submit a case if it already exists on Azure.")

    run_button = ipywidgets.Button(
        value="", description="Run", disable=False, button_style="",
        tooltip="Execute the tool",
        layout=ipywidgets.Layout(width="30%"))

    run_button.style.font_weight = "bold"

    msg = ipywidgets.Output(layout={"width": "100%"})

    # the big box
    box = ipywidgets.VBox(
        children=[yaml_selector_box, max_vm_nodes_box, node_type_box,
                  credential_option_box, ignore_exist_chk_box, run_button, msg],
        layout={"width": "100%", "flex": "1 1 auto"})

    # display in the notebook
    IPython.display.display(box)

def credential_option_change_event(changes, accordion):
    """A call back event when a user changes the way to input credential.
    """

    # a reference to underlying real widgets
    widgets = accordion.real_widgets

    if changes["new"] == "Manual input":

        accordion.selected_index = 0
        accordion.set_title(0, "Manual input")
        accordion.set_title(1, "Encrypted file (Not available)")

        # manual input Box
        for widget in widgets["manual"].values():
            widget.disabled = False
            widget.value = ""
            widget.placeholder = widget.placeholder_backup

        # file selector Box
        widgets["file"]["filepath_button"].disabled = True
        widgets["file"]["filepath_text"].disabled = True
        widgets["file"]["filepath_text"].placeholder = \
            "Only available when choosing \"Encrypted file\""
        widgets["file"]["filepath_text"].value = ""
        widgets["file"]["passcode"].disabled = True
        widgets["file"]["passcode"].value = ""
        widgets["file"]["passcode"].placeholder = \
            "Only available when choosing \"Encrypted file\""

    elif changes["new"] == "Encrypted file":

        accordion.selected_index = 1
        accordion.set_title(0, "Manual input (Not available)")
        accordion.set_title(1, "Encrypted file")

        # manial input Box
        for widget in widgets["manual"].values():
            widget.disabled = True
            widget.value = ""
            widget.placeholder = "Only available when choosing \"Manual input\""

        # file selector Box
        widgets["file"]["filepath_button"].disabled = False
        widgets["file"]["filepath_text"].disabled = False
        widgets["file"]["filepath_text"].placeholder = \
            widgets["file"]["filepath_text"].placeholder_backup
        widgets["file"]["filepath_text"].value = ""
        widgets["file"]["passcode"].disabled = False
        widgets["file"]["passcode"].value = ""
        widgets["file"]["passcode"].placeholder = \
            widgets["file"]["passcode"].placeholder_backup
