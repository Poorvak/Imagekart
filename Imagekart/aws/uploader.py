# pylint: disable=E1101, W0631, R0914, R0913, R0201, W0123, W0201, W0212, R0903, W0621
"""Uploader file to S3."""
import boto3

from pprint import pprint
from boto3.s3.transfer import S3Transfer


class AWS(object):
    """AWS class for all AWS related stuff."""
    def __init__(self, aws_access_key_id,
                 aws_secret_access_key):
        """Constructor method to define the client object."""
        self.__session = boto3.session.Session(region_name="ap-south-1")
        self.__client = self.__session.client(
            "s3", aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=boto3.session.Config(signature_version="s3v4"))
        self.__transfer = S3Transfer(client=self.__client)

    def create_bucket(self, bucket_name, region="ap-northeast-1"):
        """Creates bucket."""
        self.__client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration=dict(LocationConstraint=region))

    def upload_file(self, filename, filepath, bucket_name, acl="public-read-write"):
        """Upload File to S3."""
        url = None
        try:
            data = open(filepath, "rb")
        except Exception as exc:
            data = None
        if data:
            self.__transfer.upload_file(filename=filepath, bucket=bucket_name, key=filename)
            response = self.__client.put_object_acl(Bucket=bucket_name, ACL=acl, Key=filename)
            url = "".join(["https://", "s3.ap-south-1.amazonaws.com/", bucket_name, "/", filename])
        return url
