"""
Implements a naive but correct version of the ImageX API. This is used to generate test data.

ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""

import skimage

from context import *

import cv2
import numpy as np


def load_image(path: Path) -> np.ndarray:
    """Loads an image from disk, converting it to RGB format."""
    image = cv2.imread(str(path))
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def find(image: np.ndarray, template: np.ndarray) -> list:
    """
    Finds the template in the image and returns a list of all valid bounding boxes.

    This only finds exact matches! (Pixel perfect)

    Args:
        image: The image to search in.
        template: The template to search for.

    Returns:
        A list of all valid bounding boxes. Bounding boxes are represented as tuples (x, y, w, h).
        Bounding boxes are inclusive (i.e. the corners of the bounding box are part of the match).
        A bounding box of (0, 0, 0, 0) in the list means that no match was found.
    """
    # For each possible location of template, check if it matches image
    matches = []
    for y in range(image.shape[0] - template.shape[0] + 1):
        for x in range(image.shape[1] - template.shape[1] + 1):
            # Check if the template matches the image at this location
            if np.all(image[y:y+template.shape[0], x:x+template.shape[1]] == template):
                matches.append((x, y, template.shape[1], template.shape[0]))
    print(f"Found {len(matches)} matches")
    if not matches:
        matches.append(NONE)
    return matches


def find_heuristic(image: np.ndarray, template: np.ndarray) -> list:
    """
    Same as find, but uses cv2.matchTemplate() - meaning the results might not be right.
    Assumes that there is either 0 or 1 match.
    """
    # Try different template sizes
    best_val = 1
    best_match = None
    for scale in [1, 0.5, 2]:
        # Resize the image according to the scale
        resized = skimage.transform.rescale(template, scale, channel_axis=2, anti_aliasing=True)
        resized = (resized * 255).astype(np.uint8)
        if resized.shape[0] > image.shape[0] or resized.shape[1] > image.shape[1]:
            continue
        resized = resized.astype(np.float32) / 255
        image = image.astype(np.float32) / 255
        res = cv2.matchTemplate(image, resized, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val <= min(0.4, best_val):
            best_match = [min_loc[0], min_loc[1], resized.shape[1], resized.shape[0]]
            print(f"Found match {best_match} with scale {scale} and value {min_val}")
            best_val = min_val
            if best_val <= 0.1:
                # Good enough match; break early
                break
    return [best_match] if best_match else [NONE]
