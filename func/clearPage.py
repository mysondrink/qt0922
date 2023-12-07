import os
import datetime
import sys
import traceback
import frozen
from func.infoPage import infoMessage
from gui.clear import *
from inf.probeThread import MyProbe

class clearPage(Ui_Form, QWidget):
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

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        self.ui.clearCb.addItems(['7', '14', '21', '0'])
        self.ui.clearCb.setCurrentIndex(-1)
        self.startProbeMem()
        self.setClearBar()

    """
    @detail 遍历本地图片文件
    """
    def deleteDirs(self, now_time, root_list):
        for i in range(1, len(root_list)):
            if now_time > root_list[i][-10:]:
                self.deletePicFile(root_list[i])

    #批量删除文件
    """
    @detail 批量删除文件
    """
    def deletePicFile(self, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.deletePicFile(c_path)
            else:
                os.remove(c_path)

    # 设置存储条
    """
    @detail 设置存储条
    """
    def setClearBar(self):
        self.memorystr = QStorageInfo().root()
        self.ui.clearBar.setMinimum(0)
        self.ui.clearBar.setMaximum(100)
        mem_total = self.memorystr.bytesTotal() / (1024 * 1024 * 1024)
        mem_avail = self.memorystr.bytesAvailable() / (1024 * 1024 * 1024)
        mem_progress = (1 - (mem_avail / mem_total)) * 100
        self.ui.clearBar.setValue(int(mem_progress))

    # 存储满后显示
    """
    @detail 存储满后显示
    @detail 弃用
    """
    def checkBoxInfo(self, msg):
        if msg == "警告":
            self.ui.btnData.setEnabled(False)
            self.ui.btnHistory.setEnabled(False)
            # self.ui.btnSet.setEnabled(False)
            # self.ui.btnPara.setEnabled(False)

    # 开始存储探测
    """
    @detail 开始存储探测
    """
    def startProbeMem(self):
        self.myprobe = MyProbe()
        self.myprobe.update_progress.connect(self.memWarning)
        self.myprobe.start()

    # 存储满警告
    """
    @detail 存储满后警告
    """
    def memWarning(self):
        m_title = "警告"
        m_info = "存储已经占满，请清理图片！"
        infoMessage(m_info, m_title)
        return

    """
    @detail 确认按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnConfirm_clicked(self):
        pic_path = frozen.app_path() + "/img/"
        root_list = []
        dirs_list = []
        files_list = []
        for root, dirs, files in os.walk(pic_path):
            root_list.append(root)
            dirs_list.append(dirs)
            files_list.append(files)

        if self.ui.clearCb.currentIndex() == -1:
            m_title = "错误"
            m_title = ""
            m_info = "未选择时间，请选择后执行该操作！"
            infoMessage(m_info, m_title)
            return
        dict_mode = {
            "7": 1,
            "14": 2,
            "21": 3,
            "0": 4
        }
        if dict_mode.get(self.ui.clearCb.currentText()) == 1:
            day = -7
            now_time = datetime.datetime.now()
            now_time = now_time + datetime.timedelta(days=day)
            self.deleteDirs(str(now_time)[:10], root_list)
        elif dict_mode.get(self.ui.clearCb.currentText()) == 2:
            day = -14
            now_time = datetime.datetime.now()
            now_time = now_time + datetime.timedelta(days=day)
            self.deleteDirs(str(now_time)[:10], root_list)

        elif dict_mode.get(self.ui.clearCb.currentText()) == 3:
            day = -21
            now_time = datetime.datetime.now()
            now_time = now_time + datetime.timedelta(days=day)
            self.deleteDirs(str(now_time)[:10], root_list)

        else:
            self.deletePicFile(pic_path)

        # self.deletePicFile(pic_path)
        m_title = "确认"
        m_title = ""
        m_info = "已经完成清理!"
        infoMessage(m_info, m_title, 260)
        # self.ui.btnData.setEnabled(True)
        # self.ui.btnHistory.setEnabled(True)
        # self.ui.btnSet.setEnabled(True)
        # self.ui.btnPara.setEnabled(True)
        self.setClearBar()

    """
    @detail 返回按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)