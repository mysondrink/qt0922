import frozen
from func.infoPage import infoMessage
from gui.about import *


class aboutPage(Ui_Form, QWidget):
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

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnUpload.setIconSize(QSize(32, 32))
        self.ui.btnUpload.setIcon(QIcon(confirm_icon_path))

    def uploadFromUSB(self):
        m_title = ""
        m_info = "上传完成！"
        infoMessage(m_info, m_title)

    @Slot()
    def on_btnUpload_clicked(self):
        m_title = ""
        m_info = "上传中！"
        infoMessage(m_info, m_title)
        # 创建定时器
        self.change_timer = QTimer()
        self.change_timer.timeout.connect(self.uploadFromUSB())
        # 设置定时器延迟时间，单位为毫秒
        # 延迟2秒跳转
        delay_time = 2000
        self.change_timer.start(delay_time)

    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)

