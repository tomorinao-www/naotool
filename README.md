<div align="center">
  <a href="https://github.com/tomorinao-www">
    <img src="https://avatars.githubusercontent.com/u/53679884" 
    width="300" alt="NaoLogo" 
    style="border-radius: 50%; object-fit: cover;">
  </a>
  <br>

</div>

<div align="center">

# naotool

_✨ 🍬A packge of utils or tools keeps Python sweet. 让 py 保持甜甜的 ✨_

<a href="https://github.com/tomorinao-www/naotool/blob/main/LICENSE">
  <img src="https://img.shields.io/github/license/tomorinao-www/naotool.svg" alt="license:MIT">
</a>
<a href="https://pypi.python.org/pypi/naotool">
  <img src="https://img.shields.io/pypi/v/naotool.svg" alt="pypi">
</a>
<a hred="https://www.python.org/">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python:3.10+">
</a>

</div>

# naotool

🍬A packge of utils or tools keeps Python sweet.

# 快速上手

```sh
pip install naotool
```

# 最佳实践

```python
from naotool import deco

@deco.compat_arg_error
def f():
    pass
```

# tools

| module    | example         | description |
| --------- | --------------- | ----------- |
| img       | get_img()       | 图片相关    |
| deco      | @deco.compat_arg_error | 装饰器      |
| exception | NOException     | 异常        |
