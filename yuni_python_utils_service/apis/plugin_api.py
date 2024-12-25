from ninja import NinjaAPI

from yuni_python_utils_service.schema.schema import ResponseSchema
from ..service.plugin_service import draw_plugins_info
from ..schema.plugin_schema import GetPluginsPicInfoSchema

plugin_api = NinjaAPI()

responseSchema = ResponseSchema()


@plugin_api.post("/list")
def list_pic(request, schema: GetPluginsPicInfoSchema) -> ResponseSchema:
    return responseSchema.ok(draw_plugins_info(schema))
