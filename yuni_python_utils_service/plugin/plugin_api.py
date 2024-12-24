from ninja import NinjaAPI

from yuni_python_utils_service.schema.schema import ResponseSchema

plugin_api = NinjaAPI()


@plugin_api.get("/list")
def list_pic(request) -> ResponseSchema:
    pass
