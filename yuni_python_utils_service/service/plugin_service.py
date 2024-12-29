import asyncio
from operator import attrgetter
from typing import Callable, Any


from playwright.async_api import async_playwright, Page
from yuni_python_utils_service.schema.plugin_schema import GetPluginsPicInfoSchema
from yuni_python_utils_service.settings import TEMPLATE_DIR, PIC_DIR
from ..utils.tencent_cos_visit import upload_file_byte
from ..utils.yuni_render import get_template
from ..utils.wright_player import play_page


def screenshot_div(html: str, div_selector: str, output_img_path: str):
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
    # 渲染 html
    template = get_template("plugin_info_list.html")
    # 将字典转换为列表并按 id 排序
    plugins_info_list = sorted(schema.plugins_info.values(), key=attrgetter('id'))
    # 渲染模板并传入上下文数据
    rendered_html = template.render(plugins_info=plugins_info_list)
    # 转为图片
    output_path = PIC_DIR / 'plugin_infos.png'
    shot = screenshot_div(rendered_html, 'div.container', str(output_path))
    screenshot_bytes = asyncio.run(play_page(shot))
    # 调用对象存储
    file_url = upload_file_byte(file_byte=screenshot_bytes, file_name="plugin_infos.png")
    print(file_url)
    # 返回 url
    return {"image": file_url}
