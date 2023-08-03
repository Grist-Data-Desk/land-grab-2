import typer

from common import (state_specific_directory,
                    extract_and_clean_single_source_helper,
                    merge_single_state_helper, merge_all_states_helper,
                    delete_files_and_subdirectories_in_directory)

from constants import (STATE, STATE_TRUST_DIRECTORY, CLEANED_DIRECTORY,
                       MERGED_DIRECTORY, QUERIED_DIRECTORY)

from state_trust_config import STATE_TRUST_CONFIGS

app = typer.Typer()


def _queried_data_directory(state=None):
  return state_specific_directory(STATE_TRUST_DIRECTORY + QUERIED_DIRECTORY,
                                  state)


def _cleaned_data_directory(state=None):
  return state_specific_directory(STATE_TRUST_DIRECTORY + CLEANED_DIRECTORY,
                                  state)


def _merged_data_directory(state=None):
  return state_specific_directory(STATE_TRUST_DIRECTORY + MERGED_DIRECTORY,
                                  state)


@app.command()
def merge_single_state(state: str):
  '''
  Merge all data for a single state
  '''
  cleaned_data_directory = _cleaned_data_directory(state)
  merged_data_directory = _merged_data_directory(state)
  merge_single_state_helper(state, cleaned_data_directory,
                            merged_data_directory)


@app.command()
def merge_all_states():
  '''
  Merge all data for the entire dataset
  '''
  # first, find all states for which we have cleaned data
  cleaned_data_directory = _cleaned_data_directory()
  merged_data_directory = _merged_data_directory()
  merge_all_states_helper(cleaned_data_directory, merged_data_directory)


@app.command()
def extract_and_clean_all():
  '''
  Extract and clean data for the entire dataset
  '''
  for source in STATE_TRUST_CONFIGS.keys():
    extract_and_clean_single_source(source)


@app.command()
def extract_and_clean_single_source(source: str):
  '''
  Extract and clean data from a single data source
  '''
  # get state and correct config
  config = STATE_TRUST_CONFIGS[source]
  state = config[STATE]
  queried_data_directory = _queried_data_directory(state)
  cleaned_data_directory = _cleaned_data_directory(state)
  extract_and_clean_single_source_helper(source, config, queried_data_directory,
                                         cleaned_data_directory)


@app.command()
def build_full_dataset():
  '''
  Delete all old data files and build the entire dataset from scratch
  '''
  # first delete all previous data
  delete_files_and_subdirectories_in_directory(_queried_data_directory())
  delete_files_and_subdirectories_in_directory(_cleaned_data_directory())
  delete_files_and_subdirectories_in_directory(_merged_data_directory())

  # extract, clean, and merge all data
  extract_and_clean_all()
  merge_all_states()


if __name__ == "__main__":
  app()