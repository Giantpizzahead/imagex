"""
ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
from pathlib import Path
import sys

# Path constants
ROOT_PATH = Path(__file__).parent.parent.resolve()
TEMP_PATH = ROOT_PATH / "temp"
TEST_PATH = ROOT_PATH / "tests"
TEST_DATA_PATH = TEST_PATH / "tests"
RES_PATH = TEST_PATH / "res"

# Add root directory to path (for importing imagex)
sys.path.insert(0, str(ROOT_PATH))

import imagex
