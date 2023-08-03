import cv2
import numpy as np

from bs4 import BeautifulSoup
from PIL import Image
from pathlib import Path

def crop_image(image_path, coords, output_path):
    """
    image_path: the path to the image to edit
    coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    output_path: path to the output image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(output_path)
    print(f"Image has been saved to: {output_path}")

def get_corners(coords):
    """
    coords: A list of (x,y) coordinate tuples
    """

    # Separate the list of tuples into two lists
    x_coords = [coord[0] for coord in coords]
    y_coords = [coord[1] for coord in coords]

    # Determine the corners
    bottom_left = (min(x_coords), min(y_coords))
    top_right = (max(x_coords), max(y_coords))
    bottom_right = (max(x_coords), min(y_coords))
    top_left = (min(x_coords), max(y_coords))

    return [top_left[0], top_left[1], bottom_right[0], bottom_right[1]]

def parse_text_area_coordinate(xml):

    soup = BeautifulSoup(xml, 'lxml')

    # find all 'TextRegion' tags
    text_regions = soup.find_all('textregion')

    for region in text_regions:
        # check if 'custom' attribute contains 'marginalia'
        if region['custom'] == 'readingOrder {index:0;}':
            coords = region.coords['points']
            # The coords string is in the form "x1,y1 x2,y2 x3,y3 x4,y4 ...". Split this into a list of (x, y) tuples.
            coords = [tuple(map(float, point.split(','))) for point in coords.split()]
            print('Coordinates:', coords)

    return coords


if __name__ == '__main__':
    xml = Path('./15520015.xml').read_text()
    coords = parse_text_area_coordinate(xml)
    corner_coords = get_corners(coords)
    crop_image('./15520015.png', corner_coords, './15520015_cropped.png')
