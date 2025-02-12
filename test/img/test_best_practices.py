# 脚本任务: 将 `.jpg` 图片的文件重命名为 `{md5}.jpg`
import asyncio
import os
from pathlib import Path
from PIL import Image
import naotool as nt

Image.MAX_IMAGE_PIXELS = None
img_dir = Path(r"../../imgs")
img_name_list = filter(lambda x: x.endswith(".jpg"), os.listdir(str(img_dir)))
path_list = [img_dir / name for name in img_name_list]


async def rename_image(src: Path):
    try:
        md5 = nt.img_md5hex(await nt.get_imgs(str(src)))
        new_path = img_dir / f"{md5}{src.suffix}"
        os.rename(src, new_path)
    except Exception as e:
        print(f"Failed to process {src}: {e}")


async def main():
    await asyncio.gather(*(rename_image(src) for src in path_list))


asyncio.run(main())
