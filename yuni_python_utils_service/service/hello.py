from ..schema.schema import ResponseSchema


def hello_service():
    return ResponseSchema().ok({
        "hello": "Hello, Yuni!"
    })
