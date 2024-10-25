import httpx
import os
import asyncio
from PIL import Image
from io import BytesIO


async def get(links, client=None):
    pass


async def download_image(client, url):
    response = await client.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        log.error(f"下载失败: {url}")
        raise Exception
        return None


def copy_local_image(local_path):
    return Image.open(local_path).convert("RPGA")


async def process_link(client, link):
    if os.path.isfile(link):
        return copy_local_image(link)
    else:
        return await download_image(client, link)


async def get_imgs(links: list[str], client: httpx.AsyncClient = None):
    """批量下载图片

    Args:
        links (list[str]): url list
        client (httpx.AsyncClient, None): 自定义client，用于代理之类的. Defaults to None.

    Returns:
        list: 图片列表
    """
    images = []

    # 如果没有传入client，则创建一个新的
    if client is None:
        client = httpx.AsyncClient()
        need_close = True
    else:
        need_close = False

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


# 使用示例
# 单张下载
# images = asyncio.run(download_images('https://example.com/image.jpg'))

# 批量下载
# images = asyncio.run(download_images(['https://example.com/image1.jpg', 'path/to/local/image.jpg']))

if __name__ == "__main__":

    # 示例用法
    print(__name__)  # 输出
