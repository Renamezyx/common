import logging
import datetime
import os

from config import get_project_root


class LoggerHandler(logging.Logger):
    _instance = None
    _initialized = False

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    # 初始化 Logger
    def __init__(self,
                 name='root',
                 logger_level='DEBUG',
                 file=None,
                 logger_format=" [%(asctime)s]  %(levelname)s %(filename)s [ line:%(lineno)d ] %(message)s"
                 ):
        if self._initialized:
            pass
        # 1、设置logger收集器，继承logging.Logger
        super().__init__(name)

        # 2、设置日志收集器level级别
        self.setLevel(logger_level)

        # 5、设置 handler 格式
        fmt = logging.Formatter(logger_format)

        # 3、设置日志处理器

        # 如果传递了文件，就会输出到file文件中
        if file:
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            file_handler = logging.FileHandler(file)
            # 4、设置 file_handler 级别
            file_handler.setLevel(logger_level)
            # 6、设置handler格式
            file_handler.setFormatter(fmt)
            # 7、添加handler
            self.addHandler(file_handler)

        # 默认都输出到控制台
        stream_handler = logging.StreamHandler()
        # 4、设置 stream_handler 级别
        stream_handler.setLevel(logger_level)
        # 6、设置handler格式
        stream_handler.setFormatter(fmt)
        # 7、添加handler
        self.addHandler(stream_handler)
        if not os.path.exists(os.path.join(get_project_root(), 'logs')):
            os.makedirs(os.path.join(get_project_root(), 'logs'))

        self._initialized = True


__log_file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
logger = LoggerHandler(name='my_app_logger', logger_level='DEBUG',
                       file=f"{os.path.join(get_project_root(), 'logs', __log_file_name)}.log")
