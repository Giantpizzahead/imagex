"""
ImageX - Regex for basic_shapes
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import json
from pathlib import Path
from typing import Optional

import numpy as np

TEST_PATH = Path(__file__).parent.parent.joinpath("tests").resolve()


def gen_test_data(image_path: str, template_path: str, expected: Optional[tuple]):
    """Generate test data"""
    return {
        "image": image_path,
        "template": template_path,
        "expected": expected,
    }


def create_test(test_group: str, test_name: str, test_data: dict):
    """Create a test from a test group and test name"""
    # Get test group path
    test_group_path = TEST_PATH.joinpath(test_group)
    test_group_path.mkdir(parents=True, exist_ok=True)
    # Create test data file
    with open(test_group_path.joinpath(f"{test_name}.json"), "w") as file:
        json.dump(test_data, file, indent=4)
    print(f"Created test {test_name} in group {test_group} with data:\n{test_data}")


def naive_find(image: np.ndarray, template: np.ndarray):
    """
    Naive version of find. Returns None or (x, y, w, h).

    Borders are the last matching pixel of the template.
    """
    # For each possible location of template, check if it matches image
    for y in range(image.shape[0] - template.shape[0] + 1):
        for x in range(image.shape[1] - template.shape[1] + 1):
            # Check if template matches image
            if np.array_equal(image[y:y+template.shape[0], x:x+template.shape[1]], template):
                return x, y, template.shape[1], template.shape[0]
    return None
