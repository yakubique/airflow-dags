"""
This component uploads/downloads a file to/from an S3 bucket.
"""

from typing import List

from kfp import dsl  # pylint: disable=import-error


@dsl.component(
    base_image="python:3.11",
    packages_to_install=["boto3==1.35.86"],
)
def upload_to_s3(
    file_path: dsl.InputPath("file"),
    bucket_name: str,
    key: List[str],
):
    """
    Uploads a file to an S3 bucket.
    """
    s3_key_id = "ScoVfeV1Q1lc1X7Bc8hK"
    s3_access_key = "mHvUJ7GterdyuKwBcqebaMftn9h7cJjxwyHMm0U5"
    s3_endpoint = "https://minio-api.local.opa-oz.live"
    import boto3  # pylint: disable=import-outside-toplevel, import-error

    if not key[0].startswith("/"):
        key[0] = f"/{key}"
        print("Someone forgot to add a leading slash to the key")

    client = boto3.client(
        "s3",
        aws_access_key_id=s3_key_id,
        aws_secret_access_key=s3_access_key,
        endpoint_url=s3_endpoint,
    )

    print(f"Uploading {file_path} to s3://{bucket_name}/{key}")
    client.upload_file(file_path, bucket_name, "/".join(key))
