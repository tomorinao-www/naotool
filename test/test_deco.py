from naotool.deco import compat_arg_error


@compat_arg_error
def f():
    pass


f(1, 2, 3, a=1)
print("ok!")
