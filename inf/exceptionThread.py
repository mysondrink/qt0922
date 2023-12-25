import sys
import traceback

from PySide2.QtCore import QThread, Signal
from inf.logThread import LogThread
class ExceptionThread(QThread):
    update_log = Signal(str)

    ## @detail 创建记录异常的信息
    ## @detail 构造函数
    #  @param logFile: log的输入地址
    #  @param mainFrame: 是否需要在主窗口中弹出提醒
    def __init__(self, log_file, main_frame=None, parent=None):
        super().__init__(parent)
        self.log_file = log_file
        self.main_frame = main_frame
        # 重定向异常捕获
        sys.excepthook = self.HandleException
        self.myLogThread = LogThread(self.log_file)

    ## @detail 捕获及输出异常类
    #  @param excType: 异常类型
    #  @param excValue: 异常对象
    #  @param tb: 异常的trace back
    def HandleException(self, excType, excValue, tb):
        # then call the default handler
        sys.__excepthook__(excType, excValue, tb)

        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        # err_msg += '\n Your App happen an exception, please contact administration.'
        # Here collecting traceback and some log files to be sent for debugging.
        # But also possible to handle the error and continue working.
        self.update_log.emit(err_msg)

