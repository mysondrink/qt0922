import os
from datetime import time

import frozen
from gui.power import *
from func.infoPage import infoMessage

class powerPage(Ui_Form, QWidget):
    next_page = Signal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()

    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setBtnIcon()
    def setBtnIcon(self):
        shutdown_icon_path = frozen.app_path() + r"/res/icon/shutdown.png"
        pixImg = self.mySetIconSize(shutdown_icon_path)
        self.ui.shutdown_icon_label.setPixmap(pixImg)
        self.ui.shutdown_icon_label.setAlignment(Qt.AlignCenter)

        logout_icon_path = frozen.app_path() + r"/res/icon/logout.png"
        pixImg = self.mySetIconSize(logout_icon_path)
        self.ui.logout_icon_label.setPixmap(pixImg)
        self.ui.logout_icon_label.setAlignment(Qt.AlignCenter)

    # 设置按钮图标比例
    def mySetIconSize(self, path):
        img = QImage(path)  # 创建图片实例
        mgnWidth = 50
        mgnHeight = 50  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'homePage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnLogout_clicked(self):
        page_msg = 'loginPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnShutdown_clicked(self):
        m_title = "提示"
        m_title = ""
        m_info = "请关闭电源！"
        timer = 1
        infoMessage(m_info, m_title, 300)
        time.sleep(1000)
        # order_str = "sudo shutdown -h now"
        order_str = 'echo %s | sudo %s' % ('orangepi', 'shutdown -h now')
        os.system(order_str)