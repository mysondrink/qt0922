import pymysql

import frozen
from func.infoPage import infoMessage
from gui.register import *
from keyboard.keyboard import KeyBoard

class registerPage(Ui_Form, QWidget):
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

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        self.setFocusWidget()
        self.installEvent()

    def installEvent(self):
        for item in self.focuswidget:
            item.installEventFilter(self)

    def setFocusWidget(self):
        self.focuswidget = [self.ui.nameLine, self.ui.pwdLine, self.ui.pwdLine_2]
        for item in self.focuswidget:
            item.setFocusPolicy(Qt.ClickFocus)

    def eventFilter(self, obj, event):
        if obj in self.focuswidget:
            if event.type() == QEvent.Type.FocusIn:
                # print(obj.setText("hello"))
                self.setKeyBoard(obj)

    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    def setKeyBoard(self, obj):
        self.keyboardtext = KeyBoard()
        self.keyboardtext.text_msg.connect(self.getKeyBoardText)
        obj_name = obj.objectName()
        obj_text = obj.text()
        self.keyboardtext.textInput.setText(obj_text)
        if obj_name == "nameLine":
            self.keyboardtext.nameLabel.setText("用户名")
        elif obj_name == "pwdLine":
            self.keyboardtext.nameLabel.setText("新密码")
        else:
            self.keyboardtext.nameLabel.setText("再次输入")
        self.keyboardtext.showWindow()

    # 用户名检测
    def checkName(self):
        if self.ui.pwdLine.text() == "" or self.ui.nameLine.text() == "" or self.ui.pwdLine_2.text() == "" :
            m_title = "错误"
            m_title = ""
            m_info = "请输入用户名或密码！"
            infoMessage(m_info, m_title)
        elif self.ui.pwdLine.text() != self.ui.pwdLine_2.text():
            m_title = "错误"
            m_title = ""
            m_info = "两次输入不正确！"
            infoMessage(m_info, m_title)
        else:
            self.insertUser()
            # self.setUserDict()
            m_title = ""
            m_info = "操作成功！"
            infoMessage(m_info, m_title, 300)
            page_msg = 'loginPage'
            self.next_page.emit(page_msg)

    # 注册用户写入数据库
    def insertUser(self):
        user_name = self.ui.nameLine.text()
        user_code = self.ui.pwdLine.text()
        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = 'INSERT INTO user_table(user_name, user_code) VALUES (%s,%s)'

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [user_name, user_code])
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()
        # 释放内存
        cursor.close()
        connection.close()

    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'loginPage'
        self.next_page.emit(page_msg)

    @Slot()
    def on_btnConfirm_clicked(self):
        self.checkName()

