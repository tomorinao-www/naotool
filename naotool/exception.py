from abc import ABC, abstractmethod


class BaseError(Exception, ABC):
    """自定义异常基类，通用抽象接口"""

    @abstractmethod
    def get_error_code(self) -> int:
        """获取错误代码，子类必须实现此方法"""
        pass

    def __init__(self, message: str = None):
        # self属性初始化
        self.message = message or "发生了一般错误"
        # super父类初始化
        super().__init__(self.message)
        # 使用子类实现的抽象方法
        ec = self.get_error_code()
        print((ec))

    def __str__(self) -> str:
        return f"{self.message} (错误代码: {self.get_error_code()})"


class ImageGetError(BaseError):
    """自定义异常类，用于表示图片获取失败的情况。"""

    def __init__(self, link, msg="图片获取失败"):
        self.link = link
        self.msg = msg
        self.code = 114514
        super().__init__(f"{msg} === {link}")

    def get_error_code(self) -> int:
        """获取错误代码，具体实现可以根据需要定义。"""
        return self.code

    def __str__(self) -> str:
        return f"{self.msg}. link={self.link} (错误代码: {self.get_error_code()})"


ImageGetError("http://114514")
