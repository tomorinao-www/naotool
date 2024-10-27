import asyncio
import os
from pathlib import Path
from PIL import Image
from naotool.img.op import img_md5hex
from naotool.img import get

Image.MAX_IMAGE_PIXELS = None
img_dir = Path(r"../../imgs/")
img_name_list = filter(lambda x: x.endswith(".jpg"), os.listdir(str(img_dir)))
path_list = [img_dir / name for name in img_name_list]


async def rename_image(src: Path):
    try:
        md5 = img_md5hex(await get(str(src)))
        new_path = img_dir / f"{md5}{src.suffix}"
        os.rename(src, new_path)
    except Exception as e:
        print(f"Failed to process {src}: {e}")


async def main():
    await asyncio.gather(*(rename_image(src) for src in path_list))


asyncio.run(main())
