#! --*-- coding:utf-8 --*--

__author__ = 'sm'

import os
import sys
import logging
import logging.handlers

from singleton import Singleton


LOGGINS_PATH = os.path.dirname(os.path.abspath(__file__))


class StdioOnnaStick(object):
    """
    Class that pretends to be stdout/err, and turns writes into log messages.

    @ivar isError: boolean indicating whether this is stderr, in which cases
                   log messages will be logged as errors.

    @ivar encoding: unicode encoding used to encode any unicode strings
                    written to this object.
    """

    closed = 0
    softspace = 0
    mode = 'wb'
    name = '<stdio (log)>'

    def __init__(self, logging, isError=0, encoding=None):
        self.logging = logging
        self.isError = isError
        if encoding is None:
            encoding = sys.getdefaultencoding()
        self.encoding = encoding
        self.buf = ''

    def close(self):
        pass

    def fileno(self):
        return -1

    def flush(self):
        pass

    def read(self):
        raise IOError("can't read from the log!")

    readline = read
    readlines = read
    seek = read
    tell = read

    def write(self, data):
        if isinstance(data, unicode):
            data = data.encode(self.encoding)
        d = (self.buf + data).split('\n')
        self.buf = d[-1]
        messages = d[0:-1]
        for message in messages:
            if self.isError:
                self.logging.error(message)
            else:
                self.logging.info(message)

    def writelines(self, lines):
        for line in lines:
            if isinstance(line, unicode):
                line = line.encode(self.encoding)
            if self.isError:
                self.logging.error(line)
            else:
                self.logging.info(line)


