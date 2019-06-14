#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Common functions used by other modules.
"""
import functools
import tkinter
import tkinter.filedialog
import ipywidgets
import IPython.display


def run_button():
    """A button to run the tool.
    """

    button = ipywidgets.Button(
        value="", description="Run", disable=False, button_style="",
        tooltip="Execute the tool", layout={"width": "30%"})

    button.style.font_weight = "bold"

    return button

def run(button, big_box, true_run):
    """Event when an user click the "Run" button.

    Args:
        button: A ipywidgets.Button object.
        big_box: the box containing this tool
        true_run: the true callback event function when clicking run.
    """

    # capture stdout and stderr in the Output widget
    # assume the last children is always an ipytwidget.Output
    with big_box.real_widgets["msg"]:

        # clean the message in the output widget
        IPython.display.clear_output()

        # the real/underlying event
        true_run(big_box)

def dir_selector_event(button, text):
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

def file_selector_event(button, text):
    """Underlying event when a user click yaml selector button.

    Args:
        button: a ipywidgets.Button object.
        text: a ipywidgets.Text object.
    """

    tkinter.Tk().withdraw() # Close the root window
    file_path = tkinter.filedialog.askopenfilename()

    # if users indeed select a folder, update the value of the Text object
    if isinstance(file_path, str):
        text.value = file_path

def label_text_pair(label_text, placeholder_text):
    """A helper to create a HBox with a Label and a Text widgets.

    Args:
        label_text: the text content in the label.
        placeholder_text: placeholder text in the Text widget.
    """

    label = ipywidgets.Label(value=label_text, layout={"flex": "1 1 35%"})

    password = ipywidgets.Text(
        placeholder=placeholder_text, layout={"flex": "1 1 65%"})

    # make a copy of the placeholder text
    password.placeholder_backup = password.placeholder

    box = ipywidgets.HBox(
        children=[label, password], layout=ipywidgets.Layout(width="100%"))

    return box

def label_password_pair(label_text, placeholder_text):
    """A helper to create a HBox with a Label and a Password widgets.

    Args:
        label_text: the text content in the label.
        placeholder_text: placeholder text in the password widget.
    """

    label = ipywidgets.Label(value=label_text, layout={"flex": "1 1 35%"})

    password = ipywidgets.Password(
        placeholder=placeholder_text, layout={"flex": "1 1 65%"})

    # make a copy of the placeholder text
    password.placeholder_backup = password.placeholder

    box = ipywidgets.HBox(
        children=[label, password], layout=ipywidgets.Layout(width="100%"))

    return box

def dir_or_file_selector_pair(
        dir_or_file, label_text, button_tooltip, input_placeholder):
    """Create a HBox asking the paht to a directory or a file.

    Args:
        dir_or_file: either "dir" or "file"
        label_text: content on the label
        button_tooltip: the tip when the mouse pointer stays longer on the button.
        input_placeholder: the placeholder in the Text widget.
    """

    label = ipywidgets.Label(value=label_text, layout={"flex": "1 1 35%"})

    button = ipywidgets.Button(
        description="Click to select", tooltip=button_tooltip,
        layout={"flex": "1 1 20%"})

    text = ipywidgets.Text(
        placeholder=input_placeholder, layout={"flex": "1 1 45%"})

    text.placeholder_backup = text.placeholder

    if dir_or_file == "dir":
        button.on_click(functools.partial(dir_selector_event, text=text))
    elif dir_or_file == "file":
        button.on_click(functools.partial(file_selector_event, text=text))
    else:
        raise ValueError("dir_or_file should be either \"dir\" or \"file\".")

    return ipywidgets.HBox(children=[label, button, text], layout={"width": "100%"})
