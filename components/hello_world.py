from kfp import dsl


@dsl.component(base_image="python:3.11")
def hello_world(name: str) -> str:
    hello_text = f"Hello, {name}!"
    print(hello_text)

    return hello_text


@dsl.component(base_image="python:3.11")
def hello_world_docker():
    return dsl.ContainerOp(
        name="Hello World",
        image="alpine:3.6",
        command=["echo", "Hello, World!"],
    )
