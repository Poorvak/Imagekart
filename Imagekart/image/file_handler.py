# pylint: disable=locally-disabled, C0103, R0201, C0411, W0403, W0401, W0611, R0913
"""Module for handling files."""
import os
import urlparse
import pySmartDL


class Downloader(object):
    """Downloader class for handling all download operations."""

    def __init__(self, project, dest=None, progress_bar=None, thread_count=None, user_agent=None):
        """Initializer for `Downloader` class."""
        if not dest:
            dest = "/var/{project_name}".format(project_name=project)
        if not progress_bar:
            progress_bar = False
        if not thread_count:
            thread_count = pySmartDL.pySmartDL.multiprocessing.cpu_count()
        if not user_agent:
            user_agent = False
        self.dest = dest
        self.project = project
        self.thread_count = thread_count
        self.progress_bar = progress_bar
        if user_agent:
            self.user_agents = pySmartDL.utils.get_random_useragent

    def download(self, urls, dest=None, file_name=None):
        """Download method for managing the downloads."""
        if not dest:
            dest = self.dest
        if not isinstance(urls, list):
            urls = [urls]
        return_list = list()
        for url in urls:
            if not file_name:
                urlparser = urlparse.urlparse(url)
                file_name = urlparser.path.split("/")[-1]
            return_path = os.path.join(dest, file_name)
            download_obj = pySmartDL.SmartDL(urls=urls, progress_bar=self.progress_bar,
                                             dest=return_path)
            download_obj.start(blocking=False)
            if download_obj.isSuccessful():
                return_list.append(return_path)
            else:
                return_list.append(None)
        return return_list
