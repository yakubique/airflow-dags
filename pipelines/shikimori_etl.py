"""
This module contains the pipeline definition for the Shikimori ETL pipeline.
"""

from components.date import today_as_s3_key
from components.duckdb import jsonl_2_pq
from components.s3 import upload_to_s3
from components.shikimori import grab_pages
from kfp import dsl  # pylint: disable=wrong-import-order,import-error


@dsl.pipeline(
    name="Shikimori ETL",
    display_name="Shikimori ETL",
    description="Extract, transform, and load data from Shikimori",
)
def shikimori_etl_pipeline(is_testing: bool = True):
    """
    The Shikimori ETL pipeline.
        1. Grabs the anime and manga pages from Shikimori.
        2. Converts the JSONL files to Parquet files.
        3. Uploads the Parquet files to S3.
    """
    import uuid  # pylint: disable=import-outside-toplevel

    filename = str(uuid.uuid4()).split("-", maxsplit=1)[0]
    today = today_as_s3_key()
    today.set_caching_options(False)

    pages_task = grab_pages(  # pylint: disable=no-value-for-parameter
        is_testing=is_testing
    )
    anime_pq_task = jsonl_2_pq(  # pylint: disable=no-value-for-parameter
        json_input_path=pages_task.outputs["anime_path"]
    )
    manga_pq_task = jsonl_2_pq(  # pylint: disable=no-value-for-parameter
        json_input_path=pages_task.outputs["manga_path"]
    )

    modifier = "" if is_testing else "prod/"

    upload_to_s3(
        bucket_name="shikimori",
        key=[f"/poor/{modifier}anime", today.output, f"{filename}.parquet"],
        file_path=anime_pq_task.outputs["pq_output_path"],
    )
    upload_to_s3(
        bucket_name="shikimori",
        key=[f"/poor/{modifier}manga", today.output, f"{filename}.parquet"],
        file_path=manga_pq_task.outputs["pq_output_path"],
    )
