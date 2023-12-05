from PySide2.QtCore import QThread, Signal

time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202

class CheckSerialThread(QThread):
    update_json = Signal(dict)

    """
    @detail 构造函数
    @param parent: 无父类
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    """
    @detail 线程开启
    @detail 串口的检测
    """
    def run(self):
        # qmutex.tryLock(trylock_time)
        try:
            info_msg = "串口检测中。。。"
            code_msg = succeed_code
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            self.sleep(time_to_sleep)
            info_msg = "连接串口成功！"
            code_msg = succeed_code
            status_msg = self.currentThread()
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            # qmutex.unlock()
        except Exception as e:
            print(e)