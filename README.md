# Land Grab University

## HOWTO build the dataset

* at a Terminal type the following (don't type the dollar sign)
    * `$ pip install -e .` N.B. This needs to be done only the first time running the script
    * `$ DATA=data build-stl-dataset`
* look for output in `data/output`

## OLD INSTRUCTIONS -- NOT USED -- Steps to build the dataset

First, install python. We recommend using the [mamba](https://mamba.readthedocs.io/en/latest/index.html#)
or [conda](https://docs.conda.io/en/latest/) package managers.

Next, [clone the github repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
to your computer.

Open up a terminal and create a conda environment with the required packages

```
conda env create -f environment.yml
```

Finally, in the terminal, from the project's root directory, run the following python command

```
python create_state_trust_dataset.py build-full-dataset
```
