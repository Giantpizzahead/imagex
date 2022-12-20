"""
ImageX - Regex for basic_shapes
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""

from pathlib import Path
import sys

TEST_PATH = Path(__file__).parent.joinpath("tests").resolve()
RES_PATH = Path(__file__).parent.joinpath("res").resolve()

# Add root directory to path (for importing imagex)
sys.path.insert(0, str(TEST_PATH.parent.parent))

import imagex
