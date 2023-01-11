"""
ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import json

import pytest

from conftest import *


# Boundaries for a test to be considered correct
MAX_SIZE_ERROR_RATIO = 0.125
MAX_SIZE_ERROR_FLAT = 15
MAX_POS_ERROR_RATIO = 0.125
MAX_POS_ERROR_FLAT = 15

# Special None constant
NONE = [0, 0, 0, 0]


# Get list of all test groups
test_groups = [path.name for idx, path in enumerate(TEST_DATA_PATH.iterdir()) if path.is_dir()]
# Sort directories
test_groups.sort()
# Parameterize tests
test_groups = [pytest.param(name, marks=[pytest.mark.xfail] if idx >= 1 else [])
               for idx, name in enumerate(test_groups)]
# test_groups = test_groups[:1]


def run_test(test_path: Path, test_name: str):
    """Run a test, returning a debug string if it fails"""
    # print(f"Running test {test_name}...")
    # Get test data
    with test_path.open("r") as file:
        test_data = json.load(file)
    # Run test
    image_path = str(RES_PATH / test_data["image"])
    template_path = str(RES_PATH / test_data["template"])
    image = imagex.Image(image_path)
    template = imagex.Image(template_path)
    result = imagex.find(image, template)
    answers = test_data["bounding_boxes"]

    failed = False
    if result is None:
        if NONE not in answers:
            failed = "False negative"
    elif len(answers) == 1 and answers[0] == NONE:
        failed = "False positive"
    else:
        # Check if any of the expected matches is returned
        for box in answers:
            if box == NONE:
                continue
            failed = False
            # Check if width and height are similar enough
            w_error_flat = abs(result.w - box[2])
            w_error_ratio = w_error_flat / box[2]
            h_error_flat = abs(result.h - box[3])
            h_error_ratio = h_error_flat / box[3]
            if w_error_flat > MAX_SIZE_ERROR_FLAT and w_error_ratio > MAX_SIZE_ERROR_RATIO:
                failed = "Incorrect width"
            elif h_error_flat > MAX_SIZE_ERROR_FLAT and h_error_ratio > MAX_SIZE_ERROR_RATIO:
                failed = "Incorrect height"

            # Check if center x and y are similar enough
            cx = result.x + result.w / 2
            cy = result.y + result.h / 2
            expected_cx = box[0] + box[2] / 2
            expected_cy = box[1] + box[3] / 2
            x_error_flat = abs(cx - expected_cx)
            x_error_ratio = x_error_flat / box[2]
            y_error_flat = abs(cy - expected_cy)
            y_error_ratio = y_error_flat / box[3]
            if x_error_flat > MAX_POS_ERROR_FLAT and x_error_ratio > MAX_POS_ERROR_RATIO:
                failed = "Incorrect x"
            elif y_error_flat > MAX_POS_ERROR_FLAT and y_error_ratio > MAX_POS_ERROR_RATIO:
                failed = "Incorrect y"
            if not failed:
                break

    # Result should be close enough to expected
    if failed:
        output = f"{test_name} [{failed}]\n"
        output += f"Group: {test_path.parent.relative_to(TEST_DATA_PATH)}\n"
        if len(answers) == 1 and answers[0] == NONE:
            output += "Expected no match"
        else:
            if len(answers) == 1:
                output += f"Expected {answers[0]}"
            else:
                output += f"Expected one of {answers[:3]}"
                if len(answers) > 5:
                    output += f"... ({len(answers)-5} more)"
                if NONE in answers:
                    output += " or no match"
        output += f", got {result}"
        return output


@pytest.mark.parametrize("test_group", test_groups)
def test(test_group: Path):
    # print("Testing", test_group)
    # For each test in the test group
    failed = []
    tests = list((TEST_DATA_PATH / test_group).rglob("*.json"))
    for test_path in tests:
        # Run test
        result = run_test(test_path, test_path.name)
        if result:
            failed.append(result)
    if failed:
        output_msg = [  # "\n" + "-" * 20 + "   TESTS FAILED   " + "-" * 20,
                      f"Missed {len(failed)}/{len(tests)} tests in {test_group}, first failure:",
                      failed[0]]
        # Write to standard error
        pytest.fail("\n".join(output_msg))
