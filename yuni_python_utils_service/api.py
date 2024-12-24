from ninja import NinjaAPI

from .service.hello import hello_service

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    # return hello_service()
    return hello_service()
