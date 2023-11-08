from func.infoPage import infoMessage
from gui.home import *
from inf.probeThread import MyProbe


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
        # self.startProbeMem()

    """
    # 开始存储探测
    def startProbeMem(self):
        self.myprobe = MyProbe()
        self.myprobe.update_progress.connect(self.memWarning)
        self.myprobe.start()

    # 存储满警告
    def memWarning(self):
        m_title = "警告"
        m_info = "存储已经占满，请清理图片！！！"
        infoMessage(m_info, m_title)
        return
    """

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