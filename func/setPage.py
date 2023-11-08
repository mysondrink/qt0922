from func.infoPage import infoMessage
from gui.set import *


class setPage(Ui_Form, QWidget):
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
        self.ui.modeBox_4.addItems(["5000x4000", "3000x2000"])

    @Slot()
    def on_btnConfirm_clicked(self):
        m_title = ""
        m_info = "成功！"
        infoMessage(m_info, m_title)

    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)

