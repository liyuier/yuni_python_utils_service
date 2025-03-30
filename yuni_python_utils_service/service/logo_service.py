import asyncio
import time
from io import BytesIO

from PIL import Image, ImageOps
from playwright.async_api import Page
from playwright.sync_api import Playwright, sync_playwright

from yuni_python_utils_service.schema.logo_schema import BlueArchiveLogoSchema
from yuni_python_utils_service.settings import TEMPLATE_DIR, PIC_DIR
from yuni_python_utils_service.utils.tencent_cos_visit import upload_file_byte
from yuni_python_utils_service.utils.wright_player import play_page


def write_test_logo(img_bytes: bytes):
    logo_path = PIC_DIR / "test.png"
    print(logo_path)
    with open(str(logo_path), 'wb') as img:
        img.write(img_bytes)
        print("Test logo written.")


def write_test_html(html: str):
    template_path = TEMPLATE_DIR / "test.html"
    print(template_path)
    with open(str(template_path), 'w',  encoding='utf-8') as f:
        f.write(html)
        print("Test html written.")


def screenshot_ba_logo(schema: BlueArchiveLogoSchema):
    async def shot(page: Page):
        # 访问本地部署的服务
        await page.goto('http://localhost:5174/')
        await page.click("input#textL")
        await page.press("input#textL", 'Control+A')
        await page.press("input#textL", 'Backspace')
        await page.type("input#textL", schema.textl)
        await page.click("input#textR")
        await page.press("input#textR", 'Control+A')
        await page.press("input#textR", 'Backspace')
        await page.type("input#textR", schema.textr)
        await page.locator("html").click()
        await asyncio.sleep(0.5)
        # 截取画面
        container_div = page.locator('canvas#canvas')
        screenshot_bytes = await container_div.screenshot(path=None)
        print("load end")
        return screenshot_bytes
    return shot


# 裁剪图片两端空白部分
def auto_crop_with_margin(image_bytes, margin=10, background_color=None):
    # 将字节数据加载到 BytesIO 对象中
    image_stream = BytesIO(image_bytes)

    # 打开图像文件
    image = Image.open(image_stream).convert('RGBA')

    # 如果提供了背景颜色，则创建一个与图像大小相同的背景图像，并将原图与其合并。
    if background_color:
        bg = Image.new('RGBA', image.size, background_color)
        image = Image.alpha_composite(bg, image)
        image = image.convert('RGB')  # 将带有透明度的图像转换为RGB模式

    # 转换为灰度图像，并应用阈值处理，将图像二值化（黑白）
    bw_image = image.convert('L')  # 转换为灰度图像
    bw_image = bw_image.point(lambda x: 0 if x < 245 else 255, '1')  # 二值化

    # 获取图像的边界框，即非白色区域的最小矩形
    bbox = bw_image.getbbox()

    if bbox:
        # 添加外边距
        left, upper, right, lower = bbox
        width, height = image.size

        # 确保新的边界不会超出图像的实际尺寸
        left = max(0, left - margin)
        upper = max(0, upper - margin)
        right = min(width, right + margin)
        lower = min(height, lower + margin)

        # 使用调整后的边界框裁剪原始图像
        cropped_image = image.crop((left, upper, right, lower))

        # 将裁剪后的图像保存到一个新的 BytesIO 对象中
        output_stream = BytesIO()
        cropped_image.save(output_stream, format='PNG')  # 你可以根据需要更改格式
        output_stream.seek(0)  # 确保读取指针位于开始位置

        return output_stream.getvalue()  # 返回裁剪后的图像字节数据
    else:
        print("图像完全是空白的或无法检测到内容")
        return None


def draw_ba_logo(schema: BlueArchiveLogoSchema):
    print(schema)
    shot = screenshot_ba_logo(schema)
    screenshot_bytes = asyncio.run(play_page(shot))
    screenshot_bytes_tailed = auto_crop_with_margin(screenshot_bytes, margin=20, background_color=(255, 255, 255))
    # 调用对象存储
    file_url = upload_file_byte(file_byte=screenshot_bytes_tailed, file_name=f"ba_logo_{schema.textl + '_' + schema.textr}.png")
    # 返回 url
    return {"image": file_url}
