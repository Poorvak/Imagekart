# pylint: disable=locally-disabled, C0103, R0201, C0411, W0403, W0401, W0611, R0913, R0902, R0903
"""Main module for aggreator of all image related tasks."""
import os

from aws import AWS
from image import (Resizer, Downloader)

from pprint import pprint


class Performer(object):
    """Class for performing all the image actions."""

    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 req_ratio=None, req_width=None, req_height=None,
                 consideration_rate=None, dest=None, ):
        """
        Performer constructor method.
        :args:
            :required_ratio: The `desired` ratio of the output image
            :consideration_rate: The approximation value.
            :max_ratio: The maximum ratio to consider.
            :min_ratio: The minimum ration to consider.
        """
        if not req_ratio:
            req_ratio = 1.9
        if not req_width:
            req_width = 1330
        if not req_height:
            req_height = 700
        if not consideration_rate:
            consideration_rate = 0.9
        self.req_ratio = req_ratio
        self.consideration_rate = consideration_rate
        self.dest = dest
        if (self.req_ratio or self.consideration_rate) < 0:
            raise ValueError("The required_ration and consideration_rate should be positive value")

        self.min_ratio = self.req_ratio - self.consideration_rate
        self.max_ratio = self.req_ratio + self.consideration_rate
        if self.min_ratio < 0:
            self.min_ratio = 0

        self.downloader = Downloader(project="news", progress_bar=False,
                                     dest=self.dest)
        self.resizer = Resizer(req_ratio=self.req_ratio, min_ratio=self.min_ratio,
                               max_ratio=self.max_ratio)
        self.aws = AWS(aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key)

    def perform_resize(self, urls):
        """
        Method to perform the resize operations.
        :args:

        """
        local_img_path = self.downloader.download(urls=urls)
        return_list = list()
        for local_path in local_img_path:
            _performed_imgs = self.resizer.resize(path=local_path)
            uploaded_url = None
            if _performed_imgs:
                for _performed_img in _performed_imgs:
                    filename = os.path.split(_performed_img)
                    uploaded_url = self.aws.upload_file(filename=filename[1],
                                                        filepath=_performed_img,
                                                        bucket_name="timepass-images")
                    if uploaded_url:
                        os.remove(_performed_img)
                    return_list.append(uploaded_url)
            try:
                os.remove(local_path)
            except OSError:
                pass
        return return_list
