from gui.testinfo import *


class MyTestInfo(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
        self.timer = None

    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(320, 180, 200, 80)
        self.info_timer = QTimer()
        self.info_timer.timeout.connect(self.closeWin)
        self.info_timer.start(2000)
    def closeWin(self):
        print("close!")
        self.close()
        self.info_timer.stop()
