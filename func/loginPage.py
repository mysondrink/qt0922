import frozen
import sys
import traceback
from gui.login import *
# from func.homePage import homePage
# from func.registerPage import registerPage
from keyboard.keyboard import KeyBoard
from func.infoPage import infoMessage
import pymysql

screen_top = 30

class loginPage(Ui_Form, QWidget):
    next_page = Signal(str)
    # next_page = Signal(QWidget)
    update_json = Signal(dict)
    update_log = Signal(str)

    """
    @detail 初始化加载界面信息，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()
        sys.excepthook = self.HandleException
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
        self.setUserDict()

    """
    @detail 捕获及输出异常类
    @param excType: 异常类型
    @param excValue: 异常对象
    @param tb: 异常的trace back
    """
    def HandleException(self, excType, excValue, tb):
        sys.__excepthook__(excType, excValue, tb)
        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        self.update_log.emit(err_msg)

    """
    @detail 发送异常信息
    """
    def sendException(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.update_log.emit(err_msg)

    """
    @detail 设置界面相关信息
    """
    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # screen = QDesktopWidget().screenGeometry()
        # _x, _y = screen.left(), screen.top()
        # h, w = self.width(), self.height()
        # self.setGeometry(screen.left(), screen.top() + screen_top, h, w)
        # self.showMaximized()
        self.setBtnIcon()
        self.mytest()
        self.setFocusWidget()
        self.installEvent()

    """
    @detail 测试账号
    """
    def mytest(self):
        self.ui.nameLine.setText("test")
        self.ui.numLine.setText("123456")

    """
    @detail 设置按钮图标
    """
    def setBtnIcon(self):
        login_icon_path = frozen.app_path() + r"/res/icon/login.png"
        pixImg = self.mySetIconSize(login_icon_path)
        self.ui.login_icon_label.setPixmap(pixImg)
        self.ui.login_icon_label.setAlignment(Qt.AlignCenter)

        register_icon_path = frozen.app_path() + r"/res/icon/register.png"
        pixImg = self.mySetIconSize(register_icon_path)
        self.ui.register_icon_label.setPixmap(pixImg)
        self.ui.register_icon_label.setAlignment(Qt.AlignCenter)

    """
    @detail 设置按钮图标比例
    @param path: 图片路径
    """
    def mySetIconSize(self, path):
        img = QImage(path)  # 创建图片实例
        mgnWidth = 50
        mgnHeight = 50  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

    """
    @detail 安装事件监听
    """
    def installEvent(self):
        for item in self.focuswidget:
            item.installEventFilter(self)

    """
    @detail 设置组件点击焦点
    """
    def setFocusWidget(self):
        self.focuswidget = [self.ui.nameLine, self.ui.numLine]
        for item in self.focuswidget:
            item.setFocusPolicy(Qt.ClickFocus)

    """
    @detail 事件过滤
    @detail 槽函数
    @param obj: 发生事件的组件
    @param event: 发生的事件
    """
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

    """
    @detail 设置可以键盘弹出的组件
    @detail 槽函数
    @param obj: 键盘弹出的组件
    """
    def setKeyBoard(self, obj):
        self.keyboardtext = KeyBoard()
        self.keyboardtext.text_msg.connect(self.getKeyBoardText)
        obj_name = obj.objectName()
        obj_text = obj.text()
        self.keyboardtext.textInput.setText(obj_text)
        if obj_name == "nameLine":
            self.keyboardtext.nameLabel.setText("用户名")
        else:
            self.keyboardtext.nameLabel.setText("密码")
        self.keyboardtext.showWindow()

    """
    @detail 获取键盘的文本信息
    @detail 槽函数
    @param msg: 信号，键盘文本信息
    """
    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    """
    @detail 用户字典生成
    """
    def setUserDict(self):
        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = 'SELECT * FROM user_table'
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
        user_name = []
        user_code = []

        for x in cursor.fetchall():
            user_name.append(x[0])
            user_code.append(x[1])

        self.user_dict = dict(zip(user_name, user_code))

        # 释放内存
        cursor.close()
        connection.close()

    """
    @detail 登录按钮操作，对用户信息进行判断
    @detail 槽函数
    """
    @Slot()
    def on_loginBtn_clicked(self):
        # super().on_loginBtn_clicked()
        if self.ui.nameLine.text() == "" or self.ui.numLine.text() == "":
            m_title = "错误"
            m_title = ""
            m_info = "用户名或密码未填写！"
            infoMessage(m_info, m_title, 280)
        else:
            if self.user_dict.get(self.ui.nameLine.text()) is None or self.user_dict.get(
                    self.ui.nameLine.text()) != self.ui.numLine.text():
                m_title = "错误"
                m_title = ""
                m_info = "用户名或编号错误!"
                infoMessage(m_info, m_title, 300)
            else:
                # page_msg = homePage()
                page_msg = 'homePage'
                self.next_page.emit(page_msg)

    """
    @detail 注册按钮操作，跳转到注册界面
    @detail 槽函数
    """
    @Slot()
    def on_registerBtn_clicked(self):
        # page_msg = registerPage()
        page_msg = 'registerPage'
        self.next_page.emit(page_msg)