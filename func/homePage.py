from gui.home import *

class homePage(Ui_Form, QWidget):
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
    def on_btnPower_clicked(self):
        page_msg = 'powerPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnData_clicked(self):
        page_msg = 'testPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnHistory_clicked(self):
        page_msg = 'historyPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnSet_clicked(self):
        page_msg = 'editPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnPara_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)