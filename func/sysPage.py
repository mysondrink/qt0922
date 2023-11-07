from gui.sys import *

class sysPage(Ui_Form, QWidget):
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