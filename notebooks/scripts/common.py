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
import os
import sys
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

def file_selector_event(button, text, multiple=False):
    """Underlying event when a user click yaml selector button.

    Args:
        button: a ipywidgets.Button object.
        text: a ipywidgets.Text object.
    """

    tkinter.Tk().withdraw() # Close the root window

    if multiple:
        file_path = tkinter.filedialog.askopenfilenames()

        if len(file_path) > 0:
            temp = ""
            for p in file_path:
                temp += ";{}".format(p)
            file_path = temp.lstrip(";")
    else:
        file_path = tkinter.filedialog.askopenfilename()

    # if users indeed select a file, update the value of the Text object
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
        dir_or_file, label_text, button_tooltip, input_placeholder,
        multiple=False):
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
        button.on_click(functools.partial(
            file_selector_event, text=text, multiple=multiple))
    else:
        raise ValueError("dir_or_file should be either \"dir\" or \"file\".")

    return ipywidgets.HBox(children=[label, button, text])

def label_boundedinttext_pair(label_text, default_value, minimum, maximum, step):
    """A helper to create a HBox with a Label and a BoundedIntText widgets.

    Args:
        label_text: the text content in the label.
        default_value: the default value in the BoundedIntText.
        minimum: the minimum value allowed in the BoundedIntText.
        maximum: the maximum value allowed in the BoundedIntText.
        step: the size of increment used in the BoundedIntText.
    """

    label = ipywidgets.Label(
        value=label_text, layout={"flex": "1 1 35%", "align-self": "flex-start"})

    boundedinttext = ipywidgets.BoundedIntText(
        value=default_value, min=minimum, max=maximum, step=step,
        layout={"flex": "1 1 65%", "align-self": "flex-end"})

    return ipywidgets.HBox(
        children=[label, boundedinttext],
        layout={"width": "100%", "flex": "1 1 auto"})

def label_boundedfloattext_pair(label_text, default_value, minimum, maximum, step):
    """A helper to create a HBox with a Label and a BoundedFloatText widgets.

    Args:
        label_text: the text content in the label.
        default_value: the default value in the BoundedFloatText.
        minimum: the minimum value allowed in the BoundedFloatText.
        maximum: the maximum value allowed in the BoundedFloatText.
        step: the size of increment used in the BoundedFloatText.
    """

    label = ipywidgets.Label(
        value=label_text, layout={"flex": "1 1 35%", "align-self": "flex-start"})

    boundedfloattext = ipywidgets.BoundedFloatText(
        value=default_value, min=minimum, max=maximum, step=step,
        layout={"flex": "1 1 65%", "align-self": "flex-end"})

    return ipywidgets.HBox(
        children=[label, boundedfloattext],
        layout={"width": "100%", "flex": "1 1 auto"})

def label_dropdown_pair(label_text, default_value, options):
    """A helper to create a HBox with a Label and a Dropdown widgets.

    Args:
        label_text: the text content in the label.
        default_value: the default value in the Dropdown.
        options: the available options in the Dropdown.
    """

    label = ipywidgets.Label(
        value=label_text, layout={"flex": "1 1 35%", "align-self": "flex-start"})

    dropdown = ipywidgets.Dropdown(
        value=default_value, options=options,
        layout={"flex": "2 1 65%", "align-self": "flex-end"})

    return ipywidgets.HBox(
        children=[label, dropdown], layout=ipywidgets.Layout(width="100%"))

def relative_to_a_file(basefile, path):
    """Convert a rel path to an abs path relative to the folder of the basefile.
    """

    # only do this when the path provided is not an absolute path
    if not os.path.isabs(path):
        path = os.path.abspath(os.path.join(os.path.dirname(basefile), path))

    return path

def get_point_info(workdir, shapefilepath):
    """Get the information of the rupture points from a shapefile.

    Args:
        workdir: prefix of the simulation case directory of the points.
        shapefilepath: the path to the shapefile

    Return:
        A list. Each element in the list represents a point and is represented
        by a Python dict. In each dict, the key "xy" is the coordinates in EPSG
        3857, and the key "casename" is the case folder name.
    """
    import fiona
    import fiona.transform

    shapefile = fiona.open(shapefilepath, 'r')

    # check if the feature is a Point
    if shapefile.schema["geometry"] != "Point":
        raise TypeError("The feature type is not \"Point\".")

    # check if the key "LINE_ID", "ROUTE_ID", and "POINT_ID" exist
    for key in ["LINE_ID", "ROUTE_ID", "POINT_ID"]:
        if key not in shapefile.schema["properties"]:
            raise KeyError("The attribute \"{}\" does not exist.".format(key))

    # initialize return data
    data = []

    # get information and coordinate transformation
    for feature in shapefile:

        xy = list(fiona.transform.transform_geom(
            shapefile.crs, "EPSG:3857", feature["geometry"])["coordinates"])

        casename = "LID{}_RID{}_PID{}".format(
            feature['properties']['LINE_ID'], feature['properties']['ROUTE_ID'],
            feature['properties']['POINT_ID'])

        dirname = os.path.join(workdir, casename)

        data.append({"xy": xy, "casename": casename, "dirname": dirname})

    shapefile.close()

    return data

