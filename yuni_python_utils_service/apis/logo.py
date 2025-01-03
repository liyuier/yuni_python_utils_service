from ninja import NinjaAPI

from yuni_python_utils_service.apis.plugin_api import responseSchema
from yuni_python_utils_service.schema.logo_schema import BlueArchiveLogoSchema
from yuni_python_utils_service.schema.schema import ResponseSchema
from yuni_python_utils_service.service.logo_service import draw_ba_logo

logo_api = NinjaAPI()


@logo_api.post("/ba")
def ba_logo(request, schema: BlueArchiveLogoSchema) -> ResponseSchema:
    return responseSchema.ok(draw_ba_logo(schema))
