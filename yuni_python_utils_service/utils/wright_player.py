from typing import Callable, Any
from playwright.async_api import async_playwright, Page


async def play_page(operator: Callable[[Page], Any]):
    print("play_page enter")
    result = None
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        result = await operator(page)
        await browser.close()
    print("play_page end")
    return result
