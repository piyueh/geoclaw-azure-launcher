#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Load or create an Azure credential file.
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

def load_a_credential_file_box():
    """The GUI interface for loading an Azure credential file."""

    # the largest box
    frame = ipywidgets.VBox(
        layout={
            "width": "100%", "flex": "1 1 auto", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # select a file path
    select_file = common.dir_or_file_selector_pair(
        "file", "Select a credential file", "Select an Azure credential file",
        "Path to an Azure credential file")

    select_file.layout.width = "100%"

    # asking for the passcode
    passcode_box = common.label_password_pair("Passcode", "Passcode")

    # "load" button
    load_button = ipywidgets.Button(description="Load")
    load_button.layout.margin = "10px 2px 2px 2px"
    load_button.style.button_color = "slategray"
    load_button.style.font_weight = "bold"

    # set children of the largest box
    frame.children = [select_file, passcode_box, load_button]

    # an easier way to access components
    frame.data = {}
    frame.data["filepath"] = select_file.children[2]
    frame.data["passcode"] = passcode_box.children[1]
    frame.data["load"] = load_button

    return frame

def create_a_new_credential_file_box():
    """The GUI interface for creating a new credential file."""

    # the largest box
    frame = ipywidgets.VBox(
        layout={
            "width": "100%", "flex": "1 1 auto", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # Azure Batch and Storage information
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

    passcode = common.label_password_pair("Passcode", "Passcode")

    confirm_passcode = common.label_password_pair("Confirm passcode", "Confirm passcode")

    # a button to save existing YAML settings
    save_as_button = ipywidgets.Button(
        description="Save as", layout={"padding": "2px 2px 2px 2px"})

    save_as_button.layout.margin = "10px 2px 2px 2px"
    save_as_button.style.button_color = "slategray"
    save_as_button.style.font_weight = "bold"

    # set children of the largest box
    frame.children = (
        batch_name, batch_key, batch_url, storage_name, storage_key, passcode,
        confirm_passcode, save_as_button)

    # an easier way to access data
    frame.data = {}
    frame.data["batch_name"] = batch_name.children[1]
    frame.data["batch_key"] = batch_key.children[1]
    frame.data["batch_url"] = batch_url.children[1]
    frame.data["storage_name"] = storage_name.children[1]
    frame.data["storage_key"] = storage_key.children[1]
    frame.data["passcode"] = passcode.children[1]
    frame.data["confirm_passcode"] = confirm_passcode.children[1]
    frame.data["save_as"] = save_as_button

    return frame

def create_tool_gui():
    """Create the GUI for the tool "Load/Create a YAML"."""

    # a label as the title of loading
    label_load = ipywidgets.Label(value="Load a credential file")
    label_load.add_class("bold-face")

    # the largest box
    frame = ipywidgets.VBox(
        layout={
            "flex": "1 1 auto", "border": "1px solid black",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"})

    # the section of loading a YAML
    load_section = load_a_credential_file_box()

    # a label between two sections
    label_or = ipywidgets.Label(value="or create a new one")
    label_or.add_class("bold-face")

    # the section of creating a new YAML
    create_section = create_a_new_credential_file_box()

    # finish the frame
    frame.children = (label_load, load_section, label_or, create_section)

    # easy access
    frame.data = {}
    frame.data["load"] = load_section
    frame.data["create"] = create_section
    frame.data["filepath"] = None
    frame.data["credential"] = None
    frame.data["msg"] = None
    frame.data["extracallback"] = None

    # register on-click events
    load_section.data["load"].on_click(functools.partial(
        common.on_click_wrapper, gui=frame, true_event=load_event))
    create_section.data["save_as"].on_click(functools.partial(
        common.on_click_wrapper, gui=frame, true_event=save_as_event))

    return frame

def load_event(gui):
    """Real callback after clicking "Save as"."""
    import tkinter
    import tkinter.filedialog

    # tricky part: import helper module using relative path to this file
    root = os.path.dirname(os.path.dirname(script_dir))

    if root in sys.path:
        sys.path.remove(root)

    sys.path.insert(0, root)
    import helpers.azuretools

    # make sure the correct object is passed in
    assert "load" in gui.data.keys()
    assert "create" in gui.data.keys()
    assert "credential" in gui.data.keys()
    assert "filepath" in gui.data.keys()

    # reference to the dictionary of underlying real widgets
    widgets = gui.data["load"].data

    # filepath
    gui.data["filepath"] = widgets["filepath"].value

    # UserCredential
    gui.data["credential"] = helpers.azuretools.UserCredential()
    gui.data["credential"].read_encrypted(
        widgets["passcode"].value, widgets["filepath"].value)

    # clear passcode input
    widgets["passcode"].value = ""

    # extra call back function
    if gui.data["extracallback"] is not None:
        gui.data["extracallback"]()

    # message
    print("Done loading credential file.")

def save_as_event(gui):
    """Real callback after clicking "Save as"."""
    import tkinter
    import tkinter.filedialog

    # tricky part: import helper module using relative path to this file
    root = os.path.dirname(os.path.dirname(script_dir))

    if root in sys.path:
        sys.path.remove(root)

    sys.path.insert(0, root)
    import helpers.azuretools

    # make sure the correct object is passed in
    assert "load" in gui.data.keys()
    assert "create" in gui.data.keys()
    assert "credential" in gui.data.keys()
    assert "filepath" in gui.data.keys()

    # pop-up for asking path to save
    tkinter.Tk().withdraw()
    filepath = tkinter.filedialog.asksaveasfilename(
        initialdir="./", initialfile="azure_cred.bin")

    if not isinstance(filepath, str) or len(filepath)==0:
        print("Creation is canceled.")
        return

    # reference to the dictionary of underlying real widgets
    widgets = gui.data["create"].data

    # check passcodes
    print("Checking passcodes.")
    check_passcode(widgets["passcode"].value, widgets["confirm_passcode"].value)

    # UserCredential object
    print("Creating an UserCredential instance.")
    UC = helpers.azuretools.UserCredential(
        widgets["batch_name"].value, widgets["batch_url"].value,
        widgets["batch_key"].value, widgets["storage_name"].value,
        widgets["storage_key"].value)

    print("Writing an encrypted file to\n\t{}.".format(filepath))
    UC.write_encrypted(widgets["passcode"].value, filepath)

    # output success message to the output widget
    print("Creation succeeded!\n")

    # save opened credential to gui
    gui.data["credential"] = UC
    gui.data["filepath"] = filepath

    # extra call back function
    if gui.data["extracallback"] is not None:
        gui.data["extracallback"]()

def check_passcode(passcode1, passcode2):
    """Check passcodes."""

    if not isinstance(passcode1, str):
        raise TypeError("Passcode should be a string.")

    if not passcode1:
        raise ValueError("The provided passcode is an empty string.")

    if passcode1 != passcode2:
        raise ValueError("The first passcode does not match the second one.")
