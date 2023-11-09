import frozen
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
        self.setBtnIcon()

    def setBtnIcon(self):
        reagent_icon_path = frozen.app_path() + r"/res/icon/reagent.png"
        pixImg = self.mySetIconSize(reagent_icon_path)
        self.ui.reagent_icon_label.setPixmap(pixImg)
        self.ui.reagent_icon_label.setAlignment(Qt.AlignCenter)

        history_icon_path = frozen.app_path() + r"/res/icon/history.png"
        pixImg = self.mySetIconSize(history_icon_path)
        self.ui.history_icon_label.setPixmap(pixImg)
        self.ui.history_icon_label.setAlignment(Qt.AlignCenter)

        reagent_set_icon_path = frozen.app_path() + r"/res/icon/set.png"
        pixImg = self.mySetIconSize(reagent_set_icon_path)
        self.ui.reagent_set_icon_label.setPixmap(pixImg)
        self.ui.reagent_set_icon_label.setAlignment(Qt.AlignCenter)

        sys_icon_path = frozen.app_path() + r"/res/icon/sys.png"
        pixImg = self.mySetIconSize(sys_icon_path)
        self.ui.sys_icon_label.setPixmap(pixImg)
        self.ui.sys_icon_label.setAlignment(Qt.AlignCenter)

        power_icon_path = frozen.app_path() + r"/res/icon/power.png"
        self.ui.btnPower.setIconSize(QSize(32, 32))
        self.ui.btnPower.setIcon(QIcon(power_icon_path))

    # 设置按钮图标比例
    def mySetIconSize(self, path):
        img = QImage(path)  # 创建图片实例
        mgnWidth = 50
        mgnHeight = 50  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

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