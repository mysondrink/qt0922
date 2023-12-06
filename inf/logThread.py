from PySide2.QtCore import QThread
import frozen as frozen
import logging
import sys
import traceback

log_file = frozen.app_path() + r"/reagent.log"

class LogThread(QThread):
    """
    @detail 初始化线程
    @detail 构造函数
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = None
        self.log_file = log_file

    """
    @detail 线程运行函数
    @detail 进行日志的创建
    """
    def run(self):
        try:
            # 创建一个logger
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO

            # 创建一个handler，用于写入日志文件
            # logfile = frozen.app_path() + r'/reagent.log'
            fh = logging.FileHandler(self.log_file, mode='a')  # open的打开模式这里可以进行参考
            fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

            # 定义handler的输出格式（时间，文件，行数，错误级别，错误提示）
            formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
            fh.setFormatter(formatter)

            # 将logger添加到handler里面
            self.logger.addHandler(fh)

            # 日志级别
            #
            # DEBUG：详细的信息,通常只出现在诊断问题上
            # INFO：确认一切按预期运行
            # WARNING（默认）：一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”)。这个软件还能按预期工作。
            # ERROR：更严重的问题,软件没能执行一些功能
            # CRITICAL：一个严重的错误,这表明程序本身可能无法继续运行
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            self.logger.warning(err_msg)

    """
    @detail 获取线程的日志信息
    @detail 槽函数
    """
    def getLogMsg(self, msg):
        self.logger.info(msg)
