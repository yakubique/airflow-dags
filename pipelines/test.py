from components.hello_world import hello_world
from kfp import dsl


@dsl.pipeline
def test_pipeline(recipient: str) -> str:
    hello_task = hello_world(name=recipient)

    return hello_task.output
