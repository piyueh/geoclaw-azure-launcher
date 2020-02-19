#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Create GeoClaw cases on a local machine.
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

    frame.data = collections.OrderedDict()

    # information header
    info_box = ipywidgets.VBox(
        layout={
            "width": "100%", "border": "1px solid gray",
            "padding": "2px 2px 2px 2px", "justify_content": "center",
            "align_items": "center"},
        children=[
            ipywidgets.HBox(
                children=[
                    ipywidgets.Label("Working directory:", layout={"width": "25%"}),
                    ipywidgets.Text(placeholder="N/A", layout={"width": "75%"}, disabled=True)
                ],
                layout={"width": "100%"}),
            ipywidgets.HBox(
                children=[
                    ipywidgets.Label("Rupture point shapefile:", layout={"width": "25%"}),
                    ipywidgets.Text(placeholder="N/A", layout={"width": "75%"}, disabled=True)
                ],
                layout={"width": "100%"}),
            ipywidgets.HBox(
                children=[
                    ipywidgets.Label("Total number of points:", layout={"width": "25%"}),
                    ipywidgets.Text(placeholder="N/A", layout={"width": "75%"}, disabled=True)
                ],
                layout={"width": "100%"})
        ])

    # a button to create folders
    create_button = ipywidgets.Button(
        description="Create folders",
        layout={
            "padding": "2px 2px 2px 2px", "margin": "10px 2px 2px 2px",
            "button_color": "slategray", "font_weight": "bold"
        })

    # label
    output_label = ipywidgets.Label("Case folder status:", layout={"width": "100%"})

    # progress bar
    progress_bar = ipywidgets.IntProgress(
        value=0, min=0, max=10, step=1, description='N/A',
        bar_style='info', orientation='horizontal',
        layout={"width": "100%", "padding": "1px 1px 1px 1px"},
        style={"description_width": "initial"})

    # a button to create folders
    refresh_button = ipywidgets.Button(
        description="Refresh status",
        layout={
            "padding": "2px 2px 2px 2px", "margin": "10px 2px 2px 2px",
            "button_color": "slategray", "font_weight": "bold"
        })

    # output area
    output = ipywidgets.Output(layout={"width": "100%"})

    # add children to frame
    frame.children = (
        info_box, create_button, output_label, progress_bar, output, refresh_button)

    # quick access
    frame.data["workdir"] = info_box.children[0].children[1]
    frame.data["filepath"] = info_box.children[1].children[1]
    frame.data["npoints"] = info_box.children[2].children[1]
    frame.data["create"] = create_button
    frame.data["progress"] = progress_bar
    frame.data["output"] = output
    frame.data["refresh"] = refresh_button
    frame.data["points"] = None
    frame.data["yaml_gui_ref"] = yaml_gui
    frame.data["msg"] = None

    # the path to the workdir
    ipywidgets.link(
        (yaml_gui.data["create"].data["basic_settings"].data["wd"], "value"),
        (frame.data["workdir"], "value"))

    # the path to the shapefile
    ipywidgets.link(
        (yaml_gui.data["create"].data["basic_settings"].data["rupture_points"], "value"),
        (frame.data["filepath"], "value"))

    # total number of points
    frame.data["filepath"].observe(
        functools.partial(filepath_observer_event, gui=frame), names="value")

    # register on-click events
    frame.data["create"].on_click(functools.partial(
        common.on_click_wrapper, gui=frame, true_event=create_button_event))

    frame.data["refresh"].on_click(functools.partial(
        common.on_click_wrapper, gui=frame, true_event=refresh_button_event))

    return frame

def filepath_observer_event(change, gui):
    """Observe the change of filepath."""
    import IPython.display
    import pandas

    assert change["new"] == gui.data["filepath"].value

    if change["new"] == "":
        gui.data["npoints"].value = ""
        gui.data["points"] = None
        gui.data["progress"].description = "N/A"
        gui.data["progress"].value = 0
        gui.data["progress"].max = 0
        with gui.data["output"]:
            IPython.display.clear_output()
        return

    gui.data["points"] = common.get_point_info(gui.data["workdir"].value, change["new"])
    refresh_button_event(gui)

