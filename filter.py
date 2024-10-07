# This is a simple image filter script with a command line interface
# The user can apply different filters to an image file
# The resulting filtered image is saved as a separate file

import argparse
from enum import Enum
from PIL import Image
from typing import Any, Callable


class Filter(Enum):
    GRAYSCALE = 1
    SEPIA = 2
    WARMER = 3
    COOLER = 4


def filter_from_string(filter_name: str) -> Filter:
    """
    Converts the specified filter name to the corresponding Filter enum member.
    :param filter_name: filter name as a string
    :return: Filter enum member
    """
    enum_name = filter_name.upper()
    return Filter[enum_name]


def function_for_filter(filter_name: Filter) -> Callable[[Any, int, int], None]:
    """
    Converts the specified Filter enum member to its corresponding conversion function.
    :param filter_name: filter as a Filter enum member
    :return: conversion function as a Callable object
    """
    filter_map = {
        Filter.GRAYSCALE: convert_to_grayscale,
        Filter.SEPIA: convert_to_sepia,
        Filter.WARMER: convert_to_warmer,
        Filter.COOLER: convert_to_cooler
    }

    return filter_map[filter_name]


def apply_filter(input_img_name: str, output_img_name: str, filter_name: Filter, show_result: bool) -> None:
    """
    Applies the specified filter to the entire input image and saves the changes to the specified output image.
    :param input_img_name: file name of input image as a string
    :param output_img_name: file name of output image as a string
    :param filter_name: filter as a Filter enum member
    :param show_result: Boolean, display the filtered image if True, do not display if False
    :return: none
    """
    # Open the input image
    working_image = Image.open(input_img_name)

    # Extract pixel map and size of input image
    pixel_map = working_image.load()
    width, height = working_image.size

    # Apply corresponding conversion function
    function_for_filter(filter_name)(pixel_map, width, height)

    # Save and show the result
    working_image.save(output_img_name, format="png")

    if show_result:
        working_image.show()


def transform_pixels(pixel_map, width: int, height: int,
                     conversion_function: Callable[[Any, int, int], tuple[int, int, int]]) -> None:
    """
    Applied the specified conversion function to each pixel in the specified pixel map.
    :param pixel_map: pixel map of the working image as a PixelAccess object
    :param width: working image width as an integer
    :param height: working image height as an integer
    :param conversion_function: conversion function as a Callable object
    :return: none
    """
    for i in range(width):
        for j in range(height):
            # Save rgb value of current pixel
            r, g, b = pixel_map[i, j]

            # Apply conversion function to current pixel
            pixel_map[i, j] = conversion_function(r, g, b)


def convert_to_grayscale(pixel_map, width: int, height: int) -> None:
    """
    Converts the working image to grayscale.
    :param pixel_map: pixel map of the working image as a PixelAccess object
    :param width: working image width as an integer
    :param height: working image height as an integer
    :return: none
    """
    def grayscale_conversion_func(r: int, g: int, b: int) -> tuple[int, int, int]:
        # Convert pixel to grayscale using NTSC formula
        grayscale = (0.299 * r + 0.587 * g + 0.114 * b)
        return int(grayscale), int(grayscale), int(grayscale)

    transform_pixels(pixel_map, width, height, grayscale_conversion_func)


def convert_to_sepia(pixel_map, width: int, height: int) -> None:
    """
    Converts the working image to sepia.
    :param pixel_map: pixel map of the working image as an Image.core.PixelAccess object
    :param width: working image width as an integer
    :param height: working image height as an integer
    :return: none
    """
    def sepia_conversion_func(r: int, g: int, b: int) -> tuple[int, int, int]:
        # Convert pixel to sepia following Microsoft recommendation
        sepia_red = (0.393 * r + 0.769 * g + 0.189 * b)
        sepia_green = (0.349 * r + 0.686 * g + 0.168 * b)
        sepia_blue = (0.272 * r + 0.534 * g + 0.131 * b)
        return int(sepia_red), int(sepia_green), int(sepia_blue)

    transform_pixels(pixel_map, width, height, sepia_conversion_func)


def convert_to_warmer(pixel_map, width: int, height: int) -> None:
    """
    Converts the working image to a warmer color scale.
    :param pixel_map: pixel map of the working image as an Image.core.PixelAccess object
    :param width: working image width as an integer
    :param height: working image height as an integer
    :return: none
    """
    def warmer_conversion_func(r: int, g: int, b: int) -> tuple[int, int, int]:
        # Convert pixel to warmer color by increasing red and decreasing blue
        warmer_red = r + 15
        warmer_blue = b - 15
        return int(warmer_red), int(g), int(warmer_blue)

    transform_pixels(pixel_map, width, height, warmer_conversion_func)


def convert_to_cooler(pixel_map, width: int, height: int) -> None:
    """
    Converts the working image to a cooler color scale.
    :param pixel_map: pixel map of the working image as an Image.core.PixelAccess object
    :param width: working image width as an integer
    :param height: working image height as an integer
    :return: none
    """
    def cooler_conversion_func(r: int, g: int, b: int) -> tuple[int, int, int]:
        # Convert pixel to cooler color by decreasing red and increasing blue
        cooler_red = r - 15
        cooler_blue = b + 15
        return int(cooler_red), int(g), int(cooler_blue)

    transform_pixels(pixel_map, width, height, cooler_conversion_func)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="specify file name for image to be modified")
    parser.add_argument("-o", "--output", type=str, default="output_img.png",
                        help="Optional: specify file name for the output image")
    parser.add_argument("filter", choices=['grayscale', 'sepia', 'warmer', 'cooler'],
                        help="Enter filter name. Available filters: grayscale, sepia, warmer, cooler")
    parser.add_argument("-s", "--show", action="store_true", help="show output image")
    args = parser.parse_args()

    apply_filter(args.input, args.output, filter_from_string(args.filter), args.show)


if __name__ == '__main__':
    main()
