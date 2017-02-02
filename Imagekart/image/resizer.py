"""Resizer module."""
from __future__ import division
# pylint: disable=locally-disabled, C0103, R0903, C0411, W0403, W0401, W0611, R0913, C0301
import os

from pprint import pprint
try:
    from PIL import Image
except ImportError:
    raise ImportError("Install Pillow using pip install pillow")


class Resizer(object):
    """Resizer class for performing all logic based resizing."""

    def __init__(self, req_ratio, max_ratio=None, min_ratio=None, network_ver_dict=None, density_dict=None):
        """
        Resizer constructor.

        :args:
            :network_ver_dict: The `dict` of network states for different qualities
            :density_dict: The `dict` of density version with size as `set`
        """
        if not network_ver_dict:
            network_ver_dict = dict(low=30, high=60, small=15)
        if not density_dict:
            density_dict = dict(hdpi=(500, 263), xdpi=(666, 350),
                                xxdpi=(1000, 525), xxxdpi=(1330, 700))
        self.req_ratio = req_ratio
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.density_dict = density_dict
        self.network_ver_dict = network_ver_dict

    def resize(self, path):
        """Resize image handler"""
        try:
            img = Image.open(path)
        except Exception as exc:
            pprint(exc)
            img = None
        return_list = list()
        if img:
            original_img_width = img.size[0]
            original_img_height = img.size[1]
            img_ratio = original_img_width / original_img_height

            if self.min_ratio <= img_ratio <= self.max_ratio:
                # Maintain original image aspect ratio before cropping image.
                required_canvas = self.density_dict.get("xxxdpi")
                required_ratio = required_canvas[0] / required_canvas[1]
                # Case 1: When image completely greater than canvas.
                if original_img_width > required_canvas[0] and original_img_height > required_canvas[1]:
                    # Case 1.1: When ratio less than required ratio(do width meet)(Shrink Height)
                    if img_ratio < required_ratio:
                        new_width = required_canvas[0]
                        new_height = new_width / img_ratio
                    # Case 1.2: When ration greater than required ratio(do height meet)(Shrink Width)
                    elif img_ratio > required_ratio:
                        new_height = required_canvas[1]
                        new_width = new_height / img_ratio

                #Case 2: When image completely less than canvas.
                elif  original_img_width < required_canvas[0] and original_img_height < required_canvas[1]:
                    # Case 2.1: When ratio less than required ratio(do width meet)(Stretch Height)
                    if img_ratio < required_ratio:
                        new_width = required_canvas[0]
                        new_height = new_width * img_ratio

                    # Case 2.2: When ration greater than required ratio(do height meet)(Stretch width)
                    elif img_ratio > required_ratio:
                        new_height = required_canvas[1]
                        new_width = new_height * img_ratio

                #Case 3: When width is only greater than canvas but height less than canvas.
                elif original_img_width > required_canvas[0] and original_img_height < required_canvas[1]:
                    # Case 3.1: When ration greater than required ratio(do height meet)(Stretch width)
                    new_height = required_canvas[1]
                    new_width = new_height * img_ratio
                elif original_img_width < required_canvas[0] and original_img_height > required_canvas[1]:
                #Case 4: When height is only grater than canvas but width less than canvas.
                    # Case 4.1: When ratio less than required ratio(do width meet)(Stretch height)
                    new_width = required_canvas[0]
                    new_height = new_width * img_ratio

                dimensions = None
                # If True then something needs to be cropped.
                if new_width - required_canvas[0] or new_height - required_canvas[1]:
                    # Width greater than required canvas
                    if new_width - required_canvas[0]:
                        diff = abs(new_width - required_canvas[0])/2
                        dimensions = (int(diff), 0, int(new_width - diff), int(new_height))
                    # Height greater than required canvas
                    else:
                        diff = abs(new_height - required_canvas[1])/2
                        dimensions = (0, int(diff), int(new_width), int(new_height - diff))

                img = img.resize(size=(int(new_width), int(new_height)), resample=Image.ANTIALIAS)
                if dimensions:
                    img = img.crop(dimensions)
            else:
                pass
            split_path = path.split("/")
            path_save = "/".join(split_path[:-1])
            img_name = split_path[-1].split(".")[0]
            for key_net, value_net in self.network_ver_dict.iteritems():
                for key_den, val_den in self.density_dict.iteritems():
                    if img:
                        img_low = img.resize(size=val_den, resample=Image.ANTIALIAS)
                        img_save_name = ".".join(["_".join([img_name, key_net, key_den]), "jpg"])
                        img_low.save(os.path.join(path_save, img_save_name),
                                     progressive=True, quality=value_net, format="JPEG")
                        return_list.append(os.path.join(path_save, img_save_name))
        return return_list
