"""
ImageX - Regex for basic_shapes
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import time
from pathlib import Path
import drawer
import test_maker
from random import randint, seed


RES_NAME = "basic_shapes"
OUTPUT_PATH = Path(__file__).parent.parent.joinpath("res", RES_NAME).resolve()


seed(68543)
C1 = randint(15, 30)
C2 = randint(15, 30)
C3 = randint(8, 15)
C4 = randint(15, 30)
C5 = randint(8, 15) * 2  # Must be even


def draw_blue_rectangle(image, x, y):
    """Blue rectangle"""
    # Don't draw if not entirely in image
    if x < 0 or y < 0 or x+C1 > image.shape[1] or y+C2 > image.shape[0]:
        return False
    drawer.draw_rectangle(image, x, y, C1, C2, drawer.Color.BLUE)
    return True


def draw_green_circle(image, x, y):
    """Green circle with red background"""
    # Don't draw if not entirely in image
    if x < 0 or y < 0 or x+C3*2 > image.shape[1] or y+C3*2 > image.shape[0]:
        return False
    drawer.draw_rectangle(image, x, y, C3*2, C3*2, drawer.Color.RED)
    drawer.draw_circle(image, x+C3, y+C3, C3, drawer.Color.GREEN)
    return True


def draw_purple_triangle(image, x, y):
    """Purple triangle with yellow background"""
    # Don't draw if not entirely in image
    if x < 0 or y < 0 or x+C4 > image.shape[1] or y+C4 > image.shape[0]:
        return False
    drawer.draw_rectangle(image, x, y, C5, C4, drawer.Color.YELLOW)
    drawer.draw_triangle(image, x, y+C4, x+C5, y+C4, x+C5//2, y, drawer.Color.PURPLE)
    return True


def clear_output_dir(output_dir):
    for file in output_dir.glob("*"):
        file.unlink()
    print("Cleared output directory, waiting for a bit...")
    time.sleep(5)


def gen_templates():
    # Templates
    blue_rect = drawer.create_blank_image(C1, C2)
    draw_blue_rectangle(blue_rect, 0, 0)
    drawer.save_image(blue_rect, OUTPUT_PATH / "template_rect.png")

    green_circle = drawer.create_blank_image(C3*2, C3*2)
    draw_green_circle(green_circle, 0, 0)
    drawer.save_image(green_circle, OUTPUT_PATH / "template_circle.png")

    purple_triangle = drawer.create_blank_image(C2, C2)
    draw_purple_triangle(purple_triangle, 0, 0)
    drawer.save_image(purple_triangle, OUTPUT_PATH / "template_triangle.png")


def gen_batch(batch_size, name, min_size, max_size, num_shapes):
    assert num_shapes <= 3
    for i in range(1, batch_size+1):
        image = drawer.create_blank_image(randint(min_size, max_size), randint(min_size, max_size))
        shapes_drawn = 0
        used = set()
        while shapes_drawn < num_shapes:
            x = randint(0, image.shape[1])
            y = randint(0, image.shape[0])
            r = randint(0, 2)
            did_draw = False
            if r in used:
                continue
            if r == 0:
                did_draw = draw_blue_rectangle(image, x, y)
            elif r == 1:
                did_draw = draw_green_circle(image, x, y)
            elif r == 2:
                did_draw = draw_purple_triangle(image, x, y)
            if did_draw:
                shapes_drawn += 1
                used.add(r)
        drawer.save_image(image, OUTPUT_PATH / f"image_{name}_{i}.png")


def gen_images():
    # Images
    gen_batch(2, "small", 50, 100, 1)
    gen_batch(2, "medium", 100, 300, 2)
    gen_batch(2, "large", 300, 1000, 3)
    gen_batch(5, "overlap", 50, 100, 3)
    # Edge cases
    image = drawer.create_blank_image(100, 5)
    drawer.save_image(image, OUTPUT_PATH / "image_edge_1.png")
    image = drawer.create_blank_image(5, 100)
    drawer.save_image(image, OUTPUT_PATH / "image_edge_2.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.PURPLE)
    drawer.save_image(image, OUTPUT_PATH / "image_solid_1.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.YELLOW)
    drawer.save_image(image, OUTPUT_PATH / "image_solid_2.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.GREEN)
    drawer.save_image(image, OUTPUT_PATH / "image_solid_3.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.RED)
    drawer.save_image(image, OUTPUT_PATH / "image_solid_4.png")
    image = drawer.create_blank_image(100, 100, drawer.Color.BLUE)
    drawer.save_image(image, OUTPUT_PATH / "image_solid_5.png")


def gen_test_1(template_path, test_name):
    template = drawer.load_image(OUTPUT_PATH / template_path)
    expected = test_maker.naive_find(template, template)
    test_data = test_maker.gen_test_data(str(Path(RES_NAME).joinpath(template_path)),
                                         str(Path(RES_NAME).joinpath(template_path)), expected)
    test_maker.create_test("01-find-identity/basic_shapes", test_name, test_data)


def gen_test_suite_1():
    def _gen_test(template_path, test_name):
        _template = drawer.load_image(OUTPUT_PATH / template_path)
        expected = test_maker.naive_find(_template, _template)
        test_data = test_maker.gen_test_data(str(Path(RES_NAME).joinpath(template_path)),
                                             str(Path(RES_NAME).joinpath(template_path)), expected)
        test_maker.create_test("01-find-identity/basic_shapes", test_name, test_data)
    # For each template
    test_num = 1
    for template in OUTPUT_PATH.glob("template_*.png"):
        _gen_test(template.name, str(test_num))
        test_num += 1


def gen_test_suite_2():
    def _gen_test(image_path, template_path, test_name):
        _image = drawer.load_image(OUTPUT_PATH / image_path)
        _template = drawer.load_image(OUTPUT_PATH / template_path)
        expected = test_maker.naive_find(_image, _template)
        test_data = test_maker.gen_test_data(str(Path(RES_NAME).joinpath(image_path)),
                                             str(Path(RES_NAME).joinpath(template_path)), expected)
        test_maker.create_test("02-find-copy-exact/basic_shapes", test_name, test_data)
    # For each template
    test_num = 1
    for template in OUTPUT_PATH.glob("template_*.png"):
        # For each image
        for image in OUTPUT_PATH.glob("image_*.png"):
            _gen_test(image.name, template.name, str(test_num))
            test_num += 1


def main():
    clear_output_dir(OUTPUT_PATH)
    gen_templates()
    gen_images()
    clear_output_dir(test_maker.TEST_PATH / "01-find-identity" / "basic_shapes")
    gen_test_suite_1()
    gen_test_suite_2()
    print("Done!")


if __name__ == '__main__':
    main()
