# pylint: disable=locally-disabled, C0103, R0201, C0411, W0403, W0401, W0611
"""Main module for aggreator of all image related tasks."""
import aws
import file_handler
try:
    import cv2
except ImportError:
    raise ImportError("Build and update cv2.so in $PATH")


class Performer(object):
    """Class for performing all the image actions."""

    def __init__(self, req_ratio=None, req_width=None, req_height=None,
        consideration_rate=None, dest=None):
        """
        Performer constructor method.
        :args:
            :required_ratio: The `desired` ratio of the output image
            :consideration_rate: The approximation value.
            :max_ratio: The maximum ratio to consider.
            :min_ratio: The minimum ration to consider.
        """
        if not req_ratio:
            req_ratio = 1.78
        if not req_width:
            req_width = 1330
        if not req_height:
            req_height = 700
        if not consideration_rate:
            consideration_rate = 0.5
        self.required_ratio = required_ratio
        self.consideration_rate = consideration_rate
        self.dest = dest
        if (self.required_ratio or self.consideration_rate) < 0:
            raise ValueError("The required_ration and consideration_rate should be positive value")

        self.min_ratio = self.required_ratio - self.consideration_rate
        self.max_ratio = self.required_ratio + self.consideration_rate
        if self.min_ratio < 0:
            self.min_ratio = 0

        self.downloader = file_handler.Downloader(project="news", progress_bar=False, dest=self.dest)
        self.resizer = resizer.Resizer()

    def perform_resize(self, urls):
        """
        Method to perform the resize operations.
        :args:

        """
        local_img_path = self.downloader.download(urls=urls)
        for local_path in local_img_path:
            self.resizer.resize(path=local_path)
