from ninja import NinjaAPI

plugin_api = NinjaAPI()


@plugin_api.get("/list")
def list_pic(request):
    return "pic list"
