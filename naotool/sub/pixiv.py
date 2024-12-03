import asyncio
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
import traceback

from PIL import Image
from playwright.async_api import async_playwright
from playwright.async_api._generated import Page, Locator

from .xpostx import Xpost
from ..img.op import add_top_border


class Ppost(Xpost):
    pid: str


async def get_pposts(
    user_data_dir: str | Path,
    sub_ids: list[str],
    *,
    limit: int = 3,
    last_time: float = 0.0,
    img_dir: str = None,
    local_timezone: timezone = timezone(timedelta(hours=8)),
    wait_time: int = 3,
    **playwright_args,
) -> list[Ppost]:
    _cache: dict[str, list[Xpost]] = {}
    async with async_playwright() as ap:
        # 0.init
        browser_context = await ap.chromium.launch_persistent_context(
            # 指定本机用户缓存地址
            user_data_dir=user_data_dir,
            # 指定本机google客户端exe的路径
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            # 要想通过这个下载文件这个必然要开  默认是False
            accept_downloads=True,
            # 设置不是无头模式
            headless=False,
            bypass_csp=True,
            slow_mo=10,
            # 跳过检测
            args=[
                "--disable-blink-features=AutomationControlled",
                "--remote-debugging-port=9222",
            ],
        )
        page = await browser_context.new_page()
        res = []
        for sub_id in sub_ids:
            try:
                if sub_id in _cache:
                    ps = _cache[sub_id]
                else:
                    ps = await _get_sub_posts(
                        page=page,
                        sub_id=sub_id,
                        limit=limit,
                        last_time=last_time,
                        img_dir=img_dir,
                        local_timezone=local_timezone,
                        wait_time=wait_time,
                    )
                    _cache[sub_id] = ps
                res += ps
            except Exception as e:
                print(f"error: fetch {sub_id} error!")
                print(e)
                traceback.print_exc()
        return res


async def _get_sub_posts(
    page: Page,
    sub_id: str = "",
    limit: int = 3,
    last_time: float = 0.0,
    last_id: str = "",
    img_dir: str = None,
    local_timezone: timezone = timezone(timedelta(hours=8)),
    wait_time: int = 3,
) -> list[Xpost]:
    # 1.goto
    page_url = "https://www.pixiv.net" + (f"/users/{sub_id}" if sub_id else "")
    await page.goto(page_url)
    await asyncio.sleep(wait_time)  # 给页面加载时间
    await page.wait_for_load_state()
    await asyncio.sleep(wait_time)  # 给页面加载时间
    if sub_id == "":
        await page.goto("https://www.pixiv.net/bookmark_new_illust.php?p=1")
        sub_tab = page.locator(
            "xpath=//main/div/div/div/div[1]/div/div[1]"
            "/div[1]/div/nav/div/div[2]/div/div[1]"
        )
        await sub_tab.click()
    # 2.page down
    for _ in range(2):
        await page.keyboard.press("PageDown")
        await asyncio.sleep(wait_time)  # 给页面加载时间
    # 3.get key Locator by xpath
    key_loc = page.locator("xpath=//a[@data-gtm-value]")
    # 4.for url list
    res: list[Ppost] = []
    for k_loc in await key_loc.all():
        pp = Ppost()
        # last_id
        pp.id = await k_loc.get_attribute("data-gtm-value")
        pp.id = str(pp.id)
        if pp.id == str(last_id):
            continue
        # click()
        pp.sub_id = sub_id
        await k_loc.click()
        await asyncio.sleep(wait_time)  # wait
        await page.wait_for_load_state()  # wait
        await asyncio.sleep(wait_time)  # wait
        pp.url = page.url

        # date_time => 2024-11-21T15:40:00.000Z
        time_loc = page.locator("xpath=//time")
        utc_datetime_s = await time_loc.get_attribute("datetime")
        if utc_datetime_s:
            utc_datetime = datetime.strptime(
                utc_datetime_s,
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
            pp.timestamp = utc_datetime.timestamp()
            if pp.timestamp <= last_time:  # out time
                continue
            pp.date_time = utc_datetime.astimezone(local_timezone)

        # screenshot
        sections: Locator = page.locator("xpath=//main/section")
        if sections:
            section = sections.first
            pp.screenshot = await section.screenshot(type="jpeg")
            img = add_top_border(Image.open(BytesIO(pp.screenshot)), 200)
            if img_dir:
                img_path = Path(img_dir) / f"{pp.id}.jpg"
                img.save(str(img_path), format="JPEG")
        # text
        figcaption: Locator = page.locator("xpath=//figcaption")
        figcaption = figcaption.first
        if text := await figcaption.text_content():
            pp.text = text
        # img_urls
        pp.img_urls = []
        try:  # if has a button
            page.set_default_timeout(3000)
            all_button = section.locator(
                "xpath=//main/section/div[1]/div/div[5]/div/div[2]/button"
            )
            await all_button.click()
            asyncio.sleep(wait_time)
            await page.wait_for_load_state()
            asyncio.sleep(wait_time)
        except Exception as e:
            print(e)
            print("no button")
        img_list = section.locator(
            "xpath=//main/section//figure//a[@href] | //a[@data-page]"
        )
        for img in await img_list.all():
            img_url = await img.get_attribute("href")
            if not img_url:
                img_url = await img.get_attribute("href")
            if (
                not img_url
                or not (
                    img_url.startswith("https://i.pximg.net/img-original/")
                    or img_url.startswith("https://pbs.twimg.com/card_img")
                    or pp.id in img_url
                )
                or img_url in pp.img_urls
            ):
                continue
            elif (pack := img_url.split("?")) and len(pack) > 1:
                # ps = pack[1].split("&")
                # params = "&".join([p for p in ps if "format=" in p])
                # img_url = f"{pack[0]}?{params}"
                img_url = img_url.replace("name=medium", "")
                img_url = img_url.replace("name=small", "name=medium")
            pp.img_urls.append(img_url)
        # goback
        await page.go_back()
        # res
        res.append(pp)
        if len(res) >= limit:
            break
    res.sort(key=lambda x: x.timestamp)
    return res
