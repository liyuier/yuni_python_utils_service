from yuni_python_utils_service.schema.plugin_schema import GetPluginsPicInfoSchema


def draw_plugins_info(schema: GetPluginsPicInfoSchema):
    print(str(schema))
    return {"image": "ok"}
