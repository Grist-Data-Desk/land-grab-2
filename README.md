# Land Grab University

## Steps to build the dataset

First, install python. We recommend using the [mamba](https://mamba.readthedocs.io/en/latest/index.html#) or [conda](https://docs.conda.io/en/latest/) package managers.

Next, [clone the github repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your computer.

Open up a terminal and create a conda environment with the required packages

```
conda env create -f environment.yml
```
Finally, in ther terminal, from the project's root directory, run the following python command
```
python create_state_trust_dataset.py build-full-dataset
```