def obtain_common_yaml_settings(yamldata):
    """Set common settings of all points.

    Args:
        yamldata: the raw data obtained from the project YAML file.

    Return:
        A dict that can be passed to write_setrun function.
    """
    import numpy

    params = {}

    params["extent"] = [
        yamldata["basic settings"]["computational domain"]["top"],
        yamldata["basic settings"]["computational domain"]["bottom"],
        yamldata["basic settings"]["computational domain"]["left"],
        yamldata["basic settings"]["computational domain"]["right"]]

    params["end_time"] = yamldata["basic settings"]["simulation time"]
    params["output_time"] = yamldata["basic settings"]["output time spacing"]

    params["res"] = [
        yamldata["basic settings"]["finest grid resolutions"]["x"],
        yamldata["basic settings"]["finest grid resolutions"]["y"]]

    params["ref_mu"] = yamldata["fluid settings"]["ref dynamic viscosity"]
    params["ref_temp"] = yamldata["fluid settings"]["ref temperature"]
    params["amb_temp"] = yamldata["fluid settings"]["ambient temperature"]
    params["density"] = yamldata["fluid settings"]["density"]

    params["leak_profile"] = numpy.zeros(
        (len(yamldata["basic settings"]["leak profile"]), 2), dtype=numpy.float)

    params["evap_type"] = yamldata["fluid settings"]["evaporation model"]["model"]
    params["evap_coeffs"] = yamldata["fluid settings"]["coefficients"]

    for i, stage in enumerate(yamldata["basic settings"]["leak profile"]):
        params["leak_profile"][i, 0] = stage["end time"]
        params["leak_profile"][i, 1] = stage["rate"]

    if yamldata["basic settings"]["hydrologic files"] == "from NHD server":
        params["n_hydros"] = 1
    else:
        params["n_hydros"] = len(yamldata["basic settings"]["hydrologic files"])

    params["friction_type"] = yamldata["darcy-weisbach settings"]["coefficient model"]
    params["roughness"] = yamldata["darcy-weisbach settings"]["surface roughness"]

    params["dt_init"] = yamldata["advanced numerical parameters"]["initial dt"]
    params["dt_max"] = yamldata["advanced numerical parameters"]["max dt"]
    params["cfl_desired"] = yamldata["advanced numerical parameters"]["desired cfl"]
    params["cfl_max"] = yamldata["advanced numerical parameters"]["max cfl"]
    params["amr_max"] = yamldata["advanced numerical parameters"]["total AMR levels"]
    params["refinement_ratio"] = yamldata["advanced numerical parameters"]["AMR refinement ratio"]

    return params

def crop_raster(outputfile, raster, xy, extent, recreate):
    """Crop a raster file.

    Args:
        outputfile: the path to output topography file.
        raster: data returned by rasterio.open.
        xy: a list of the xy coorfinates ([x, y]).
        extent: the relative extent to the xy location.
        recreate: whether to recreate the file if it already exists.
    """
    import rasterio.mask

    # if the file already exists
    if os.path.isfile(outputfile) and not recreate:
        return

    # calculate the absolute extent
    top = xy[1] + extent[0] + 10
    bottom = xy[1] - extent[1] - 10
    left = xy[0] - extent[2] - 10
    right = xy[0] + extent[3] + 10

    # the cutting window
    geometry = {
        "type": "Polygon",
        "coordinates": [[
            (left, bottom), (right, bottom), (right, top), (left, top),
            (left, bottom)]]}

    # crop the input raster and return the new topo
    out_raster, out_transform = \
        rasterio.mask.mask(raster, [geometry], crop=True)

    # get the meta data of the new topo
    out_meta = raster.meta.copy()

    out_meta.update({"driver": "AAIGrid",
                     "height": out_raster.shape[1],
                     "width": out_raster.shape[2],
                     "transform": out_transform})

    # a workaround to the ERROR 4 message
    rasterio.open(
        outputfile, "w", driver="GTiff", width=1, height=1, count=1,
        crs=rasterio.crs.CRS.from_epsg(3857), transform=out_transform,
        dtype=rasterio.float32, nodata=-9999.).close()

    # write the new topo to the outputfile
    with rasterio.open(outputfile, "w", **out_meta) as dest:
        dest.write(out_raster)

