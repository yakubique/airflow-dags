"""
Components that utilizes `datetime` library.
"""

from kfp import dsl  # pylint: disable=import-error


@dsl.component(base_image="python:3.11")
def today_as_s3_key() -> str:
    """
    Returns the current date in the format of `year=%Y/month=%m/day=%d`.
    """
    from datetime import datetime  # pylint: disable=import-outside-toplevel

    return datetime.now().strftime("year=%Y/month=%m/day=%d")
