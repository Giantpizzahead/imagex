"""
Generates the basic_shapes test suite.

Resources:
basic_shapes/

Test data:
01-find-identity/basic_shapes/
02-find-copy-exact/basic_shapes/

ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import drawer
import make_tests
from context import *


SHAPES_PATH = RES_PATH / "basic_shapes"


# For consistency
seed_gens("constant_gen")
C1 = random.randint(15, 30)
C2 = random.randint(15, 30)
C3 = random.randint(8, 15)
C4 = random.randint(15, 30)
C5 = random.randint(8, 15) * 2  # Must be even


def draw_blue_rectangle(image, x, y, scale=1.0):
    """Blue rectangle"""
    # Don't draw if not entirely in image
    scaled_C1 = round(C1 * scale)
    scaled_C2 = round(C2 * scale)
    if x < 0 or y < 0 or x+scaled_C1 > image.shape[1] or y+scaled_C2 > image.shape[0]:
        return False
    drawer.draw_rectangle(image, x, y, scaled_C1, scaled_C2, drawer.Color.BLUE)
    return True


def draw_green_circle(image, x, y, scale=1.0):
    """Green circle with red background"""
    # Don't draw if not entirely in image
    scaled_C3 = round(C3 * scale)
    if x < 0 or y < 0 or x+scaled_C3*2 > image.shape[1] or y+scaled_C3*2 > image.shape[0]:
        return False
    drawer.draw_rectangle(image, x, y, scaled_C3*2, scaled_C3*2, drawer.Color.RED)
    drawer.draw_circle(image, x+scaled_C3, y+scaled_C3, scaled_C3, drawer.Color.GREEN)
    return True


def draw_purple_triangle(image, x, y, scale=1.0):
    """Purple triangle with yellow background"""
    # Don't draw if not entirely in image
    scaled_C4 = round(C4 * scale)
    scaled_C5 = round(C5 * scale)
    if x < 0 or y < 0 or x+scaled_C5 > image.shape[1] or y+scaled_C4 > image.shape[0]:
        return False
    drawer.draw_rectangle(image, x, y, scaled_C5, scaled_C4, drawer.Color.YELLOW)
    drawer.draw_triangle(image, x, y+scaled_C4, x+scaled_C5,
                         y+scaled_C4, x+scaled_C5//2, y, drawer.Color.PURPLE)
    return True


def gen_normal_templates():
    # Basic templates
    blue_rect = drawer.create_blank_image(C1, C2)
    draw_blue_rectangle(blue_rect, 0, 0)
    drawer.save_image(blue_rect, SHAPES_PATH / "template_normal_rect.png")

    green_circle = drawer.create_blank_image(C3*2, C3*2)
    draw_green_circle(green_circle, 0, 0)
    drawer.save_image(green_circle, SHAPES_PATH / "template_normal_circle.png")

    purple_triangle = drawer.create_blank_image(C5, C4)
    draw_purple_triangle(purple_triangle, 0, 0)
    drawer.save_image(purple_triangle, SHAPES_PATH / "template_normal_triangle.png")


def gen_scaled_templates():
    # Small templates
    blue_rect = drawer.create_blank_image(round(C1*0.5), round(C2*0.5))
    draw_blue_rectangle(blue_rect, 0, 0, scale=0.5)
    drawer.save_image(blue_rect, SHAPES_PATH / "template_scaled_rect1.png")

    green_circle = drawer.create_blank_image(round(C3*2*0.5), round(C3*2*0.5))
    draw_green_circle(green_circle, 0, 0, scale=0.5)
    drawer.save_image(green_circle, SHAPES_PATH / "template_scaled_circle1.png")

    purple_triangle = drawer.create_blank_image(round(C5*0.5), round(C4*0.5))
    draw_purple_triangle(purple_triangle, 0, 0, scale=0.5)
    drawer.save_image(purple_triangle, SHAPES_PATH / "template_scaled_triangle1.png")

    # Large templates
    blue_rect = drawer.create_blank_image(round(C1*1.5), round(C2*1.5))
    draw_blue_rectangle(blue_rect, 0, 0, scale=1.5)
    drawer.save_image(blue_rect, SHAPES_PATH / "template_scaled_rect2.png")

    green_circle = drawer.create_blank_image(round(C3*2*1.5), round(C3*2*1.5))
    draw_green_circle(green_circle, 0, 0, scale=1.5)
    drawer.save_image(green_circle, SHAPES_PATH / "template_scaled_circle2.png")

    purple_triangle = drawer.create_blank_image(round(C5*1.5), round(C4*1.5))
    draw_purple_triangle(purple_triangle, 0, 0, scale=1.5)
    drawer.save_image(purple_triangle, SHAPES_PATH / "template_scaled_triangle2.png")

    # Huge templates
    green_circle = drawer.create_blank_image(round(C3*2*4.1), round(C3*2*4.1))
    draw_green_circle(green_circle, 0, 0, scale=4.1)
    drawer.save_image(green_circle, SHAPES_PATH / "template_scaled_circle3.png")

    purple_triangle = drawer.create_blank_image(round(C5*13.6), round(C4*13.6))
    draw_purple_triangle(purple_triangle, 0, 0, scale=13.6)
    drawer.save_image(purple_triangle, SHAPES_PATH / "template_scaled_triangle3.png")


def gen_batch(batch_size, name, min_size, max_size, num_shapes, noise=None, scale=None):
    """
    Generate a batch of images with random shapes

    Args:
        batch_size: Number of images to generate
        name: Name of the batch
        min_size: Minimum size of the image
        max_size: Maximum size of the image
        num_shapes: Number of shapes to draw
        noise: If not None, add noise to the image based on the given (noise_type, noise_amount)
        scale: If not None, scale each template by a float in the range (min_scale, max_scale)
    """
    assert num_shapes <= 3
    for i in range(1, batch_size+1):
        image = drawer.create_blank_image(random.randint(min_size, max_size),
                                          random.randint(min_size, max_size))
        # Draw shapes
        shapes_drawn = 0
        used = set()
        while shapes_drawn < num_shapes:
            # Choose a random unused shape to draw
            x = random.randint(0, image.shape[1])
            y = random.randint(0, image.shape[0])
            r = random.randint(0, 2)
            if r in used:
                continue
            if r == 0:
                draw_func = draw_blue_rectangle
            elif r == 1:
                draw_func = draw_green_circle
            elif r == 2:
                draw_func = draw_purple_triangle
            else:
                raise ValueError("Invalid shape")
            # Draw the shape
            if scale is not None:
                min_scale, max_scale = scale
                curr_scale = random.random() * (max_scale - min_scale) + min_scale
                did_draw = draw_func(image, x, y, scale=curr_scale)
            else:
                did_draw = draw_func(image, x, y)
            # Check if the shape was drawn
            if did_draw:
                shapes_drawn += 1
                used.add(r)
        # Add noise
        if noise is not None:
            image = drawer.add_noise(image, *noise)
        drawer.save_image(image, SHAPES_PATH / f"image_{name}_{i}.png")


def gen_exact_images():
    # Exact images
    gen_batch(2, "exact_small", 50, 100, 1)
    gen_batch(2, "exact_medium", 100, 300, 2)
    gen_batch(2, "exact_large", 300, 1000, 3)
    gen_batch(5, "exact_overlap", 50, 100, 3)
    # Edge cases
    image = drawer.create_blank_image(100, 5)
    drawer.save_image(image, SHAPES_PATH / "image_exact_edge_1.png")
    image = drawer.create_blank_image(5, 100)
    drawer.save_image(image, SHAPES_PATH / "image_exact_edge_2.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.PURPLE)
    drawer.save_image(image, SHAPES_PATH / "image_exact_solid_1.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.YELLOW)
    drawer.save_image(image, SHAPES_PATH / "image_exact_solid_2.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.GREEN)
    drawer.save_image(image, SHAPES_PATH / "image_exact_solid_3.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.RED)
    drawer.save_image(image, SHAPES_PATH / "image_exact_solid_4.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.BLUE)
    drawer.save_image(image, SHAPES_PATH / "image_exact_solid_5.png")


def gen_noised_images():
    # Noised images
    for noise_type in drawer.NOISE_TYPES:
        gen_batch(1, f"noised_{noise_type}_light", 100, 150, 3, noise=(noise_type, 0.03))
        gen_batch(1, f"noised_{noise_type}_medium", 100, 150, 3, noise=(noise_type, 0.09))
        gen_batch(1, f"noised_{noise_type}_heavy", 100, 150, 3, noise=(noise_type, 0.15))


def gen_scaled_images():
    # Scaled images
    gen_batch(3, "scaled_half", 100, 200, 3, scale=(0.5, 0.5))
    gen_batch(3, "scaled_double", 200, 400, 3, scale=(2.0, 2.0))
    gen_batch(3, "scaled_random", 150, 400, 3, scale=(0.5, 2.0))
    gen_batch(2, "scaled_tiny", 100, 200, 3, scale=(0.1, 0.5))
    gen_batch(2, "scaled_huge", 600, 1000, 3, scale=(2.0, 10.0))
    # Scaled and noise images
    for noise_type in drawer.NOISE_TYPES:
        gen_batch(1, f"scaled&noised_{noise_type}_light", 200, 400, 3,
                  noise=(noise_type, 0.03), scale=(0.3, 3.0))
        gen_batch(1, f"scaled&noised_{noise_type}_medium", 200, 400, 3,
                  noise=(noise_type, 0.09), scale=(0.3, 3.0))
        gen_batch(1, f"scaled&noised_{noise_type}_heavy", 200, 400, 3,
                  noise=(noise_type, 0.15), scale=(0.3, 3.0))


def main():
    # Generate images, templates, and test suites
    regen_images = make_tests.regenerate_dir(SHAPES_PATH, "Generate images and templates")
    if regen_images:
        seed_gens("regen_images")
        gen_normal_templates()
        gen_exact_images()
        gen_noised_images()
        gen_scaled_templates()
        gen_scaled_images()
    seed_gens("normal_templates")
    normal_templates = list(SHAPES_PATH.glob("template_normal_*.png"))
    normal_templates.sort()
    make_tests.gen_test_suite(TEST_DATA_PATH / "01-find-identity" / "basic_shapes",
                              normal_templates, normal_templates)
    make_tests.gen_test_suite(TEST_DATA_PATH / "02-find-copy-exact" / "basic_shapes",
                              list(SHAPES_PATH.glob("image_exact_*.png")), normal_templates,
                              gen_pairs=True)
    make_tests.gen_test_suite(TEST_DATA_PATH / "03-find-copy-noise" / "basic_shapes",
                              list(SHAPES_PATH.glob("image_noised_*.png")), normal_templates,
                              gen_pairs=True, manual_labels=True, max_tests=20)
    make_tests.gen_test_suite(TEST_DATA_PATH / "06-find-scaled-exact" / "basic_shapes",
                              list(SHAPES_PATH.glob("image_scaled_*.png")),
                              list(SHAPES_PATH.glob("template_scaled_*.png")) + normal_templates,
                              gen_pairs=True, manual_labels=True, max_tests=20)
    make_tests.gen_test_suite(TEST_DATA_PATH / "07-find-scaled-noise" / "basic_shapes",
                              list(SHAPES_PATH.glob("image_scaled&noised_*.png")),
                              list(SHAPES_PATH.glob("template_scaled_*.png")) + normal_templates,
                              gen_pairs=True, manual_labels=True, max_tests=20)
    print("Done!")


if __name__ == '__main__':
    main()
