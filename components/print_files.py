from kfp import dsl


@dsl.component(base_image="python:3.11")
def print_json(input_path: dsl.InputPath("json")):
    # NOTE: this is just path, not the actual data
    print(input_path)
    with open(input_path, "r") as f:
        print(f.read())
