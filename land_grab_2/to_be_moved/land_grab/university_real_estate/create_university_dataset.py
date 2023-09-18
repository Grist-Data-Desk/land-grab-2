import typer

from tasks.to_be_moved.land_grab.common import (state_specific_directory,
                                                extract_and_clean_single_source_helper,
                                                merge_single_state_helper, merge_all_states_helper)

from tasks.to_be_moved.land_grab.constants import (STATE, UNIVERSITY_DIRECTORY, CLEANED_DIRECTORY,
                                                   MERGED_DIRECTORY, QUERIED_DIRECTORY)

from university_config import UNIVERSITY_CONFIGS

app = typer.Typer()


def _queried_data_directory(state=None):
  return state_specific_directory(UNIVERSITY_DIRECTORY + QUERIED_DIRECTORY,
                                  state)


def _cleaned_data_directory(state=None):
  return state_specific_directory(UNIVERSITY_DIRECTORY + CLEANED_DIRECTORY,
                                  state)


def _merged_data_directory(state=None):
  return state_specific_directory(UNIVERSITY_DIRECTORY + MERGED_DIRECTORY,
                                  state)


@app.command()
def merge_single_state(state: str):
  cleaned_data_directory = _cleaned_data_directory(state)
  merged_data_directory = _merged_data_directory(state)
  merge_single_state_helper(state, cleaned_data_directory,
                            merged_data_directory)


@app.command()
def merge_all_states():
  # first, find all states for which we have cleaned data
  cleaned_data_directory = _cleaned_data_directory()
  merged_data_directory = _merged_data_directory()
  merge_all_states_helper(cleaned_data_directory, merged_data_directory)


@app.command()
def extract_and_clean_all():
  for source in UNIVERSITY_CONFIGS.keys():
    extract_and_clean_single_source(source)


@app.command()
def extract_and_clean_single_source(source: str):
  # get state and correct config
  config = UNIVERSITY_CONFIGS[source]
  state = config[STATE]
  queried_data_directory = _queried_data_directory(state)
  cleaned_data_directory = _cleaned_data_directory(state)
  extract_and_clean_single_source_helper(source, config, queried_data_directory,
                                         cleaned_data_directory)


if __name__ == "__main__":
  app()
