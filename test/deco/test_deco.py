import naotool.deco as deco


@deco.decodeco  # Directly call the decorator from root module `nt.`
@deco.compat_arg_error  # Use a submodule(`.deco`) to improve readability and make IDE's syntax prompts more precise
def f():
    pass


f(1, 2, 3, a=1)
print("ok!")
