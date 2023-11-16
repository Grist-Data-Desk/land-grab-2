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
    * output will be `data/stl_dataset/step_1/output/national_stls.[csv, geojson]`
* Stage 2
    * input will be `data/stl_dataset/step_1/output/national_stls.[csv, geojson]`
    * the data directory contains state-specific information about the activities that occur on all land-parcels.
    * Match this activity information to the exact parcels in our unified multi-state dataset.
    * `$ DATA=data PYTHONHASHSEED=42 python run.py stl-stage-2`
    * output will be `data/stl_dataset/step_2/output/stl_dataset_extra_activities.[csv, geojson]`
* Stage 2.5 -- A manual step
    * input will be `data/stl_dataset/step_2/output/stl_dataset_extra_activities.[csv, geojson]`
    * enrich the unified dataset with land-cession information per-parcel.
    * once completed move the updated dataset to `data/stl_dataset/step_2_5/output`
      * title should be `stl_dataset_extra_activities_plus_cessions.csv`
      * though, as evidenced by the Stage 3 input details, the title is not important to the code.
      * IMPORTANT: ensure there is only one csv in this directory
* Stage 3
    * input will be the first csv found in `data/stl_dataset/step_2_5/output/`
    * the data directory contains a listing of prices paid for land. this will be used to calculate ...TBD
    * `$ DATA=data python run.py stl-stage-3`
    * output will be `data/stl_dataset/step_3/output/stl_dataset_extra_activities_plus_cessions_plus_prices.[csv, geojson]`
* Stage 4
    * input will be `data/stl_dataset/step_3/output/stl_dataset_extra_activities_plus_cessions_plus_prices.[csv, geojson]`
    * calculate summaries correlating universities and cessions to tribes
    * `$ DATA=data python run.py stl-stage-4`
    * output will be 
      * `data/stl_dataset/step_4/output/university-summary.csv`
      * `data/stl_dataset/step_4/output/tribe-summary-condensed.csv`

### Private Holdings Dataset

* `$ DATA=data python run.py --help`
* `$ DATA=data python run.py --help`
* 