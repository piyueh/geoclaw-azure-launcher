# Instruction of project YAML file parameters
---------------------------------------------

For the script-based workflow, a YAML file is required for setting up a project.
This document provides the instruction for the parameters in this YAML file.
To see an example of the project YAML file, check the **project.yaml** in the
folder.

There are five first-level node in the YAML file:

1. `project metadata`
2. `basic settings`
3. `fluid settings`
4. `darcy-weisbach settings`
5. `misc`
6. `advanced numerical parameters`

We use [PyYAML](https://pyyaml.org/) to parse the YAML file, so Python-style
lists and dictionaries can be used to replace some of the sub-nodes in the YAML.

## 1. `project metedata` node
-----------------------------

The parameters in `project metadata` node are not used in simulations. They are
just for users to manage projects.

1. **name**: a string

    The name of the project.

2. **timestamp**: a YAML acceptable timestamp string format.

    The timestamp of when this YAML file was created/modified.

## 2. `basic settings` node
---------------------------

1. **working directory**: a string

    Path to the working directory where all simulation cases will be located
    in. If a relative path is provided, then it will be relative to the folder
    that has the YAML file.

2. **rupture points**: a string

    Path to a Esri shapefile which has the information of the ruptured points.
    If a relative path is provided, then it will be relative to the folder that
    has the YAML file.

3. **leak profile**: a list of dictionaries / a YAML sub-node

    The information of each stage in the leak profile. The unit of time is
    in seconds, and the unit of leak rate is in cubmic meters per second.
    For example, if a leak profile is (r is the leak rate, and t is time):

    * r = 0.5 m^3/s, when 0s &lt; t &le; 60s
    * r = 0.1 m^3/s, when 60s &lt; t &le; 120s
    * r = 0.05 m^3/s, when 120s &lt; t &le; 180s
    * r = 0 m^3/s, afterward

    Then in Python list/dictionary style, it is
    `leak profile: [{end time: 60, rate: 0.1}, ..., ]`. And if using YAML style,
    it is:

    ```
    leak profile:
      - end time: 60
        rate: 0.5
      - end time: 120
        rate: 0.1
      - end time: 180
        rate: 0.05
    ```

4. **simulation time**: an integer

    The simulation end time. The unit is hour. For example, to simulation the
    flow 8 hours after the rupture event, then set this parameters to 8.

5. **output time spacing**: an integer

    How long it is between two consecutive outputs of the results. The unit is
    in minute. For example, if setting this parameter to 2 and the simulation
    time is 1 hour, then it means we will have the flow patterns at T = 2 min,
    4 min, 6 min, ..., 60 min after the pipeline ruptured.

6. **topography file**: a string

    Either "from 3DEP server" or a path to a topography file. "from 3DEP
    server" means the solver will try to download topography from 3DEP map
    server at runtime, so users don't have to prepare the topography before
    running simulations. The file format is Esri ASCII raster. If a relative 
    path is provided, then it will be relative to the folder that has the YAML 
    file.

7. **hydrologic files**: "from NHD server" or a list of strings

    If using "from NHD server", the solver will download hydrological data
    from NHD feature servers. Users can also provide a list of strings to
    indicate the paths to hydrological files that will be used by the solver.
    Note for hydrological data, the files should be raster files in Esri ASCII
    format, not the shapefile format. Also, the solver accepts multiple
    hydrological files, so users must use a list, rather than a single string.
    If a relative path is provided, then it will be relative to the folder that 
    has the YAML file.


8. **use topo res as grid res**: a boolean

    Whether to use the the raster file's resolution as the finest grid
    resolution for the AMR grid during flow simulations. This option only
    works when users provide their own topography file, i.e., not using
    the "from 3DEP server" option.

9. **finest grid resolutions**: a Python dictionary / a YAML sub-node

    The finest AMR grid resolution for the flow solver. Use either a Python
    dictionary or a YAML sub-node with keys `x` and `y` to indicate the
    resolution. The unit is meter. For example, if the finest grid resolution in
    both x and y direction is 1 meter, use:

    ```
    finest grid resolution: {x: 1, y: 1}
    ```

    or

    ```
    finest grid resolution:
      x: 1
      y: 1
    ```

10. **computational domain**: a Python dictionary or a YAML sub-node

    The distance between a rupture point to the four boundaries of the
    computational domain. Use `top` (north), `bottom` (south), `left` (west),
    and `right` (east) to indicate the boundaries. The unit is meter. For
    example, if all four boundaries are 1000 meters away from the rupture
    point of a simulation, then in YAML sub-node format:

    ```
    computational domain:
      top: 1000
      bottom: 1000
      left: 1000
      right: 1000
    ```

    or in Python dictionary format:

    ```
    computational domain: {top: 1000, bottom: 1000, left: 1000, right: 1000}
    ```

## 3. `fluid settings` node
---------------------------

1. **ref dynamic viscosity**: a floating point number

    The dynamic viscosity at a reference temperature of the working fluid. The
    unit is cP.

2. **ref temperature**: a floating point number

    The reference temperature which the `ref dynamic viscosity` is at. The unit
    is Celsius.

3. **ambient temperature**: a floating point number

    The ambient temperature which the working fluid is at in simulations. The
    unit is Celsius.

4. **density**: a floating point number

    The density of the working fluid. The unit is kilograms per cubic meter.

5. **evaporation model**: a Python dictionary or a YAML sub-node

    The evaporation model used in simulations. Use the key `model` to specify
    the model, and use `coefficients` to provide model coefficients.
    `coefficients` is a Python list or a YAML sub-node. Currently, there are
    three options for the key `model`: "None", "Fingas1996 Log Law", and
    "Fingas1996 SQRT Law". For "None", there's no need to provide coefficients.
    An example is using the log law for Maya Crude:

    ```
    evaporation model:
      model: Fingas1996 Log Law
      coefficients:
        - 1.38
        - 0.045
    ```

    or

    ```
    evaporation model: {model: Fingas1996 Log Law, coefficients: [1.38, 0.045]}
    ```

## 4. `darcy-weisbach settings` node
------------------------------------

1. **coefficient model**: a string

    The model used to calculate the Darcy-Weisbach coefficient. We have several
    models in GeoClaw, but in this front-end, we only accepts "None" and 
    "Three-regime model".

2. **surface roughness**: a floating point number

    The absolute surface roughness, required by Darcy-Weisbach coefficient
    models. The unit is meter.

## 5. `misc` node
-----------------

1. **skip if case exist**: a boolean

    Indicate if we should re-create a new simulation case and overwrite the old
    one if we find the case already exists in the working dorectory.

## 5. `advanced numerical parameters` node
------------------------------------------

1. **initial dt**: a floating point number

    The value of the initial time-step size. Time steps in the solver change
    adaptively based on flow conditions. But we still need to specify the size
    of the first time step. The unit is second.

2. **max dt**: a floating point number

    The maximum allowed time-step size. The unit is second. Time steps in the 
    solver change adaptively based on flow conditions. We can specify a maximum
    allowed step size to limit it.

3. **desired cfl**: a floating point number

    The CFL number that is desired during a simulation. The solver will change
    the time-step size to match this CFL if the current CFL is much greater. If
    the current CFL is just slightly larger than this value, time-step size
    may not be changed in this step.

4. **max cfl**: a floating point number

    The maximum allowed CFL number. If the current CFL is greater than this
    value, the solver will definitely change the time-step size to match the
    desired CFL.

5. **total AMR levels**: an integer

    The number of AMR grid levels. The default is 2, which may be good enough 
    for pipeline overland analysis.

6. **AMR refinement ratio**: an integer

    The ratio between a coarse grid and its child grids.
