from ninja import NinjaAPI

from yuni_python_utils_service.schema.schema import ResponseSchema
from ..service.plugin_service import draw_plugins_info, draw_plugin_detail
from ..schema.plugin_schema import GetPluginsPicInfoSchema, GetPluginDetailInfoSchema

plugin_api = NinjaAPI()

responseSchema = ResponseSchema()


@plugin_api.post("/list")
def list_pic(request, schema: GetPluginsPicInfoSchema) -> ResponseSchema:
    return responseSchema.ok(draw_plugins_info(schema))


@plugin_api.post("/detail")
def detail_pic(request, schema: GetPluginDetailInfoSchema) -> ResponseSchema:
    return responseSchema.ok(draw_plugin_detail(schema))