"""
Contains helper functions for test suite generation.

ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import json
from typing import Optional

import imagex_mock
import imagex_manual
from context import *


def clear_dir(output_dir: Path) -> None:
    """Removes all files in the given directory."""
    # Delete files in directory
    for file in output_dir.glob("*"):
        file.unlink()


def regenerate_dir(output_dir: Path, reason: str) -> bool:
    """
    Removes all files in the given directory if the user agrees to.

    Args:
        output_dir: The path to the directory.
        reason: The reason for regenerating the directory.

    Returns:
        True if the directory was cleared, False otherwise.
    """
    # Make directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    # Warn user if directory is not empty
    if len(list(output_dir.glob("*"))) > 0:
        print(f"Warning: {output_dir} is not empty")
        print(f"Reason for regeneration: {reason}")
        result = input("Would you like to regenerate this directory? [y/N] ")
        if result.lower() != "y":
            print("Skipping...")
            return False
        print("Clearing...")
        clear_dir(output_dir)
    return True


def gen_test_data(image_path: Path, template_path: Path, manual_labels: bool = False,
                  test_dir: Optional[Path] = None) -> dict:
    """
    Generate test data dictionary for a "find-one" test.

    Args:
        image_path: The path to the image. Must be in the resource folder.
        template_path: The path to the template. Must be in the resource folder.
        manual_labels: Whether to generate test data manually (human labeling).
        test_dir: The path to the test data directory. Needs to be set when manual_labels is True.
    """
    # Generate answers
    image = imagex_mock.load_image(image_path)
    template = imagex_mock.load_image(template_path)
    # print(f"Finding {template_path.name} in {image_path.name}")
    if not manual_labels:
        bounding_boxes = imagex_mock.find(image, template)
    else:
        if test_dir is None:
            raise ValueError("test_dir must be set when manual_labels is True")
        bounding_boxes = imagex_manual.find(image, template, test_dir)
    # Get relative paths
    try:
        image_path = image_path.relative_to(RES_PATH)
        template_path = template_path.relative_to(RES_PATH)
    except ValueError:
        raise ValueError("Image and template paths must be relative to the resource folder")
    # Create test data
    return {
        "type": "find-one",
        "image": str(image_path),
        "template": str(template_path),
        "bounding_boxes": bounding_boxes,
    }


def save_test(test_dir: Path, test_name: str, test_data: dict) -> None:
    """
    Saves test data to disk as a json file.

    Args:
        test_dir: The path to the test data directory.
        test_name: The name of the test.
        test_data: The test data dictionary.
    """
    # Make test group path
    test_dir.mkdir(parents=True, exist_ok=True)
    # Create test data file
    with open(test_dir / f"{test_name}.json", "w") as file:
        json.dump(test_data, file)
    # print(f"Created test {test_name} in {test_dir.relative_to(TEST_DATA_PATH)}")


def gen_test_suite(test_dir: Path, images: list, templates: list,
                   gen_pairs: bool = False, manual_labels: bool = False,
                   max_tests: int = -1) -> None:
    """
    Generate a "find-one" test suite for the given image and template iterators.

    Warning: This function will overwrite any existing test data in the given directory.

    Args:
        test_dir: The path to the test data directory.
        images: An list of image paths.
        templates: An list of template paths.
        gen_pairs: Whether to generate tests for all pairs of images and templates. If set to False
        (default), each image will only be matched with the template at the same index.
        manual_labels: Whether to generate test data manually (human labeling).
        max_tests: The maximum number of tests to generate. Set to -1 (default) to generate all.
    """
    # Clear test directory
    if not regenerate_dir(test_dir, "Create test suite"):
        return
    # Seed RNG
    seed_gens(str(test_dir.relative_to(TEST_DATA_PATH)))
    # Generate pairs of images and templates
    if gen_pairs:
        tests = [(image, template) for image in images for template in templates]
    else:
        if len(images) != len(templates):
            raise ValueError("Number of images and templates must be equal if gen_pairs is False")
        tests = list(zip(images, templates))
    # Shuffle test order
    random.shuffle(tests)
    # Limit number of tests
    if max_tests >= 0:
        tests = tests[:max_tests]
    # Create tests
    for i, (image_path, template_path) in enumerate(tests):
        if manual_labels:
            print(f"Test {i + 1}/{len(tests)}")
        test_data = gen_test_data(image_path, template_path, manual_labels=manual_labels,
                                  test_dir=test_dir)
        # Get image name without prefix
        image_name = image_path.stem
        if image_name.startswith("image_"):
            image_name = image_name[6:]
        # Get template name without prefix
        template_name = template_path.stem
        if template_name.startswith("template_"):
            template_name = template_name[9:]
        test_name = f"{image_name}:{template_name}"
        save_test(test_dir, test_name, test_data)
    print(f"Generated {len(tests)} tests in {test_dir.relative_to(TEST_DATA_PATH)}")


def main():
    print("Creating mock test...")
    image_path = RES_PATH / "basic_shapes" / "image_noised_gaussian_light_1.png"
    # image_path = RES_PATH / "basic_shapes" / "image_scaled.png"
    template_path = RES_PATH / "basic_shapes" / "template_normal_triangle.png"
    test_data = gen_test_data(image_path, template_path, manual_labels=True,
                              test_dir=TEST_DATA_PATH / "00-mock")
    print(test_data)


if __name__ == "__main__":
    main()