def create_button_event(gui):
    """Create GeoClaw local case folders."""
    import rasterio

    # make sure the correct object is passed in
    keys = ["workdir", "filepath", "npoints", "create", "progress", "output",
            "refresh", "points"]

    for key in keys:
        assert key in gui.data.keys()

    if gui.data["points"] is None:
        return

    if gui.data["yaml_gui_ref"].data["yaml"] is None:
        raise ValueError("YAML not loaded!")

    # alias
    yamldata = gui.data["yaml_gui_ref"].data["yaml"] # alias
    points = gui.data["points"]
    recreate = yamldata["misc settings"]["local folder"]["force creation"]

    # obtain common settings
    common_params = common.obtain_common_yaml_settings(yamldata)

    # open the local topography if it exists
    if yamldata["basic settings"]["topography file"] != "from 3DEP server":
        toporaster = rasterio.open(yamldata["basic settings"]["topography file"], 'r')
    else:
        toporaster = None

    # hydrological data
    if yamldata["basic settings"]["hydrologic files"] != "from NHD server":
        hydrorasters = []
        for raster in yamldata["basic settings"]["hydrologic files"]:
            hydrorasters.append(rasterio.open(raster, 'r'))
    else:
        hydrorasters = None

    # loop through each point and create its case folder and setrun.py
    for i, point in enumerate(points):
        points[i]["Folder exist"] = False

        create_single_folder(common_params, point, toporaster, hydrorasters, recreate)

        # update progress bar
        gui.data["progress"].description = "{} exist / {} total".format(i+1, len(points))
        gui.data["progress"].value = i+1
        gui.data["progress"].max = len(points)

        points[i]["Folder exist"] = True

    # close topography raster
    if toporaster is not None:
        toporaster.close()

    # close hydrological rasters
    if hydrorasters is not None:
        for raster in hydrorasters:
            raster.close()

def create_single_folder(params, point, topo, hydros, recreate):
    """Create a single GeoClaw folder."""
    import shutil

    # add the top-most level to module search path
    root = os.path.dirname(os.path.dirname(script_dir))

    if root in sys.path:
        sys.path.remove(root)

    sys.path.insert(0, root)
    from helpers.arcgistools.write_geoclaw_params import write_setrun

    # setup the case folder path and create the folder
    params["out_dir"] = point["Path"]

    if os.path.isdir(params["out_dir"]):
        if recreate:
            shutil.rmtree(params["out_dir"])
        else:
            return

    os.makedirs(params["out_dir"], exist_ok=True)

    # copy the coordinates
    params["point"] = point["Coordinates"]

    # create topography file if not downloading from 3DEP
    if topo is not None:
        common.crop_raster(
            os.path.join(params["out_dir"], "topo.asc"),
            topo, point["Coordinates"], params["extent"], recreate)

    # create topography file if not downloading from 3DEP
    if hydros is not None:
        for i, raster in enumerate(hydros):
            common.crop_raster(
                os.path.join(params["out_dir"], "hydro_{}.asc".format(i)),
                raster, point["Coordinates"], params["extent"], recreate)

    # create setrun.py in the case folder
    write_setrun(**params)

def refresh_button_event(gui):
    """Refresh the case status."""
    import IPython.display
    import pandas

    # make sure the correct object is passed in
    keys = ["workdir", "filepath", "npoints", "create", "progress", "output",
            "refresh", "points"]

    for key in keys:
        assert key in gui.data.keys()

    if gui.data["points"] is None:
        return

    # get a pandas DataFrame
    df = pandas.DataFrame(
        gui.data["points"],
        columns=["Case ID", "Coordinates", "Folder exist", "Path"])

    # update number of points
    gui.data["npoints"].value = str(len(gui.data["points"]))

    # update progress bar
    gui.data["progress"].description = \
        "{} exist / {} total".format(
            df["Folder exist"].sum(), len(gui.data["points"]))

    gui.data["progress"].value = df["Folder exist"].sum()
    gui.data["progress"].max = len(gui.data["points"])

    # prepare panda array
    with gui.data["output"]:
        IPython.display.clear_output()
        IPython.display.display(df)
