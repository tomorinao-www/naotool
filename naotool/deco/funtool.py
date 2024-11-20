from functools import wraps
from typing import Callable


def fun_filter(
    func: Callable = None,
    other: object = None,
    ext_func: Callable = None,
) -> Callable:
    """这个装饰器接收一个函数func用于判断入参x是否要过滤,

    返回一个函数:
    仍然接收一个变量x,
    如果func(x)==True 返回x;
    否则返回other, 或者ext_func(x)
    注意：这个函数并不过滤集合的元素，只能处理单个变量

    Args:
        func (Callable, optional): 函数func用于判断是否要过滤
        other (object, optional): 过滤后替换为other
            Defaults to None.
        ext_func (Callable, optional): 过滤后替换为ext_func(x)
            Defaults to None.

    Returns:
        Callable: 装饰后的函数
    """

    if func is None:
        return lambda f: fun_filter(f, other, ext_func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        x = args[0]
        if func(*args, **kwargs):
            return x
        else:
            if ext_func:
                return ext_func(x)
            else:
                return other

    return wrapper


if __name__ == "__main__":
    # 示例用法1 替换'key'为 None
    func1 = fun_filter(lambda x: x not in "key")
    s = func1("key")
    print(f"s={s}")

    # 示例2 替换'key'为 'other'
    func2 = fun_filter(other="other")(lambda x: x not in "key")
    s2 = func2("key")
    print(f"s2={s2}")

    # 示例3 替换'key'为 x + "word"
    @fun_filter(ext_func=lambda x: x + "word")
    def func3(x: str):
        return x not in "key"

    s3 = func3("key")
    print(f"s3={s3}")
