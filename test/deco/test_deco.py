import naotool.deco as deco


@compat_arg_error
def f(a: int = 0) -> int:
    return a



f(1, 2, 3, a=1)
print("ok!")
