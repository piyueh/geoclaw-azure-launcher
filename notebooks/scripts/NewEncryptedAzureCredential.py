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
import tkinter
import tkinter.filedialog
import ipywidgets
import traitlets
import IPython.display


def azure_batch_account_name():
    """Return a HBox for asking Azure Batch account name.
    """

    batch_account_name_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="Azure Batch account name")

    batch_account_name_text = ipywidgets.Password(
        placeholder="Azure Batch account name",
        layout=ipywidgets.Layout(width="65%"))

    batch_account_name_box = ipywidgets.HBox(
        children=[batch_account_name_label, batch_account_name_text],
        layout=ipywidgets.Layout(width="90%"))

    return batch_account_name_box

def azure_batch_account_key():
    """Return a HBox for asking Azure Batch account key.
    """

    batch_account_key_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="Azure Batch account key")

    batch_account_key_text = ipywidgets.Password(
        value="",
        placeholder="Azure Batch account key",
        layout=ipywidgets.Layout(width="65%"))

    batch_account_key_box = ipywidgets.HBox(
        children=[batch_account_key_label, batch_account_key_text],
        layout=ipywidgets.Layout(width="90%"))

    return batch_account_key_box

def azure_batch_account_url():
    """Return a HBox for asking Azure Batch account URL.
    """

    batch_account_URL_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="Azure Batch account URL")

    batch_account_URL_text = ipywidgets.Password(
        placeholder="Azure Batch account URL",
        layout=ipywidgets.Layout(width="65%"))

    batch_account_URL_box = ipywidgets.HBox(
        children=[batch_account_URL_label, batch_account_URL_text],
        layout=ipywidgets.Layout(width="90%"))

    return batch_account_URL_box

def azure_storage_account_name():
    """Return a HBox for asking Azure Storage account name.
    """
    storage_account_name_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="Azure Storage account name")

    storage_account_name_text = ipywidgets.Password(
        placeholder="Azure Storage account name",
        layout=ipywidgets.Layout(width="65%"))

    storage_account_name_box = ipywidgets.HBox(
        children=[storage_account_name_label, storage_account_name_text],
        layout=ipywidgets.Layout(width="90%"))

    return storage_account_name_box

def azure_storage_account_key():
    """Return a HBox for asking Azure Storage account key.
    """

    storage_account_key_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="Azure Storage account key")

    storage_account_key_text = ipywidgets.Password(
        value="",
        placeholder="Azure Storage account key",
        layout=ipywidgets.Layout(width="65%"))

    storage_account_key_box = ipywidgets.HBox(
        children=[storage_account_key_label, storage_account_key_text],
        layout=ipywidgets.Layout(width="90%"))

    return storage_account_key_box

def passcode():
    """Asking for a passcode to encrypt the credential.
    """

    passcode_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"), value="Passcode")

    passcode_text = ipywidgets.Password(
        value="",
        placeholder="Passcode", layout=ipywidgets.Layout(width="65%"))

    passcode_box = ipywidgets.HBox(
        children=[passcode_label, passcode_text],
        layout=ipywidgets.Layout(width="90%"))

    return passcode_box

def confirm_passcode():
    """Asking for a confirmation to the passcode.
    """

    confirm_passcode_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"), value="Confirm passcode")

    confirm_passcode_text = ipywidgets.Password(
        value="",
        placeholder="Confirm passcode", layout=ipywidgets.Layout(width="65%"))

    confirm_passcode_box = ipywidgets.HBox(
        children=[confirm_passcode_label, confirm_passcode_text],
        layout=ipywidgets.Layout(width="90%"))

    return confirm_passcode_box

def dir_selection():
    """The widget box asking for an output directory.
    """

    dir_select_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="The directory where the encrypted file will be output to")

    dir_select_label.add_class("label-wrapped")

    dir_select_button = ipywidgets.Button(
        value="", description="Click to select", disable=False, button_style="",
        tooltip="The directory where the encrypted file will be output to.",
        layout=ipywidgets.Layout(width="20%"))

    dir_path_text = ipywidgets.Text(
        disable=False, placeholder="The path to the output directory",
        layout=ipywidgets.Layout(width="45%"),
        description="")

    dir_select_button.on_click(
        functools.partial(dir_select_event, text=dir_path_text))

    dir_select_box = ipywidgets.HBox(
        children=[dir_select_label, dir_select_button, dir_path_text],
        layout=ipywidgets.Layout(width="90%"))

    return dir_select_box

