"""
Contains helper functions for drawing on images.

ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
from context import *

import cv2
import numpy as np
import skimage


class Color:
    """Class representing common colors"""
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (165, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (150, 75, 0)

    def __init__(self, r: int, g: int, b: int):
        """Create a custom RGB color."""
        self.value = (r, g, b)


def load_image(path: Path) -> np.ndarray:
    """Loads an image from disk, converting it to RGB format."""
    image = cv2.imread(str(path))
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_image(image: np.ndarray, path: Path) -> None:
    """Saves an image to disk."""
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(path), image)
    print(f"Image saved to {str(path.relative_to(ROOT_PATH))}")


def display_image(image: np.ndarray) -> None:
    """Displays an image."""
    print("Displaying image...")
    cv2.imshow("Image", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    cv2.waitKey(0)


def create_blank_image(width: int, height: int, color: tuple = Color.WHITE) -> np.ndarray:
    """Creates a blank image of a given size and color."""
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(color))
    image[:] = color
    return image


def draw_rectangle(image: np.ndarray, x: int, y: int, w: int, h: int, color: tuple,
                   thickness: int = 1, filled: bool = True) -> None:
    """
    Draws a rectangle on an image. Mutates the image.

    Args:
        image: The image to draw on.
        x: The x coordinate of the top left corner of the rectangle.
        y: The y coordinate of the top left corner of the rectangle.
        w: The width of the rectangle.
        h: The height of the rectangle.
        color: The RGB color of the rectangle.
        thickness: The thickness of the rectangle's outline. Has no effect if filled is True.
        filled: Whether to fill the rectangle.
    """
    cv2.rectangle(image, (x, y), (x + w, y + h), color, cv2.FILLED if filled else thickness)


def draw_circle(image: np.ndarray, x: int, y: int, r: int, color: tuple,
                thickness: int = 1, filled: bool = True) -> None:
    """
    Draws a circle on an image. Mutates the image.

    Args:
        image: The image to draw on.
        x: The x coordinate of the center of the circle.
        y: The y coordinate of the center of the circle.
        r: The radius of the circle.
        color: The RGB color of the circle.
        thickness: The thickness of the circle's outline. Has no effect if filled is True.
        filled: Whether to fill the circle.
    """
    cv2.circle(image, (x, y), r, color, cv2.FILLED if filled else thickness)


def draw_triangle(image: np.ndarray, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int,
                  color: tuple, thickness: int = 1, filled: bool = True) -> None:
    """
    Draws a triangle on an image. Mutates the image.

    Args:
        image: The image to draw on.
        x1: The x coordinate of the first vertex of the triangle.
        y1: The y coordinate of the first vertex of the triangle.
        x2: The x coordinate of the second vertex of the triangle.
        y2: The y coordinate of the second vertex of the triangle.
        x3: The x coordinate of the third vertex of the triangle.
        y3: The y coordinate of the third vertex of the triangle.
        color: The RGB color of the triangle.
        thickness: The thickness of the triangle's outline. Has no effect if filled is True.
        filled: Whether to fill the triangle.
    """
    cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    cv2.line(image, (x2, y2), (x3, y3), color, thickness)
    cv2.line(image, (x3, y3), (x1, y1), color, thickness)
    if filled:
        cv2.fillPoly(image, [np.array([[x1, y1], [x2, y2], [x3, y3]])], color)


def draw_text(image: np.ndarray, text: str, x: int, y: int, color: tuple, font_scale: float = 1,
              thickness: int = 2) -> None:
    """
    Draws text on an image. Mutates the image.

    Args:
        image: The image to draw on.
        text: The text to draw.
        x: The x coordinate of the text.
        y: The y coordinate of the text.
        color: The RGB color of the text.
        font_scale: The scale of the text relative to its base size.
        thickness: The thickness of the text.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)


NOISE_TYPES = ["gaussian", "speckle", "s&p"]


def add_noise(image: np.ndarray, noise_type: str, amount: float) -> np.ndarray:
    """
    Adds noise to an image. Use the NOISE_TYPES global to get a list of supported noise types.

    Args:
        image: The image to add noise to.
        noise_type: The type of noise to add. Can be "gaussian", "speckle", "s&p", or "poisson".
        amount: The amount of noise to add. Must be between 0 and 1. Has no effect for poisson.

    Returns:
        The image with noise added.
    """
    if noise_type == "gaussian":
        image = skimage.util.random_noise(image, mode="gaussian", var=amount/3)
    elif noise_type == "speckle":
        image = skimage.util.random_noise(image, mode="speckle", var=amount/3)
    elif noise_type == "s&p":
        image = skimage.util.random_noise(image, mode="s&p", amount=amount)
    else:
        raise ValueError(f"Invalid noise type: {noise_type}")
    image = image.astype(np.float32) * 255
    return image.astype(np.uint8)


def main():
    # Create a white image
    image = create_blank_image(500, 300, Color.WHITE)
    draw_rectangle(image, 30, 80, 250, 150, Color.BLUE, filled=True)
    draw_circle(image, 250, 150, 50, Color.RED, filled=True)
    draw_text(image, "Hello, world!", 30, 30, Color.BLACK)
    # Add noise
    image = add_noise(image, "s&p", 0.05)
    print(image.shape)
    # Display the image
    # display_image(image)
    # Save the image
    save_image(image, TEMP_PATH / "test.png")


if __name__ == '__main__':
    main()
