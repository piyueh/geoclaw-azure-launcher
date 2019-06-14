#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Underlying script to create widgets for NewEncryptedAzureCredential.
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


def azure_credential_request_box():
    """Create a box for asking Azure credential info.
    """

    batch_name = common.label_password_pair(
        "Azure Batch account name", "Azure Batch account name")

    batch_key = common.label_password_pair(
        "Azure Batch account key", "Azure Batch account key")

    batch_url = common.label_password_pair(
        "Azure Batch account URL", "Azure Batch account URL")

    storage_name = common.label_password_pair(
        "Azure Storage account name", "Azure Storage account name")

    storage_key = common.label_password_pair(
        "Azure Storage account key", "Azure Storage account key")

    return ipywidgets.VBox(
        children=[batch_name, batch_key, batch_url, storage_name, storage_key],
        layout={"width": "100%", "flex": "1 1 auto"})

def new_passcode_request_box():
    """Create a box for asking encryption passcode and confirmation.
    """

    passcode = common.label_password_pair("Passcode", "Passcode")

    confirm_passcode = common.label_password_pair(
        "Confirm passcode", "Confirm passcode")

    return ipywidgets.VBox(
        children=[passcode, confirm_passcode],
        layout={"width": "100%", "flex": "1 1 auto"})

def output_info_request_box():
    """Create a VBox for asking for output path and filename.
    """

    output_dir = common.dir_or_file_selector_pair(
        "dir", "Output destination folder",
        "The directory where the encrypted file will be output to.",
        "The path to the output directory")

    output_filename = common.label_text_pair(
        "Output file name", "The name of the resulting encrypted credential file")

    return ipywidgets.VBox(
        children=[output_dir, output_filename],
        layout={"width": "100%", "flex": "1 1 auto"})

def display_gui():
    """Display all widgets with a big VBox.
    """

    # load CSS style
    css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    IPython.display.display(IPython.display.HTML(open(css, 'r').read()))

    # create and assemble widgets
    azure_credential_box = azure_credential_request_box()
    passcode_box = new_passcode_request_box()
    output_info_box = output_info_request_box()

    # the "Run" button
    run_button = common.run_button()

    # an extra output message widget
    msg = ipywidgets.Output(layout={"width": "100%"})

    # the big box
    box = ipywidgets.VBox(
        children=[
            azure_credential_box, passcode_box, output_info_box,
            run_button, msg],
        layout={"width": "100%", "flex": "1 1 auto"})

    # reference to the real widgets storing values
    box.real_widgets = {
        "batch_name": azure_credential_box.children[0].children[1],
        "batch_key": azure_credential_box.children[1].children[1],
        "batch_url": azure_credential_box.children[2].children[1],
        "storage_name": azure_credential_box.children[3].children[1],
        "storage_key": azure_credential_box.children[4].children[1],
        "passcode1": passcode_box.children[0].children[1],
        "passcode2": passcode_box.children[1].children[1],
        "wd": output_info_box.children[0].children[2],
        "fn": output_info_box.children[1].children[1],
        "msg": msg
    }

    # register the callback event when clicking the "Run" button
    run_button.on_click(functools.partial(
        common.run, big_box=box, true_run=run_real))

    # display in the notebook
    IPython.display.display(box)

def check_passcode(passcode1, passcode2):
    """Check passcodes.
    """

    if not isinstance(passcode1, str):
        raise TypeError("Passcode should be a string.")

    if not passcode1:
        raise ValueError("The provided passcode is an empty string.")

    if passcode1 != passcode2:
        raise ValueError("The first passcode does not match the second one.")

def run_real(big_box):
    """The real work when an user click run.

    Args:
        big_box: the box containing this tool
    """

    # tricky part: import helper module using relative path to this file
    root = os.path.dirname(os.path.dirname(script_dir))

    if root in sys.path:
        sys.path.remove(root)

    sys.path.insert(0, root)
    import helpers.azuretools

    # reference to the dictionary of underlying real widgets
    widgets = big_box.real_widgets

    # check passcodes
    print("Checking passcodes.")

    check_passcode(widgets["passcode1"].value, widgets["passcode2"].value)

    # UserCredential object
    print("Creating an UserCredential instance.")

    UC = helpers.azuretools.UserCredential(
        widgets["batch_name"].value, widgets["batch_url"].value,
        widgets["batch_key"].value, widgets["storage_name"].value,
        widgets["storage_key"].value)

    # write to file
    filepath = os.path.join(
        widgets["wd"].value, widgets["fn"].value)

    print("Writing an encrypted file to\n\t{}.".format(filepath))

    UC.write_encrypted(widgets["passcode1"].value, filepath)

    # output success message to the output widget
    print("\nSuccess!\n")
