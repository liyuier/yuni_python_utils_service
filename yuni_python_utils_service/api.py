from ninja import NinjaAPI

from .schema.schema import ResponseSchema
from .service.hello import hello_service

api = NinjaAPI()


@api.get("/hello")
def hello(request) -> ResponseSchema:
    return hello_service()
