# Land Grab 2

## Installation

### Prerequisities

This project uses [Git LFS](https://git-lfs.com/) to store `.zip`, `.dbf`, and `.shp` files remotely on GitHub rather than directly in the repository source. In order to access these files and build the datasets locally, you'll need to do the following:

1. **Install Git LFS.** Follow [the installation instructions](https://github.com/git-lfs/git-lfs#installing) for your operating system.
2. At the terminal, run the following two commands (without typing the dollar sign):

```sh
$ git lfs install
$ git lfs pull
```

Together, these commands will install the Git LFS configuration, fetch LFS changes from the remote, and replace pointer files locally with the actual data.

### Dependencies

After completing the above, install Python dependencies. At the terminal, run the following command (again, omit the dollar sign):

```sh
$ pip install -e .
```

This only needs to be done the first time you run the script.

## Building the datasets

All functionality is orchestrated by a single top-level command `run.py`. To see a listing of all available command options, run the following command:

```
$ DATA=data python run.py --help
```

`run.py` expects a particular directory structure for the datasets, which is already enforced by this repository's directory structure. As such, you should not move any files from their current locations.

### State Trust Lands (STL) Dataset

The STL dataset is built in stages, with the output of each stage becoming the input of the next stage.
The following assumes your data directory is itself called `data` and all paths will refer to it as such.

#### Stage 1

To execute Stage 1, run the following command at the terminal:

```sh
$ DATA=data python run.py stl-stage-1
```

This command:

- Gathers the raw data from both remote state-run servers and the input data directory.
- Collects all fields-of-interest from the raw data and normalizes the naming across datasets.
- Unifies all individual states' data into one large dataset.

Individual state datasets are written to `data/stl_dataset/step_1/output/merged/<state-abbreviation>.[csv,geojson]`. The unified dataset is written to `data/stl_dataset/step_1/output/merged/all-states.[csv,geojson]`.

#### Stage 2

To execute Stage 2, run the following command at the terminal:

```sh
$ DATA=data PYTHONHASHSEED=42 python run.py stl-stage-2
```

This command matches activity information to the parcels from the unified multi-state dataset output in Stage 1 (`data/stl_dataset/step_1/output/merged/all-states.[csv,geojson]`). The `data` directory for Stage 2 already includes state-specific information about the activities occuring on all parcels.

The output of this stage is written to `data/stl_dataset/step_2/output/stl_dataset_extra_activities.[csv, geojson]`

#### Stage 2.5 (Manual)

Stage 2.5 involves manually enriching the unified dataset from Stage 2 (`data/stl_dataset/step_2/output/stl_dataset_extra_activities.[csv, geojson]`) with land-cession information for each parcel. The new dataset should be named `stl_dataset_extra_activities_plus_cessions.csv` and located at `data/stl_dataset/step_2_5/output/` (though, as evidenced by the Stage 3 input details, the title is not important to the code).

**IMPORTANT 💡** Ensure there is only one CSV file in this directory.

#### Stage 3

To execute Stage 3, run the following command at the terminal:

```sh
DATA=data python run.py stl-stage-3
```

This command will take the first CSV found in `data/stl_dataset/step_2_5/output/` and augment it with the prices paid for each parcel of land. The `data` directory for Stage 3 already contains a listing a CSV with the listing of prices paid for land (`data/stl_dataset/step_3/input/Cession_Data.csv`).

The output of this stage is written to `data/stl_dataset/step_3/output/stl_dataset_extra_activities_plus_cessions_plus_prices.[csv, geojson]`
    
#### Stage 4

To execute Stage 4, run the following command at the terminal:

```sh
$ DATA=data python run.py stl-stage-4
```

This command will calculate summaries connecting universities and cessions to tribes using the output of Stage 3 (`data/stl_dataset/step_3/output/stl_dataset_extra_activities_plus_cessions_plus_prices.[csv, geojson]`).

The outputs of this stage are three files, written to:
- `data/stl_dataset/step_4/output/university-summary.csv`
- `data/stl_dataset/step_4/output/tribe-summary.csv`
- `data/stl_dataset/step_4/output/tribe-summary-condensed.csv`

### Private Holdings Dataset

- `$ DATA=data python run.py --help`
- `$ DATA=data python run.py --help`