def output_filename():
    """The name of the output encrypted file.
    """

    file_name_label = ipywidgets.Label(
        layout=ipywidgets.Layout(width="25%"),
        value="The name of the resulting encrypted credential file")

    file_name_label.add_class("label-wrapped")

    file_name_text = ipywidgets.Text(
        disable=False, layout=ipywidgets.Layout(width="65%"),
        placeholder="The name of the resulting encrypted credential file",
        description="")

    file_name_box = ipywidgets.HBox(
        children=[file_name_label, file_name_text],
        layout=ipywidgets.Layout(width="90%"))

    return file_name_box

def run_button():
    """A button to run the tool.
    """

    run_button = ipywidgets.Button(
        value="", description="Run", disable=False, button_style="",
        tooltip="Execute the tool",
        layout=ipywidgets.Layout(width="30%"))

    return run_button

def display_tool_gui():
    """Display all widgets with a big VBox.
    """

    # load CSS style
    css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    IPython.display.display(IPython.display.HTML(open(css, 'r').read()))

    # create widgets
    batch_name = azure_batch_account_name()
    batch_key = azure_batch_account_key()
    batch_url = azure_batch_account_url()
    storage_name = azure_storage_account_name()
    storage_key = azure_storage_account_key()
    passcode_1 = passcode()
    passcode_2 = confirm_passcode()
    wd = dir_selection()
    fn = output_filename()
    button = run_button()

    # an extra output message widget
    msg = ipywidgets.Output(layout=ipywidgets.Layout(width="90%"))

    # the big box
    box = ipywidgets.VBox(
        children=[batch_name, batch_key, batch_url,
                  storage_name, storage_key,
                  passcode_1, passcode_2, wd, fn, button, msg],
        layout=ipywidgets.Layout(width="100%"))

    # bind button click event
    button.on_click(functools.partial(run, big_box=box))

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

def run(button, big_box):
    """Event when an user click the "Run" button.

    Args:
        button: A ipywidgets.Button object.

        big_box: the box containing this tool
    """

    # capture stdout and stderr in the Output widget
    with big_box.children[-1]:

        # clean the message in the output widget
        IPython.display.clear_output()

        # the real/underlying event
        run_real(big_box)

def run_real(big_box):
    """The real work when an user click run.

    Args:
        big_box: the box containing this tool
    """

    # tricky part: import helper module using relative path to this file
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if root in sys.path:
        sys.path.remove(root)

    sys.path.insert(0, root)
    import helpers.azuretools

    # check passcodes
    print("Checking passcodes.")

    check_passcode(
        big_box.children[5].children[1].value,
        big_box.children[6].children[1].value)

    # UserCredential object
    print("Creating an UserCredential instance.")

    UC = helpers.azuretools.UserCredential(
        big_box.children[0].children[1].value,
        big_box.children[1].children[1].value,
        big_box.children[2].children[1].value,
        big_box.children[3].children[1].value,
        big_box.children[4].children[1].value)

    # write to file
    filepath = os.path.join(
        big_box.children[7].children[2].value,
        big_box.children[8].children[1].value)

    print("Writing an encrypted file to\n\t{}.".format(filepath))

    UC.write_encrypted(big_box.children[5].children[1].value, filepath)

    # output success message to the output widget
    print("\nSuccess!\n")

def dir_select_event(button, text):
    """Pop up a tk window for folder selection.

    Args:
        button: A ipywidgets.Button object.

        text: A ipywidgets.Text object.
    """

    tkinter.Tk().withdraw() # Close the root window
    dir_path = tkinter.filedialog.askdirectory()

    # if users indeed select a folder, update the value of the Text object
    if isinstance(dir_path, str):
        text.value = dir_path
