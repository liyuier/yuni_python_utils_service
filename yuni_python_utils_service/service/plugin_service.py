import asyncio
from operator import attrgetter

from playwright.async_api import Page

from yuni_python_utils_service.schema.plugin_schema import GetPluginsPicInfoSchema, GetPluginDetailInfoSchema
from yuni_python_utils_service.settings import TEMPLATE_DIR
from ..utils.tencent_cos_visit import upload_file_byte
from ..utils.wright_player import play_page
from ..utils.yuni_render import get_template


def write_test_html(html: str):
    template_path = TEMPLATE_DIR / "test.html"
    print(template_path)
    with open(str(template_path), 'w',  encoding='utf-8') as f:
        f.write(html)
        print("Test html written.")


def screenshot_div(html: str, div_selector: str):
    async def shot(page: Page):
        print("load enter")
        # 将 HTML 字符串加载到页面中
        await page.set_content(html)
        # 等待 'container' class 的 <div> 加载完成
        await page.wait_for_selector(div_selector)
        # 对 'container' class 的 <div> 截图
        container_div = page.locator(div_selector)
        screenshot_bytes = await container_div.screenshot(path=None)
        print("load end")
        return screenshot_bytes
    return shot


def draw_plugins_info(schema: GetPluginsPicInfoSchema):
    ## 渲染 html
    template = get_template("plugin_info_list.html")
    # 将字典转换为列表并按 id 排序
    plugins_info_list = sorted(schema.plugins_info.values(), key=attrgetter('id'))
    # 渲染模板并传入上下文数据
    rendered_html = template.render(plugins_info=plugins_info_list)
    # 转为图片
    shot = screenshot_div(rendered_html, 'div.container')
    screenshot_bytes = asyncio.run(play_page(shot))
    # 调用对象存储
    file_url = upload_file_byte(file_byte=screenshot_bytes, file_name="plugin_infos.png")
    print(file_url)
    # 返回 url
    return {"image": file_url}


def draw_plugin_detail(plugin_detail_schema: GetPluginDetailInfoSchema):
    plugin_detail_schema.help = plugin_detail_schema.help.replace("\n", "<br>")
    print(plugin_detail_schema)
    # 渲染 html
    template = get_template("plugin_detail_info.html")
    # 渲染模板并传入上下文数据
    rendered_html = template.render(plugin_detail=plugin_detail_schema)
    shot = screenshot_div(rendered_html, 'div.content')
    screenshot_bytes = asyncio.run(play_page(shot))
    # 调用对象存储
    file_url = upload_file_byte(file_byte=screenshot_bytes, file_name=f"plugin_detail_{plugin_detail_schema.name}.png")
    # 返回 url
    return {"image": file_url}