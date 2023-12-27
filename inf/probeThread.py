from PySide2.QtCore import QThread, Signal, QStorageInfo
import sys
import traceback

failed_code = 404
succeed_code = 202

class MyProbe(QThread):
    update_progress = Signal(int)
    update_log = Signal(str)

    """
    @detail 初始化线程，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        sys.excepthook = self.HandleException

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
    @detail 进行系统存储的检测
    """
    def run(self):
        QStorageInfo.refresh()
        memorystr = QStorageInfo().root()
        mem_total = memorystr.bytesTotal() / (1024 * 1024 * 1024)
        mem_avail = memorystr.bytesAvailable() / (1024 * 1024 * 1024)
        mem_progress = mem_avail / mem_total
        if mem_progress < 0.02:
            self.update_progress.emit(failed_code)
        else:
            self.update_progress.emit(succeed_code)