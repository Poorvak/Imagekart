"""Resizer module."""
try:
    from PIL import Image
except ImportError:
    raise ImportError("Install Pillow using pip isntall pillow")


class Resizer(object):
    """Resizer class for performing all logic based resizing."""

    def __init__(self, network_ver_dict=None, density_dict=None):
        """
        Resizer constructor.

        :args:
            :network_ver_dict: The `dict` of network states for different qualities
            :density_dict: The `dict` of density version with size as `set`
        """
        if not network_ver_dict:
            network_ver_dict = dict()
        if not density_dict:
            density_dict = dict(mdpi=(333, 175), hdpi=(500, 263),
                                xdpi=(666, 350), xxdpi=(1000, 525), xxxdpi=(1330, 700))
        self.network_ver_dict = network_ver_dict
        self.density_dict = density_dict

    def resize(self, path=None):
        """Resize image handler"""
        img = Image.open(path)