def check_helpers_path():
    """Ensure the module helpers can be found the sys path.
    """

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if root in sys.path:
        sys.path.remove(root)

    sys.path.insert(0, root)

def prepare_geoclaw_cases(yamlpath, recreate):
    """Parse a project YAML file.

    Args:
        yamlpath: a string of the path to the YAML file.
        recreate: whether to delete and re-create a case folder if it exists.
    """
    import shutil
    import yaml
    import rasterio

    # import helper module using relative path to this file
    check_helpers_path()
    import helpers.arcgistools

    # read project YAML file
    with open(yamlpath, 'r') as f:
        raw_data = yaml.load(f, Loader=yaml.SafeLoader)

    # working directory
    raw_data["basic settings"]["working directory"] = relative_to_a_file(
        yamlpath, raw_data["basic settings"]["working directory"]),

    # obtain the xy coordinates and other point information from the shapefile
    pointdata = get_point_info(
        raw_data["basic settings"]["working directory"],
        relative_to_a_file(yamlpath, raw_data["basic settings"]["rupture points"]))

    # obtain common settings
    params = obtain_common_yaml_settings(raw_data)

    # open the local topography if it exists
    if raw_data["basic settings"]["topography file"] != "from 3DEP server":
        toporaster = rasterio.open(relative_to_a_file(
            yamlpath, raw_data["basic settings"]["topography file"]), 'r')

    # hydrological data
    if raw_data["basic settings"]["hydrologic files"] != "from NHD server":
        hydrorasters = []
        for raster in raw_data["basic settings"]["hydrologic files"]:
            hydrorasters.append(
                rasterio.open(relative_to_a_file(yamlpath, raster), 'r'))

    # loop through each point and create its case folder and setrun.py
    for point in pointdata:

        # setup the case folder path and create the folder
        params["out_dir"] = point["dirname"]

        if os.path.isdir(params["out_dir"]) and recreate:
            shutil.rmtree(params["out_dir"])

        os.makedirs(params["out_dir"], exist_ok=True)

        # copy the coordinates
        params["point"] = point["xy"]

        # create topography file if not downloading from 3DEP
        if raw_data["basic settings"]["topography file"] != "from 3DEP server":
            crop_raster(
                os.path.join(params["out_dir"], "topo.asc"),
                toporaster, point["xy"], params["extent"], recreate)

        # create topography file if not downloading from 3DEP
        if raw_data["basic settings"]["hydrologic files"] != "from NHD server":
            for i, raster in enumerate(hydrorasters):
                crop_raster(
                    os.path.join(params["out_dir"], "hydro_{}.asc".format(i)),
                    raster, point["xy"], params["extent"], recreate)

        # create setrun.py in the case folder
        helpers.arcgistools.write_setrun(**params)

    # close topography raster
    if raw_data["basic settings"]["topography file"] != "from 3DEP server":
        toporaster.close()

    # close hydrological rasters
    if raw_data["basic settings"]["hydrologic files"] != "from NHD server":
        for raster in hydrorasters:
            raster.close()

    return raw_data, pointdata

def create_and_submit(yamldata, points, userparams):
    """Create Azure resources and submit simulation cases.
    """

    # import helper module using relative path to this file
    check_helpers_path()
    import helpers.azuretools

    # create an UserCredential instance
    if userparams["cred_type"] == "Encrypted file":
        uc = helpers.azuretools.UserCredential()
        uc.read_encrypted(
            userparams["cred"]["file"]["passcode"],
            userparams["cred"]["file"]["filepath"])
    elif userparams["cred_type"] == "Manual input":
        uc = helpers.azuretools.UserCredential(
            userparams["cred"]["manual"]["batch_name"],
            userparams["cred"]["manual"]["batch_key"],
            userparams["cred"]["manual"]["batch_url"],
            userparams["cred"]["manual"]["storage_name"],
            userparams["cred"]["manual"]["storage_key"])
    else:
        raise ValueError

    # create a Mission instance
    mission = helpers.azuretools.Mission()

    backup = os.path.join(
        yamldata["basic settings"]["working directory"],
        "landspill-azure_backup_file.dat")

    if os.path.isfile(backup):
        mission.init_info_from_file(backup)
    else:
        mission.init_info(
            "landspill-azure", userparams["max_nodes"], userparams["working_dir"],
            userparams["vm_type"], node_type="dedicated")

    mission.setup_communication(cred=uc)
    mission.create_resources()

    # loop through each point to add case to Azure task scheduler
    for point in points:

        if not os.path.isdir(point["dirname"]):
            if userparams["ignore_local_nonexist"]:
                continue
            else:
                raise FileNotFoundError(
                    "Can not find case folder {}".format(userparams["dirname"]))

        mission.add_task(
            point["casename"], point["dirname"], userparams["ignore_azure_exist"])

    # write a backup file to local machine
    mission.write_info_to_file()

