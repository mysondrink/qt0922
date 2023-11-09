import pymysql

import frozen
from func.infoPage import infoMessage
from gui.edit import *
page_dict = {'page': 0, 'page2': 1, 'page3': 2, 'page4': 3, 'page5': 4}
from keyboard.keyboard import KeyBoard

class editPage(Ui_Form, QWidget):
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
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.rowCb.addItems(["2x3", "2x5", "4x5", "8x5"])
        self.resetBtn()

        self.setBtnIcon()

        self.setFocusWidget()
        self.installEvent()

    def setBtnIcon(self):
        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        add_icon_path = frozen.app_path() + r"/res/icon/add.png"
        pixImg = self.mySetIconSize(add_icon_path)
        self.ui.add_icon_label.setPixmap(pixImg)
        self.ui.add_icon_label.setAlignment(Qt.AlignCenter)

        delete_icon_path = frozen.app_path() + r"/res/icon/delete.png"
        pixImg = self.mySetIconSize(delete_icon_path)
        self.ui.delete_icon_label.setPixmap(pixImg)
        self.ui.delete_icon_label.setAlignment(Qt.AlignCenter)

        edit_icon_path = frozen.app_path() + r"/res/icon/edit.png"
        pixImg = self.mySetIconSize(edit_icon_path)
        self.ui.edit_icon_label.setPixmap(pixImg)
        self.ui.edit_icon_label.setAlignment(Qt.AlignCenter)

    # 设置按钮图标比例
    def mySetIconSize(self, path):
        img = QImage(path)  # 创建图片实例
        mgnWidth = 50
        mgnHeight = 50  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

    def installEvent(self):
        for item in self.focuswidget:
            item.installEventFilter(self)

    def setFocusWidget(self):
        self.focuswidget = [self.ui.nameLine]
        for item in self.focuswidget:
            item.setFocusPolicy(Qt.ClickFocus)

    def eventFilter(self, obj, event):
        if obj in self.focuswidget:
            if event.type() == QEvent.Type.FocusIn:
                # print(obj.setText("hello"))
                self.setKeyBoard(obj)
                return True
            else:
                return False
        else:
            return False

    def setKeyBoard(self, obj):
        self.keyboardtext = KeyBoard()
        self.keyboardtext.text_msg.connect(self.getKeyBoardText)
        obj_name = obj.objectName()
        obj_text = obj.text()
        self.keyboardtext.textInput.setText(obj_text)
        if obj_name == "nameLine":
            self.keyboardtext.nameLabel.setText("试剂卡型号")
        self.keyboardtext.showWindow()

    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    def resetBtn(self):
        self.ui.btnConfirm.hide()
        self.ui.btnReturn.setGeometry(10, 10, 780, 80)

    def resetBtn_2(self):
        self.ui.btnConfirm.show()
        self.ui.btnReturn.setGeometry(410, 10, 380, 80)

    # 获取试剂卡的信息
    def setReagentCb(self):
        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = 'SELECT * FROM matrix_table'
        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()
        self.reagent_type = []
        self.reagent_matrix = []
        self.reagent_matrix_info = []

        for x in cursor.fetchall():
            self.reagent_type.append(x[1])
            self.reagent_matrix.append(x[2])
            self.reagent_matrix_info.append(x[3])

        # self.ui.modeBox_1.clear()
        # self.ui.modeBox_3.clear()
        # self.ui.modeBox_1.addItems(self.reagent_type)
        # self.ui.modeBox_1.setCurrentIndex(-1)
        # self.ui.typeLabel.setText("")
        # self.ui.modeBox_3.addItems(self.reagent_type)
        # self.ui.modeBox_3.setCurrentIndex(-1)

        self.ui.deleteCb.clear()
        self.ui.deleteCb.addItems(self.reagent_type)
        self.ui.editCb.clear()
        self.ui.editCb.addItems(self.reagent_type)

        # 释放内存
        cursor.close()
        connection.close()

    def edit(self):
        m_title = ""
        m_info = "成功！"
        infoMessage(m_info, m_title)
        self.resetBtn()
        self.ui.stackedWidget.setCurrentIndex(0)

    @Slot()
    def on_btnAdd_clicked(self):
        self.resetBtn_2()
        self.ui.stackedWidget.setCurrentIndex(1)

    @Slot()
    def on_btnDelete_clicked(self):
        self.resetBtn_2()
        self.ui.stackedWidget.setCurrentIndex(2)
        self.setReagentCb()

    @Slot()
    def on_btnModify_clicked(self):
        self.resetBtn_2()
        self.ui.stackedWidget.setCurrentIndex(3)
        self.setReagentCb()

    @Slot()
    def on_btnConfirm_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 1:
            # 添加
            self.ui.stackedWidget.setCurrentIndex(4)
        elif self.ui.stackedWidget.currentIndex() == 2:
            pass
        elif self.ui.stackedWidget.currentIndex() == 3:
            # 修改
            self.ui.stackedWidget.setCurrentIndex(4)
        elif self.ui.stackedWidget.currentIndex() == 4:
            m_title = ""
            m_info = "确认中！"
            infoMessage(m_info, m_title)
            # 创建定时器
            self.change_timer = QTimer()
            self.change_timer.timeout.connect(self.edit)
            # 设置定时器延迟时间，单位为毫秒
            # 延迟2秒跳转
            delay_time = 2000
            self.change_timer.start(delay_time)

    @Slot()
    def on_btnReturn_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            page_msg = 'homePage'
            self.next_page.emit(page_msg)
        else:
            self.resetBtn()
            self.ui.stackedWidget.setCurrentIndex(0)

