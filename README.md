# Land Grab 2

## Installation

* At a Terminal type the following (don't type the dollar sign)
    * `$ pip install -e .` N.B. This needs to be done only the first time running the script
    * Acquire the input data zip. Its contents are organized in a specific way, which all commands are expecting.

## Building the datasets

All functionality is orchestrated by a single top-level command `run.py`.
To see a listing of all available command options, execute the following:

* `$ DATA=data python run.py --help`

### State Trust Lands (STL) Dataset

The STL dataset is built in stages, with the output of each stage becoming the input of the next stage.
The following assumes your data directory is itself called `data` and all paths will refer to it as such.

* Stage 1
    * gathers the raw data from both remote state-run servers, and from the input data directory.
    * collect all fields-of-interest from the raw data, and normalize the naming across datasets.
    * unify all individual states' data into one large dataset.
    * `$ DATA=data python run.py stl-stage-1`
    * output will be `data/stl_dataset/step_1/input/national_stls.[csv, geojson]`
* Stage 2
    * the data directory contains state-specific information about the activities that occur on all land-parcels.
    * Match this activity information to the exact parcels in our unified multi-state dataset.
    * `$ DATA=data PYTHONHASHSEED=42 python run.py stl-stage-2`
    * output will be `data/stl_dataset/step_2/output/updated_grist_stl.[csv, geojson]`
* Stage 2.5 -- A manual step
    * the input for this step is `data/stl_dataset/step_2/output/updated_grist_stl.[csv, geojson]`
    * enrich the unified dataset with land-cession information per-parcel.
    * once completed move the updated dataset to `data/stl_dataset/step_1/input/national_stls.csv`
* Stage 3
    * the data directory contains a listing of prices paid for land. this will be used to calculate ...TBD
    * `$ DATA=data python run.py stl-stage-3`
    * output will be `data/stl_dataset/step_3/output/updated_grist_stl.[csv, geojson]`
* Stage 4
    * calculate summaries correlating universities and cessions to tribes
    * `$ DATA=data python run.py stl-stage-4`
    * output will be `data/stl_dataset/step_1/input/state_trust/summary_statistics`

### Private Holdings Dataset

* `$ DATA=data python run.py --help`
* `$ DATA=data python run.py --help`
* 