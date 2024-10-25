import os
import asyncio
from PIL import Image
from io import BytesIO

from httpx import AsyncClient

from naotool.exception import ImageGetError


async def get(links, client=None):
    pass


async def download_image(client: AsyncClient, url: str):

    try:
        response = await client.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content)).convert("RPGA")
        raise ImageGetError(link=url)
    except Exception:
        raise


async def open_local_img(local_path) -> Image.Image:
    return Image.open(local_path).convert("RPGA")


async def process_link(client, link) -> Image.Image:
    if os.path.isfile(link):
        return await open_local_img(link)
    else:
        return await download_image(client, link)


async def get_img(
    links: list[str] | str, client: AsyncClient = None
) -> list[Image.Image]:
    """批量下载图片

    Args:
        links (list[str]): url list
        client (httpx.AsyncClient, None): 自定义client用于代理等等, 默认不使用代理.

    Returns:
        list: 图片列表
    """
    images = []
    # 处理client
    if client is None:
        client = AsyncClient(trust_env=False, proxies=None)
        need_close = True
    else:
        need_close = False
    # 分类处理，批量还是单个
    try:
        if isinstance(links, str):

            image = await process_link(client, links)
            if image:
                images.append(image)
        elif isinstance(links, list):
            tasks = [process_link(client, link) for link in links]
            downloaded_images = await asyncio.gather(*tasks)
            images.extend(filter(None, downloaded_images))
    finally:
        if need_close:
            await client.aclose()

    return images


if __name__ == "__main__":
    images = asyncio.run(get_imgs()("https://example.com/image.jpg"))
    images = asyncio.run(
        get_imgs(["https://example.com/image1.jpg", "path/to/local/image.jpg"])
    )
