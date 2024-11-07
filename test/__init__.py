import inspect
from naotool import deco

# 动态导入模块
_module = __import__(__name__)

# 使用导入的模块
print(_module)  # 输出: 4.0

print(dir(__name__))


def decorate_all_functions(module):
    if not inspect.ismodule(module):
        return
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and not name.startswith("__"):
            decorated_func = deco.compat_arg_error(obj)
            setattr(module, name, decorated_func)


# 装饰所有函数
decorate_all_functions(_module)
# 获取函数的源码
source_code = inspect.getsource(decorate_all_functions)

print(source_code)

decorate_all_functions(1, 2, 3, 4)
print("容错ok")
