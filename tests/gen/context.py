"""
ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import random
from pathlib import Path
import sys

import numpy as np

# Path constants
ROOT_PATH = Path(__file__).parent.parent.parent.resolve()
TEMP_PATH = ROOT_PATH / "temp"
TEST_PATH = ROOT_PATH / "tests"
TEST_DATA_PATH = TEST_PATH / "tests"
RES_PATH = TEST_PATH / "res"
NONE = (0, 0, 0, 0)


def seed_gens(label: str) -> None:
    """Seeds all random number generators, given a string."""
    random.seed(abs(hash(label + "?") % (2 ** 32 - 1)))
    np.random.seed(abs(hash(label + "!") % (2 ** 32 - 1)))