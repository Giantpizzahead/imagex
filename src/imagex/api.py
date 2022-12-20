"""
ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
from typing import Optional

import cv2


class BoundingBox:
    """Represents a bounding box with the given top-left corner, width, and height."""
    x: int
    y: int
    w: int
    h: int

    def __init__(self, x: int, y: int, w: int, h: int):
        """Creates a rectangle with the given top-left corner, width, and height."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_tuple(self) -> tuple:
        """Returns the bounding box as a tuple (x, y, w, h)."""
        return self.x, self.y, self.w, self.h

    def __str__(self) -> str:
        return f"BoundingBox({self.x}, {self.y}, {self.w}, {self.h})"

    def __repr__(self) -> str:
        return self.__str__()


class Image:
    """Represents an image."""

    def __init__(self, source):
        """Creates an image from the given source."""
        assert isinstance(source, str)
        self.image = cv2.imread(source)


def find(image: Image, template: Image) -> Optional[BoundingBox]:
    """Finds the template in the image and returns its bounding box (or None if not found)."""
    return None
