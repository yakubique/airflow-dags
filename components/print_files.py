"""
This component reads a JSON file and prints its contents.
"""

from kfp import dsl  # pylint: disable=import-error


@dsl.component(base_image="python:3.11")
def print_json(input_path: dsl.InputPath("json")):
    """
    Prints the contents of a JSON file.
    NOTE: this is just path, not the actual data
    """
    print(input_path)

    with open(input_path, "r", encoding="utf8") as f:
        print(f.read())
