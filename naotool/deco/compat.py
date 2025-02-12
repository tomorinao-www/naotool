import inspect
from inspect import Parameter
from collections.abc import Callable
from .deco import decodeco


@decodeco
def compat_arg_error(
    func: Callable = None,
    rm_None: bool = True,
    func_args: tuple = None,
    func_kwargs: dict = None,
) -> Callable:
    """这个装饰器使得函数在接收错误的参数时，仍然正常执行，消除异常。（但不保证完全正确）
    正常情况下，在调用函数时传入了错误参数，Python 会抛出 TypeError 异常。有2种情况：
    1.位置参数：如果你传入了超过函数定义的参数数量，或者传入了一个不接受的位置参数，Python 会报错。
    2.关键字参数：如果你传入了不在函数定义中的关键字参数，Python 也会抛出 TypeError。

    Args:
        func (Callable): 被装饰的函数
        rm_None(bool) : 是否移除为None的参数. (default True)
    Returns:
        Callable: 装饰后的函数
    """

    signature = inspect.signature(func)
    params = signature.parameters
    # 1.过滤掉未定义的关键字参数, 以及None(当rm_None为True)
    filtered_kwargs = {
        k: v
        for k, v in func_kwargs.items()
        if k in params
        and not (rm_None and v is None)
        and (
            params[k].kind
            in {
                Parameter.KEYWORD_ONLY,
                Parameter.VAR_KEYWORD,
                Parameter.POSITIONAL_OR_KEYWORD,
            }
        )
    }

    # 2.位置参数
    func_args_list = list(func_args)
    # 2.1.类型检查，自动类型转换
    # TODO: 完善类型检查，增加参数供调用方选择，默认不再自动类型转换
    for i, (k, v) in enumerate(params.items()):
        if i >= len(func_args):
            break
        true_type = v.annotation
        if true_type is Parameter.empty:
            break
        try:
            func_args_list[i] = true_type(func_args[i])  # 尝试转换
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Warning: argument '{k}' needs type {true_type}, "
                f"but got value {func_args[i]} ({type(func_args[i])}). "
                f"Original error: {e}"
            ) from e
    # 2.2.数量检查，减少多余参数
    position_param_nums = sum(
        1
        for p in params.values()
        if p.kind
        in {
            Parameter.POSITIONAL_ONLY,
            Parameter.POSITIONAL_OR_KEYWORD,
        }
        and p.name not in filtered_kwargs
    )
    if len(func_args_list) > position_param_nums:
        func_args_list = func_args_list[:position_param_nums]

    # 3.正确性检验
    try:
        bound_args = signature.bind(*func_args_list, **filtered_kwargs)
        bound_args.apply_defaults()
    except TypeError as e:
        raise TypeError("Please report this bug!") from e
    return func(*func_args_list, **filtered_kwargs)


if __name__ == "__main__":

    # 示例用法
    @compat_arg_error
    def example_function(a, b, c=10):
        return a + b + c

    result = example_function("6", 1, 2, "9", 9, d="")  # d 参数将被忽略
    print(result)  # 输出

    # 示例用法2
    @compat_arg_error()
    def example_function2(a, b, c=10):
        return a + b + c

    # 测试
    result2 = example_function2("", 1, 2, "9", 9, d="")  # d 参数将被忽略
    print(result2)  # 输出
