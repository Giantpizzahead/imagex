"""
ImageX - Regex for basic_shapes
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import json

import pytest
from conftest import *

# Get list of all test groups
test_groups = [str(path.name) for path in TEST_PATH.iterdir() if path.is_dir()]


def run_test(test_path: Path, test_name: str):
    """Run a test, returning a debug string if it fails"""
    # print(f"Running test {test_name}...")
    # Get test data
    with test_path.open("r") as file:
        test_data = json.load(file)
    # Run test
    image_path = str(RES_PATH.joinpath(test_data["image"]))
    template_path = str(RES_PATH.joinpath(test_data["template"]))
    image = imagex.Image(image_path)
    template = imagex.Image(template_path)
    result = imagex.find(image, template)
    if result == test_data["expected"]:
        return
    # Test failed
    return "\n".join(
        [f"Test {test_name}:",
         f"Image {test_data['image']}, template {test_data['template']}",
         f"Expected {test_data['expected']}, got {result}"]
    )


@pytest.mark.parametrize("test_group", test_groups)
def test(test_group: Path):
    print("Testing", test_group)
    # For each test in the test group
    failed = []
    tests = list(TEST_PATH.joinpath(test_group).rglob("*.json"))
    for test_path in tests:
        # Run test
        result = run_test(test_path, test_path.name)
        if result:
            failed.append(result)
    if failed:
        output_msg = ["-" * 20 + "   TESTS FAILED   " + "-" * 20,
                      f"Failed {len(failed)} out of {len(tests)} tests in group {test_group}",
                      "Failures (at most 3 shown):",
                      *failed[:3]]
        # Write to standard error
        print("\n".join(output_msg), file=sys.stderr)
        pytest.fail()
