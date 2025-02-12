import asyncio
from naotool.img import _get_imgs


async def test():
    images = await _get_imgs(
        [
            "https://avatars.githubusercontent.com/u/53679884",
            "https://avatars.githubusercontent.com/u/53679884",
        ]
    )
    images[0].save("tmp.jpg", format="JPEG")


if __name__ == "__main__":
    images = asyncio.run(test())