def table_input(row_title, col_titles, col_types, col_params=None):
    """A table input."""

    if col_params is None:
        col_params = [{}] * len(col_titles)

    children = []

    # selector for the number of rows
    children.append(ipywidgets.HBox([
        ipywidgets.Label(value=row_title, layout={"flex": "1 1 50%"}),
        ipywidgets.BoundedIntText(value=1, min=1, layout={"flex": "1 1 50%"})]))

    # column title row
    temp = [[], []]
    for i, title in enumerate(col_titles):
        temp[0].append(ipywidgets.Label(value=title, layout={"flex": "1 1 1%"}))
        temp[1].append(col_types[i](**col_params[i]))


    children.append(ipywidgets.VBox([
        ipywidgets.HBox(temp[0], layout={"flex": "1 1 auto"}),
        ipywidgets.HBox(temp[1], layout={"flex": "1 1 auto"})]))

    children[-1].layout.border = "0.5px solid gray"
    children[-1].layout.padding = "1px 1px 1px 1px"

    # register callback
    children[0].children[1].observe(functools.partial(
        table_row_change, table_box=children[1]), names="value")

    return ipywidgets.VBox(children, layout={"flex": "1 1 auto"})

def table_row_change(change, table_box):
    """Change the number of rows in a table."""

    assert change["old"] == (len(table_box.children) - 1), \
        "{} vs {}".format(change["old"], len(table_box.children))

    # children of a box is a tuple, so copy it to a list
    # don't forget the first row is the title row, must copy it
    temp = []
    for i in range(min(change["new"], change["old"])+1):
        temp.append(table_box.children[i])

    # if increasing the number of rows
    if change["new"] > change["old"]:
        for i in range(change["old"], change["new"]):
            temp.append(copy(temp[-1]))

    table_box.children = temp

def label_table_input_pair(
        label_text, row_title, col_titles, col_types, col_params=None):
    """Label and table input."""


    label = ipywidgets.Label(
        value=label_text, layout={"flex": "1 1 35%", "align-self": "flex-start"})

    table = table_input(row_title, col_titles, col_types, col_params)

    return ipywidgets.HBox(
        children=[label, table], layout=ipywidgets.Layout(width="100%"))

def copy(widget):
    """Copy a widget or a Box-derived instance."""

    assert isinstance(widget, ipywidgets.Widget)

    if isinstance(widget, ipywidgets.Box):
        new = copy_box(widget)
    else:
        new = copy_widget(widget)

    return new

def copy_widget(widget):
    """Copy a widget with the same layout and attributes."""

    # make sure only basic widgets are passed into here
    assert not isinstance(widget, ipywidgets.Box)

    # a new instance with the same class tyle
    new = widget.__class__()

    # a list of properties that won't be copied
    dont_copy = ["layout", "style"]
    if not isinstance(widget, ipywidgets.Label):
        dont_copy += ["value"]

    for key, value in widget.get_state().items():
        if key not in dont_copy:
            setattr(new, key, value)

    # layout requires special handling
    new.layout = widget.layout

    # style requires special handling and some widgets don't have style
    try:
        new.style = widget.style
    except AttributeError:
        pass

    return new

def copy_box(widget):
    """Copy a Box-derived container widget."""

    # make sure the input is a Box derived instance
    assert isinstance(widget, ipywidgets.Box)

    # a new instance
    new = widget.__class__()

    # a list of properties that won't be copied
    dont_copy = ["layout", "children"]

    # copy properties
    for key, value in widget.get_state().items():
        if key not in dont_copy:
            setattr(new, key, value)

    # layout requires special handling
    new.layout = widget.layout

    # copy children
    temp = []
    for w in widget.children:
        temp.append(copy(w))

    new.children = temp

    return new
