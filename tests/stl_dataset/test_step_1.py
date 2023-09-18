import os

os.environ['DATA'] = '/Users/marcellebonterre/Projects/land-grab-2/data'

from pathlib import Path

from land_grab_2.stl_dataset.step_1.build_dataset import _cessions_data_directory
from land_grab_2.stl_dataset.step_1.constants import STATE_TRUST_DATA_SOURCE_DIRECTORY


def test_all_important_dirs_exist():
    stl_data = Path(STATE_TRUST_DATA_SOURCE_DIRECTORY)
    cession_data = Path(_cessions_data_directory())
    assert stl_data.exists()
    assert cession_data.exists()
