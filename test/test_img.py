import asyncio
from naotool.img import get


async def test():
    images = await get(
        [
            "https://avatars.githubusercontent.com/u/53679884",
            "https://avatars.githubusercontent.com/u/53679884",
        ]
    )
    images[0].save("tmp.jpg", format="JPEG")


if __name__ == "__main__":
    images = asyncio.run(test())
