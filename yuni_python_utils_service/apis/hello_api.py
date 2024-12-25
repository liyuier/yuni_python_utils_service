from ninja import NinjaAPI

from yuni_python_utils_service.schema.schema import ResponseSchema
from yuni_python_utils_service.service.hello import hello_service

api = NinjaAPI()


@api.get("/hello")
def hello(request) -> ResponseSchema:
    return hello_service()
