from naotool.deco import fun_filter


if __name__ == "__main__":
    # 示例用法1 替换'key'为 None
    func1 = fun_filter(lambda x: x != "key")
    s = func1("key")
    print(f"s={s}")

    # 示例2 替换'key'为 'other'
    func2 = fun_filter(other="other")(lambda x: x != "key")
    s2 = func2("key")
    print(f"s2={s2}")

    # 示例3 替换'key'为 x + "word"
    @fun_filter(ext_func=lambda x: x + "word")
    def func3(x: str):
        return x != "key"

    s3 = func3("key")
    print(f"s3={s3}")
