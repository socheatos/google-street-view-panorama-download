# code from 
# https://github.com/robertyoung2/sidewalk-panorama-tools/blob/master/CropRunner.py

from PIL import Image, ImageDraw
from matplotlib.pyplot import imshow, figure, gcf, gca, show
import numpy as np


def predict_crop_size(sv_image_y):
    """
    Calculate distance from point to image center

    dist_to_center = math.sqrt((x-im_width/2)**2 + (y-im_height/2)**2)
    
    Calculate distance from point to center of left edge
    dist_to_left_edge = math.sqrt((x-0)**2 + (y-im_height/2)**2)
    
    Calculate distance from point to center of right edge
    dist_to_right_edge = math.sqrt((x - im_width) ** 2 + (y - im_height/2) ** 2)
    min_dist = min([dist_to_center, dist_to_left_edge, dist_to_right_edge])
    crop_size = (4.0/15.0)*min_dist + 200
    print("Min dist was "+str(min_dist))

    """
    crop_size = 0
    distance = max(0, 19.80546390 + 0.01523952 * sv_image_y)

    if distance > 0:
        crop_size = 8725.6 * (distance ** -1.192)
    if crop_size > 1500 or distance == 0:
        crop_size = 1500
    if crop_size < 50:
        crop_size = 50

    return crop_size



def make_single_crop(path_to_image, sv_image_x, sv_image_y, PanoYawDeg, output_filename, draw_mark=False):
    """
    Makes a crop around the object of interest
    :param path_to_image: where the GSV pano is stored
    :param sv_image_x: position
    :param sv_image_y: position
    :param PanoYawDeg: heading
    :param output_filename: name of file for saving
    :param draw_mark: if a dot should be drawn in the centre of the object/image
    :return: none
    """
    im = Image.open(path_to_image)
    draw = ImageDraw.Draw(im)

    im_width = im.size[0]
    im_height = im.size[1]
    print(im_width, im_height)

    predicted_crop_size = predict_crop_size(sv_image_y)
    crop_width = predicted_crop_size
    crop_height = predicted_crop_size
    print(crop_width, crop_height)

    # Work out scaling factor based on image dimensions
    scaling_factor = im_width / 13312
    sv_image_x *= scaling_factor
    sv_image_y *= scaling_factor

    x = ((float(PanoYawDeg) / 360) * im_width + sv_image_x) % im_width
    y = im_height / 2 - sv_image_y

    r = 10
    if draw_mark:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=128)

    print("Plotting at " + str(x) + "," + str(y) + " using yaw " + str(PanoYawDeg))

    top_left_x = x - crop_width / 2
    top_left_y = y - crop_height / 2
    cropped_square = im.crop((top_left_x, top_left_y, top_left_x + crop_width, top_left_y + crop_height))
    # cropped_square.show()
    cropped_square.save(output_filename)

    return