class BaseLoggingUtil(object):

    def __init__(self, path, level, propagate=1, setStdout=0):
        pass

    def add_msg(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass

    def debug(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass


class LoggingUtil(BaseLoggingUtil):
    """ 日志工具类

    """
    formatter = logging.Formatter('[%(asctime)s] %(pathname)s[%(lineno)d] %(levelname)s %(message)s')

    def __init__(self, path, level, propagate=1, setStdout=0):
        """

        :param path: 路径
        :param level: 级别
        :param propagate: propagate=1是输出日志，同时消息往更高级别的地方传递
        :param setStdout: 设置sys.stdout和sys.stderr日志输出
        :return:
        """
        super(LoggingUtil, self).__init__(path, level, propagate=propagate)
        self.full_path = self.generate_full_path(path)
        self.file_path = os.path.dirname(self.full_path)
        self.file_name = os.path.basename(self.full_path)
        self.check_path()
        self.logger = logging.getLogger(path)
        self.logger.propagate = propagate
        self.fhandler = None
        self.set_level(level)

        if setStdout:
            self._stdout = sys.stdout
            self._stderr = sys.stderr
            sys.stdout = StdioOnnaStick(self, 0, getattr(sys.stdout, "encoding", None))
            sys.stderr = StdioOnnaStick(self, 1, getattr(sys.stderr, "encoding", None))
        else:
            self._stdout = None
            self._stderr = None

    def generate_full_path(self, path):
        """ 文件的路径

        :param path:
        :return:
        """
        if path.startswith('/'):
            return path
        else:
            return os.path.join(LOGGINS_PATH, '..', '..', 'logs', path)

    def check_path(self):
        """ 检查路径

        :return:
        """
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def set_level(self, level):
        if self.logger.level != level:
            if self.fhandler:
                self.fhandler.setLevel(level)
            self.logger.setLevel(level)

    def set_stream_handler(self):
        """ 设置StreamHandler

        :return:
        """
        if self.fhandler:
            self.logger.removeHandler(self.fhandler)

        if self._stderr:
            self.fhandler = logging.StreamHandler(stream=self._stderr)
        else:
            self.fhandler = logging.StreamHandler()
        self.fhandler.setFormatter(self.formatter)
        self.fhandler.setLevel(self.logger.level)
        self.logger.addHandler(self.fhandler)

    def set_file_handler(self, full_path=None):
        """ 设置FileHandler

        :param full_path:
        :return:
        """
        full_path = self.generate_full_path(full_path) if full_path is not None else self.full_path

        if self.fhandler:
            pass
            # self.logger.removeHandler(self.fhandler)

        dir_path = os.path.dirname(os.path.abspath(full_path))
        os.system("""[ ! -d '%s' ] && mkdir -p %s""" % (dir_path, dir_path))

        self.fhandler = logging.FileHandler(full_path)
        self.fhandler.setFormatter(self.formatter)
        self.fhandler.setLevel(self.logger.level)
        self.logger.addHandler(self.fhandler)

    def set_rotating_file_handler(self, full_path=None):
        """ 设置RotatingFileHandler

        :param full_path:
        :return:
        """
        full_path = self.generate_full_path(full_path) if full_path is not None else self.full_path

        if self.fhandler:
            self.logger.removeHandler(self.fhandler)

        self.fhandler = logging.handlers.RotatingFileHandler(full_path, maxBytes=1024 * 1024 * 200, backupCount=10)
        self.fhandler.setFormatter(self.formatter)
        self.fhandler.setLevel(self.logger.level)
        self.logger.addHandler(self.fhandler)

    def add_msg(self, sort, msg, *args, **kwargs):
        """ 添加信息

        :param sort: 类型
        :param msg: 信息
        :return:
        """
        if isinstance(sort, int):
            name = logging._levelNames.get(sort)
        else:
            name = sort
        name = name.lower()
        if hasattr(self.logger, name):
            func = getattr(self.logger, name)
            func(msg, *args, **kwargs)
            return True
        else:
            return False

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)


class PrintLoggingUtil(LoggingUtil):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')

    def __init__(self, path, level, propagate=1, setStdout=0):
        """

        :param path: 路径
        :param level: 级别
        :param propagate: propagate=1是输出日志，同时消息往更高级别的地方传递
        :param setStdout:
        :return:
        """
        super(PrintLoggingUtil, self).__init__(path, level, propagate=propagate, setStdout=setStdout)
        self.set_stream_handler()

    # def info(self, msg, *args, **kwargs):
    #     self.logger.info('[INFO] %s' % msg, *args, **kwargs)
    #
    # def debug(self, msg, *args, **kwargs):
    #     self.logger.debug('[DEBUG] %s' % msg, *args, **kwargs)
    #
    # def error(self, msg, *args, **kwargs):
    #     self.logger.error('[ERROR] %s' % msg, *args, **kwargs)

class StatLoggingUtil(LoggingUtil):
    formatter = logging.Formatter('%(message)s')

    def __init__(self, path, level, propagate=1, setStdout=0):
        """

        :param path: 路径
        :param level: 级别
        :param propagate: propagate=1是输出日志，同时消息往更高级别的地方传递
        :param setStdout:
        :return:
        """
        super(StatLoggingUtil, self).__init__(path, level, propagate=propagate, setStdout=setStdout)
        self.set_file_handler()


class InfoLoggingUtil(LoggingUtil):
    """
    玩家数据
    """
    formatter = logging.Formatter('%(message)s')

    def __init__(self, path, level, propagate=1, setStdout=0):
        """

        :param path: 路径
        :param level: 级别
        :param propagate: propagate=1是输出日志，同时消息往更高级别的地方传递
        :param setStdout:
        :return:
        """
        super(InfoLoggingUtil, self).__init__(path, level, propagate=propagate, setStdout=setStdout)
        self.set_file_handler()


class LongActionLoggingUtil(LoggingUtil):
    """ 长连动作记录

    """
    formatter = logging.Formatter('%(asctime)s %(message)s')

    def __init__(self, path, level, propagate=1, setStdout=0):
        """

        :param path: 路径
        :param level: 级别
        :param propagate: propagate=1是输出日志，同时消息往更高级别的地方传递
        :param setStdout:
        :return:
        """
        super(LongActionLoggingUtil, self).__init__(path, level, propagate=propagate, setStdout=setStdout)
        self.set_rotating_file_handler()


class LoggingCache(object):
    """ 日志缓存类

    """
    __metaclass__ = Singleton

    logging_pool = {}

    @classmethod
    def get_logging_with_filename(cls, path, logging_class=BaseLoggingUtil, level=logging.INFO, **kwargs):
        """ 通过文件名获取logging

        :param path:
        :param logging_class:
        :param level:
        :return:
        """
        logging_util = cls.logging_pool.get(path)
        if logging_util:
            return logging_util

        logging_util = logging_class(path, level, **kwargs)

        cls.logging_pool[path] = logging_util

        return logging_util


def get_log(path=None, logging_class=BaseLoggingUtil, level=logging.INFO, **kwargs):
    if path is None:
        return LoggingCache.get_logging_with_filename('default', logging_class=PrintLoggingUtil,
                                                      level=level, propagate=0, setStdout=1, **kwargs)
    else:
        return LoggingCache.get_logging_with_filename(path, logging_class=logging_class, level=level, **kwargs)


if __name__ == '__main__':
    # ul = LoggingUtil('test', 'test', 10, setStdout=0)
    # outfile = StdioOnnaStick(ul, 0, getattr(sys.stdout, "encoding", None))
    # sys.stdout = outfile
    logger = LoggingCache.get_logging_with_filename('test/test.log', level=logging.DEBUG, setStdout=1)
    logger.info('info hello')
    print 'print hello'
    logger.info('info hello')
    logger.debug('info debug')
