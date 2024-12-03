import asyncio
from naotool.sub.pixiv import get_pposts


async def test():
    res = await get_pposts(
        user_data_dir=r"C:\Users\tomorinao\AppData\Local\Google\Chrome\User Data",
        sub_ids=["705370"],
        headless=False,
    )
    (print(pp) for pp in res)


async def main():
    await test()


asyncio.run(main())
