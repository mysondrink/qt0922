import pymysql
from PySide2.QtCore import QThread, Signal

time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202

class CheckDataBaseThread(QThread):
    # global qmutex
    update_json = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.working = True
        self.num = 0

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
            print(e)

