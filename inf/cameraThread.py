from PySide2.QtCore import QThread, Signal

time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202

class CheckCameraThread(QThread):
    update_json = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            # qmutex.tryLock(trylock_time)
            info_msg = "摄像头检测中。。。"
            code_msg = succeed_code
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            self.sleep(time_to_sleep)
            info_msg = "连接摄像头成功！"
            code_msg = succeed_code
            status_msg = self.currentThread()
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            # qmutex.unlock()
        except Exception as e:
            print(e)