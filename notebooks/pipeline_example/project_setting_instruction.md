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
------------------------------

The parameters in `project metadata` node are not used in simulations. They are
just for users to manage projects.

1. **name**: a string

    The name of the project.

2. **timestamp**: a YAML acceptable timestamp string format.

    The timestamp of when this YAML file was created/modified.

## 2. `basic settings` node
------------------------------

1. **working directory**: a string

    Path to the working directory where all simulation cases will be located
    in.

2. **rupture points**: a string

    Path to a Esri shapefile which has the information of the ruptured points.

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
    running simulations.

7. **hydrologic files**: "from NHD server" or a list of strings

    If using "from NHD server", the solver will download hydrological data
    from NHD feature servers. Users can also provide a list of strings to
    indicate the paths to hydrological files that will be used by the solver.
    Note for hydrological data, the files should be raster files in Esri ASCII
    format, not the shapefile format. Also, the solver accepts multiple
    hydrological files, so users must use a list, rather than a single string.

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
