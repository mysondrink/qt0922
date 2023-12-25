import pymysql
from PySide2.QtCore import QThread, Signal
import sys
import traceback

from func.infoPage import infoMessage

time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202

class CheckDataBaseThread(QThread):
    # global qmutex
    update_json = Signal(dict)
    update_log = Signal(str)

    """
    @detail 初始化线程，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        sys.excepthook = self.HandleException
        self.working = True
        self.num = 0

    """
    @detail 捕获及输出异常类
    @param excType: 异常类型
    @param excValue: 异常对象
    @param tb: 异常的trace back
    """
    def HandleException(self, excType, excValue, tb):
        sys.__excepthook__(excType, excValue, tb)
        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        self.update_log.emit(err_msg)

    """
    @detail 发送异常信息
    @detail 在正常抛出异常时使用
    @detail 未使用
    """
    def sendException(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.update_log.emit(err_msg)

    """
    @detail 线程运行函数
    @detail 进行数据库的检测
    """
    def run(self):
        try:
            info_msg = "数据库检测中。。。"
            code_msg = succeed_code
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                         charset='utf8')
            if connection.open:
                # qmutex.tryLock(trylock_time)
                self.sleep(time_to_sleep)
                info_msg = "连接数据库成功！"
                code_msg = succeed_code
                status_msg = self.currentThread()
                # qmutex.unlock()
            else:
                # qmutex.tryLock(trylock_time)
                self.sleep(time_to_sleep)
                info_msg = "连接数据库失败！"
                code_msg = failed_code
                status_msg = self.currentThread()
                # qmutex.unlock()
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
        except Exception as e:
            self.sendException()
            m_title = ""
            m_info = "系统错误！"
            infoMessage(m_info, m_title, 300)

