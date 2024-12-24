"""
%% [markdown]
# DSL control structures tutorial
Shows how to use conditional execution, loops, and exit handlers.

%%
"""

from components.hello_world import hello_world
from kfp import dsl  # pylint: disable=wrong-import-order,import-error


@dsl.pipeline(
    name="Test Pipeline",
    description="A simple test pipeline",
    display_name="Test Pipeline",
)
def test_pipeline(recipient: str) -> str:
    """
    A simple test pipeline that says hello to the recipient
    """
    hello_task = hello_world(name=recipient)

    return hello_task.output  # pylint: disable=no-member
