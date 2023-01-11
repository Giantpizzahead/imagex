"""
Manual image labeler.

ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import imagex_mock

from context import *
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

import numpy as np


class GUI(tk.Tk):
    """
    GUI that displays a training image, and allows the user to draw bounding boxes around objects.
    """
    WIDTH = 1200
    HEIGHT = 600

    def __init__(self, image: np.ndarray, template: np.ndarray, test_dir: Path, initial_boxes: list):
        super().__init__()
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        self.title("ImageX - Manual Labeler")
        # Center the window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}"
                      f"+{round((s_width - self.WIDTH) / 2)}+{round((s_height - self.HEIGHT) / 2)}")
        self.update()
        self.resizable(False, False)

        self.image = image
        self.image_ratio = 1
        self.template = template
        self.current_box = None
        self.image_size = (0, 0)
        self.test_dir = test_dir
        self.is_drawing = False

        # Canvas on the left
        self.canvas = tk.Canvas(self, width=self.WIDTH * 0.7, height=self.HEIGHT)
        self.canvas.grid(row=0, column=0, rowspan=5)

        # Draw template on the right
        template = Image.fromarray(self.template)
        # Upscale template to 0.1 of the canvas width, preserving aspect ratio
        ratio = min((self.WIDTH * 0.1) / template.width, (self.HEIGHT * 0.2) / template.height)
        template = template.resize((round(template.width * ratio), round(template.height * ratio)))
        template = ImageTk.PhotoImage(template)

        self.template_str = tk.StringVar()
        self.update_template_str()
        template_text = tk.Label(self, textvariable=self.template_str)

        template_label = tk.Label(self, image=template)
        template_label.image = template
        # Button to undo last bounding box
        undo_button = tk.Button(self, text="Undo", command=self.remove_last_box)
        # Button to save bounding boxes on the right
        save_button = tk.Button(self, text="Done", command=self.destroy)
        # Button to mark image as ambiguous
        ambiguous_button = tk.Button(self, text="Ambiguous", command=self.mark_ambiguous)
        template_text.grid(row=0, column=1)
        template_label.grid(row=1, column=1)
        undo_button.grid(row=2, column=1, ipadx=50, ipady=20)
        save_button.grid(row=3, column=1, ipadx=50, ipady=20)
        ambiguous_button.grid(row=4, column=1, ipadx=30, ipady=20)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Convert image to PIL format
        self.pil_image = Image.fromarray(self.image)
        # Upscale image to fit canvas, preserving aspect ratio
        self.image_ratio = min((self.WIDTH * 0.75) / self.pil_image.width,
                               self.HEIGHT / self.pil_image.height)
        self.pil_image = self.pil_image.resize((round(self.pil_image.width * self.image_ratio),
                                                round(self.pil_image.height * self.image_ratio)))
        self.image_size = self.pil_image.size

        # Generate scaled initial bounding boxes
        if initial_boxes[0] is not NONE:
            self.bounding_boxes = [(round(x * self.image_ratio), round(y * self.image_ratio),
                                    round(w * self.image_ratio), round(h * self.image_ratio))
                                   for x, y, w, h in initial_boxes]
        else:
            self.bounding_boxes = []

        self.update_canvas()

    def on_click(self, event):
        """Called when the user clicks the mouse."""
        if event.x > self.image_size[0] or event.y > self.image_size[1]:
            return
        self.current_box = (event.x, event.y, 0, 0)

    def on_drag(self, event):
        """Called when the user drags the mouse."""
        if self.current_box is not None:
            x, y, w, h = self.current_box
            w = event.x - x
            h = event.y - y
            self.current_box = (x, y, w, h)
            self.update_canvas()

    def on_release(self, event):
        """Called when the user releases the mouse."""
        if self.current_box is not None:
            x, y, w, h = self.current_box
            w = event.x - x
            h = event.y - y
            self.current_box = (x, y, w, h)
            self.bounding_boxes.append(self.current_box)
            self.current_box = None
            self.update_canvas()

    def remove_last_box(self):
        """Removes the last bounding box."""
        if len(self.bounding_boxes) > 0:
            self.bounding_boxes.pop()
            self.update_canvas()

    def mark_ambiguous(self):
        """
        Marks the image as ambiguous.

        This means that ImageX would pass this test if it says no match OR finds one of
        the labeled bounding boxes).
        """
        self.bounding_boxes.append(NONE)
        self.destroy()

    def update_template_str(self):
        """Updates the template string."""
        output = f"Test group: {self.test_dir.relative_to(TEST_DATA_PATH)}\n\n"
        output += "Click and drag to add a bounding box.\n"
        output += "The outline should overlap the template.\n"
        output += "Press 'Undo' to remove the last box.\n"
        output += "Press 'Done' when finished.\n"
        output += "Press 'Ambiguous' if it's acceptable\nto output a match OR no match.\n\n"
        output += "Template:"
        self.template_str.set(output)

    def update_canvas(self):
        """Updates the image displayed in the canvas."""
        if self.is_drawing:
            return
        self.is_drawing = True
        # Draw bounding boxes
        img = self.pil_image.copy()
        draw = ImageDraw.Draw(img)
        for x, y, w, h in self.bounding_boxes:
            draw.rectangle((x, y, x + w, y + h), outline="orange", width=2)
        if self.current_box is not None:
            x, y, w, h = self.current_box
            draw.rectangle((x, y, x + w, y + h), outline="orange", width=2)

        # Display image on the right center
        image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.image = image

        # Update window title
        self.title(f"ImageX - Manual Labeler ({len(self.bounding_boxes)} bounding box"
                   f"{'es' if len(self.bounding_boxes) != 1 else ''})")

        # Update window
        self.update_template_str()
        self.update()
        self.is_drawing = False

    def get_bounding_boxes(self):
        """Returns the bounding boxes scaled to the original image size.

        Also adds some adjustments to account for human error.
        """
        actual_boxes = [(round(x / self.image_ratio), round(y / self.image_ratio),
                         round(w / self.image_ratio), round(h / self.image_ratio))
                        for x, y, w, h in self.bounding_boxes]
        # Add some adjustments to account for human error
        final_boxes = [box for box in actual_boxes]

        # def add_box(x, y, w, h):
        #     """Adds a box to the final boxes list."""
        #     if w <= 0 or h <= 0 or (x, y, w, h) in final_boxes:
        #         return
        #     final_boxes.append((x, y, w, h))

        # for x, y, w, h in actual_boxes:
        #     if (x, y, w, h) == NONE:
        #         continue
        #     # All measurements could be off by a bit
        #     # Put enough boxes for the test runner's error tolerance to accept the right answer
        #     add_box(x - 4, y - 4, w, h)
        #     add_box(x - 4, y + 4, w, h)
        #     add_box(x + 4, y - 4, w, h)
        #     add_box(x + 4, y + 4, w, h)
        #     add_box(x - 2, y - 2, w + 4, h + 4)
        #     add_box(x + 2, y + 2, w - 4, h - 4)
        if not final_boxes:
            final_boxes.append(NONE)
        return final_boxes

    def run(self):
        """Runs the GUI."""
        self.mainloop()
        return self.get_bounding_boxes()


def find(image: np.ndarray, template: np.ndarray, test_dir: Path) -> list:
    """
    Finds the template in the image and returns a list of all valid bounding boxes.

    Args:
        image: The image to search in.
        template: The template to search for.
        test_dir: The test directory.

    Returns:
        A list of all valid bounding boxes. Bounding boxes are represented as tuples (x, y, w, h).
        Bounding boxes are inclusive (i.e. the corners of the bounding box are part of the match).
    """
    # Get best match according to heuristic
    return GUI(image, template, test_dir, imagex_mock.find_heuristic(image, template)).run()
