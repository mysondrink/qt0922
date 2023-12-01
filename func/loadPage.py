import time

from gui.loading import *
from inf.dbThread import CheckDataBaseThread
from inf.cameraThread import CheckCameraThread
from inf.serialThread import CheckSerialThread
from func.loginPage import loginPage
from func.homePage import homePage
from func.powerPage import powerPage
from func.registerPage import registerPage
from func.testPage import testPage
from func.historyPage import historyPage
from func.editPage import editPage
from func.sysPage import sysPage
from func.wifiPage import wifiPage
from func.clearPage import clearPage
from func.setPage import setPage
from func.aboutPage import aboutPage
from func.dataPage import dataPage

flag_num = 0
failed_code = 404
succeed_code = 202


class loadPage(Ui_Form, QMainWindow):
    update_json = Signal(dict)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
        self.list_widget = None
        self.cur_page = None
        self.flag_num = flag_num

    def InitUI(self):
        self.statusShowTime()
        self.ui.title_label.setText('荧光判读仪器')
        self.ui.retry_icon_label.hide()
        self.ui.btnRetry.hide()
        # self.ui.textEdit.setEnabled(False)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)

        screen = QDesktopWidget().screenGeometry()
        self.move(screen.left(), screen.top())
        self.showMaximized()

        self.startThread()

    def startThread(self):
        self.thread_list = [CheckSerialThread(), CheckDataBaseThread(), CheckCameraThread()]
        self.thread_id = []

        for num in range(len(self.thread_list)):
            self.thread_id.append(self.thread_list[num])
            self.thread_list[num].update_json.connect(self.setInfoLabel)
            self.thread_list[num].finished.connect(self.thread_list[num].deleteLater)
            self.thread_list[num].start()

    # @Slot()
    def setInfoLabel(self, msg):
        try:
            info_msg, code_msg, status_msg = msg['info'], msg['code'], msg['status']
            if status_msg in self.thread_id:
                self.thread_id.remove(status_msg)
            text = self.ui.textEdit.toPlainText()
            self.ui.textEdit.append(info_msg)
            lines = text.split('\n')
            if code_msg == failed_code:
                self.retryThread()
                self.flag_num = -1
            elif len(lines) == 5 and self.flag_num == 0:
                # 创建定时器
                self.change_timer = QTimer()
                self.flag_num == -1
                self.change_timer.timeout.connect(self.showPage)
                # 设置定时器延迟时间，单位为毫秒
                # 延迟2秒跳转
                delay_time = 2000
                self.change_timer.start(delay_time)
        except Exception as e:
            print(e)

    def showPage(self):
        # print(self.flag_num)
        self.list_widget = []
        if self.flag_num == 0:
            self.change_timer.stop()
            self._s = QStackedLayout()
            self._h = QHBoxLayout()
            self.cur_page = loginPage()
            self.cur_page.next_page.connect(self.changePage)
            self.cur_page.update_json.connect(self.getJsonData)
            self.cur_page.setFocus()
            self._s.addWidget(self.cur_page)
            self._h.addLayout(self._s)
            self.ui.centerframe.setLayout(self._h)

            self._s.setSpacing(0)
            self._h.setSpacing(0)

            self._s.setContentsMargins(0, 0, 0, 0)
            self._h.setContentsMargins(0, 0, 0, 0)

            self.flag_num = -1
            self.list_widget.append(self._s.currentWidget())
            # 尾指针
            self.q_ptr = self._s.currentIndex()
            # 头指针
            self.p_ptr = self._s.currentIndex()

    """
    进行页面的跳转
    获取子页面返回的信号，信号是跳转页面
    """
    def changePage(self, msg):
        try:
            # 设置栈为2
            num = len(self.list_widget)
            if msg == 'history':
                print(self.list_widget)
                self._s.removeWidget(self._s.currentWidget())
                self.list_widget.remove(self.list_widget[1])
                self.p_ptr -= 1
                return
            # if num > 1:
            #     self._s.removeWidget(self.list_widget[0])
            #     self.list_widget.remove(self.list_widget[0])
            #     self.p_ptr += 1
            #     time.sleep(0.5)
            self.cur_page = globals()[msg]()
            self.cur_page.next_page.connect(self.changePage)
            self.cur_page.update_json.connect(self.getJsonData)
            self.cur_page.setFocus()

            # 防止页面重复
            # num = len(self.list_widget)
            # if self._s.indexOf(self.cur_page) > -1:
            #     self._s.removeWidget(self.list_widget[1])
            #     self.list_widget.remove(self.list_widget[1])
            #     self.q_ptr -= 1
            #     time.sleep(0.5)
            #     return
            if num > 1:
                self._s.removeWidget(self.list_widget[0])
                self.list_widget.remove(self.list_widget[0])
                self.p_ptr += 1
                time.sleep(0.5)

            self._s.addWidget(self.cur_page)
            self._s.setCurrentIndex(self._s.count() - 1)
            self.list_widget.append(self._s.currentWidget())
            self.q_ptr += 1
            # self.ui.centerframe.setLayout(self._s)
            # self.cur_page.show()
        except Exception as e:
            print(e)
    
    def statusShowTime(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.showCurrentTime)

        self.timer.start(1000)

    def showCurrentTime(self):
        cur_time = QDateTime.currentDateTime()
        time_display = cur_time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.ui.time_label.setText(time_display)

    def retryThread(self):
        self.ui.retry_icon_label.show()
        self.ui.btnRetry.show()

    """
    子窗口之间通信
    子窗口传输数据给父窗口，父窗口在传到指定的子窗口
    """
    def getJsonData(self, msg):
        self.update_json.connect(self.cur_page.getData)
        self.update_json.emit(msg)

    @Slot()
    def on_btnRetry_clicked(self):
        self.ui.textEdit.clear()
        self.flag_num = flag_num
        self.ui.retry_icon_label.hide()
        self.ui.btnRetry.hide()
        for num in range(len(self.thread_id)):
            stat = self.thread_id[num].isFinished()
            if self.thread_id[num].isFinished() is False:
                continue
            self.thread_id[num].deleteLater()
        self.thread_id.clear()
        self.startThread()

    @Slot()
    def loadingError(self):
        error_stylesheet = "QProgressBar {\
                               border: 2px solid lightgray;\
                               border-radius: 5px;\
                               text-align: center;\
                               color: white;\
                           }\
                           QProgressBar::chunk {\
                               background-color: #ff0000;\
                               border-radius: 4px;\
                           }"
        self.ui.progressBar.setStyleSheet(error_stylesheet)
        self.ui.btnRetry.setVisible(True)
        self.ui.retry_icon_label.setVisible(True)