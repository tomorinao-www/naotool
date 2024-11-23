# MIT License

# Copyright (c) 2024 友利奈绪-勿忘我

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .__version__ import __description__, __title__, __version__
from .cls import copy_attr
from .deco import compat_arg_error, fun_filter
from .httpn import AutoCloseAsyncClient
from .img import (
    run_get_imgs,
    get_imgs,
    img_md5hex,
    add_top_border,
    remove_bottom_border,
    crop_to_max_height,
)
from .strs import tight
from .x import Xpost, get_xposts
from .exception import BaseError, NOException

__all__ = [
    # Package metadata
    "__description__",
    "__title__",
    "__version__",
    # cls
    "copy_attr",
    # deco
    "compat_arg_error",
    "fun_filter",
    # img
    "run_get_imgs",
    "get_imgs",
    "img_md5hex",
    "add_top_border",
    "remove_bottom_border",
    "crop_to_max_height",
    # httpn
    "AutoCloseAsyncClient",
    # strs
    "tight",
    # exception
    "BaseError",
    "NOException",
    # Xpost utilities
    "Xpost",
    "get_xposts",
]


__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        setattr(__locals[__name], "__module__", "naotool")  # noqa
