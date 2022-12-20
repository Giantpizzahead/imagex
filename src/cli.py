"""
ImageX - Regex for images
https://github.com/Giantpizzahead/imagex
Copyright (C) 2022 Giantpizzahead
"""
import argparse


def main():
    """Main entry point for the application script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("template")
    args = parser.parse_args()

    image, template = args.image, args.template
    print(image, template)


if __name__ == '__main__':
    main()
