import frozen
from gui.sys import *

class sysPage(Ui_Form, QWidget):
    next_page = Signal(str)
    update_json = Signal(dict)

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
        wifi_icon_path = frozen.app_path() + r"/res/icon/wifi.png"
        pixImg = self.mySetIconSize(wifi_icon_path)
        self.ui.wifi_icon_label.setPixmap(pixImg)
        self.ui.wifi_icon_label.setAlignment(Qt.AlignCenter)

        camera_icon_path = frozen.app_path() + r"/res/icon/camera.png"
        pixImg = self.mySetIconSize(camera_icon_path)
        self.ui.camera_icon_label.setPixmap(pixImg)
        self.ui.camera_icon_label.setAlignment(Qt.AlignCenter)

        clear_icon_path = frozen.app_path() + r"/res/icon/clear.png"
        pixImg = self.mySetIconSize(clear_icon_path)
        self.ui.clear_icon_label.setPixmap(pixImg)
        self.ui.clear_icon_label.setAlignment(Qt.AlignCenter)

        about_icon_path = frozen.app_path() + r"/res/icon/about.png"
        pixImg = self.mySetIconSize(about_icon_path)
        self.ui.about_icon_label.setPixmap(pixImg)
        self.ui.about_icon_label.setAlignment(Qt.AlignCenter)

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

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
    def on_btnWifi_clicked(self):
        page_msg = 'wifiPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnClear_clicked(self):
        page_msg = 'clearPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnSet_clicked(self):
        page_msg = 'setPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnAbout_clicked(self):
        page_msg = 'aboutPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'homePage'
        self.next_page.emit(page_msg)