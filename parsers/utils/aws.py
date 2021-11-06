"""AWS Operations."""

import tempfile
from json import dumps, load
from typing import List

import boto3
from botocore.exceptions import ClientError

from ..config import settings


def get_file_content(filename: str, default: str):
    """Returns the meals saved in AWS."""
    s3 = boto3.client("s3")
    with tempfile.TemporaryFile() as fp:
        try:
            s3.download_fileobj(settings.s3_bucket_name, filename, fp)
        except ClientError as exc:
            if "404" in str(exc):
                save_file_content(default, filename)
                return get_file_content(filename, default)
            raise

        fp.seek(0)
        return load(fp)


def save_file_content(file_content: str, filename: str):
    """Saves meals in AWS."""
    s3 = boto3.client("s3")
    with tempfile.TemporaryFile() as fp:
        fp.write(file_content.encode("utf8"))
        fp.seek(0)
        try:
            s3.upload_fileobj(fp, settings.s3_bucket_name, filename)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "NoSuchBucket":
                create_bucket()
                return save_file_content(file_content, filename)
            raise


def create_bucket():
    """Creates the AWS bucket."""
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket=settings.s3_bucket_name)
