import frozen
from func.infoPage import infoMessage
from gui.about import *
import os
import shutil
import sys
import traceback
from inf.uploadThread import UploadThread
from func.testinfo import MyTestInfo



time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202
mutex = QMutex()

class aboutPage(Ui_Form, QWidget):
    next_page = Signal(str)
    update_json = Signal(dict)
    update_log = Signal(str)

    """
    @detail 初始化加载界面信息，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()
        sys.excepthook = self.HandleException
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
        self.count_num = 0

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
    @detail 设置界面相关信息
    """
    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnUpload.setIconSize(QSize(32, 32))
        self.ui.btnUpload.setIcon(QIcon(confirm_icon_path))

    """
    @detail u盘上传信息到软件
    @detail 默认上传文件为example.txt，上传内容为6个数字，每个数字各占一行
    @detail 弃用
    """
    def uploadFromUSB(self):
        # 指定目标目录
        target_dir = '/media/xiao/'

        # 获取U盘设备路径
        try:
            filename = r"/media/xiao/" + os.listdir(target_dir)[0]
        except Exception as e:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title, 240)
            return

            # 检查U盘是否已插入
        if os.path.exists(filename):
            # 在U盘根目录下查找指定文件
            file_path = os.path.join(filename, "example.txt")
            if os.path.exists(file_path):
                # 读取文件内容并打印到控制台
                with open(file_path, "r") as f:
                    # print(f.read())
                    m_title = ""
                    m_info = f.read()
                    infoMessage(m_info, m_title)
            else:
                # print("文件不存在")
                m_title = ""
                m_info = "文件不存在!"
                infoMessage(m_info, m_title, 300)
        else:
            # print("U盘未插入或无法访问")
            m_title = ""
            m_info = "U盘未插入或无法访问!"
            infoMessage(m_info, m_title, 240)

    """
    @detail 上传按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnUpload_clicked(self):
        self.testinfo = MyTestInfo()
        m_info = "数据上传中。。。"
        self.testinfo.setInfo(m_info)
        self.testinfo.setWindowModality(Qt.ApplicationModal)
        self.testinfo.show()

        """
        # 指定目标目录
        target_dir = '/media/orangepi/'
        # target_dir = '/media/xiao/'
        # 获取U盘设备路径
        try:
            if len(os.listdir(target_dir)) == 0:
                self.update_json.emit(failed_code)
                return
            else:
                u_name = r"/media/orangepi/" + os.listdir(target_dir)[0] + "/"
        except Exception as e:
            print(e)
            self.sendException()
            self.update_json.emit(failed_code)
            return
        try:
            cmd = 'su orangepi -c "cd %s"' % u_name
            flag = os.system(cmd)
            if flag != 0:
                self.update_json.emit(failed_code)
                delete_cmd = 'echo %s | sudo rm -rf %s' % ('orangepi', u_name)
                os.system(delete_cmd)
                return
        except Exception as e:
            print(e)
            self.sendException()
            self.update_json.emit(failed_code)
            return
        """
        try:
            os.system("sudo mount /dev/sda1 /mnt/mydev")
        except Exception as e:
            print("aboutPage :", e)
            return False
        u_name = "/mnt/mydev/"
        dir_list = os.listdir(u_name)
        upload_file_list = []
        for i in dir_list:
            path = u_name + i + "/new_data.xlsx"
            print(path)
            if os.path.exists(path):
                print("True")
                upload_file_list.append(path)
            else:
                print("False")
        if not upload_file_list:
            try:
                self.testinfo.closeWin()
                m_title = ""
                m_info = "上传完成!"
                infoMessage(m_info, m_title, 300)
                os.system("sudo umount /mnt/mydev")
            except Exception as e:
                print("aboutPage：", e)
            return
        self.upload_thread_list = []
        for i in upload_file_list:
            thread = UploadThread(i)
            self.upload_thread_list.append(thread)
            thread.finished.connect(lambda: thread.deleteLater())
            thread.finished.connect(self.countUploadThread)
            thread.start()

    def countUploadThread(self):
        mutex.lock()
        self.count_num = self.count_num + 1
        if len(self.upload_thread_list) <= self.count_num:
            try:
                os.system("sudo umount /mnt/mydev")
            except Exception as e:
                print("aboutPage：", e)
            self.testinfo.closeWin()
            return
        mutex.unlock()

    """
    @detail 返回按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)

    def getData(self):
        pass
