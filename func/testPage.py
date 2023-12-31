from gui.test import *
# from inf.picThread import MyPicThread
from keyboard.keyboard import KeyBoard
from func.infoPage import infoMessage
from inf.probeThread import MyProbe
import datetime
import cv2 as cv
import frozen as frozen
import utils.dirs as dirs
import random
import pymysql

allergen = [' ','花生', '牛奶', '大豆', '桃子']

class testPage(Ui_Form, QWidget):
    next_page = Signal(str)
    def __init__(self):
        super().__init__()
        self.genderCb = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
        self.startProbeMem()

    def InitUI(self):
        self.ui.btnExe.hide()
        self.ui.btnPrint.hide()
        self.ui.btnSwitch.hide()
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.genderCb = QButtonGroup()
        self.genderCb.addButton(self.ui.radioButton)
        self.genderCb.addButton(self.ui.radioButton_2)
        self.genderCb.setId(self.ui.radioButton, 0)
        self.genderCb.setId(self.ui.radioButton_2, 1)

        self.ui.modeBox_1.currentIndexChanged.connect(self.changeType)
        # self.mypicthread = MyPicThread()

        self.setFocusWidget()
        self.installEvent()
        self.setReagentCb()
        self.mytest()
        self.setBtnIcon()

    def setBtnIcon(self):
        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/exe.png"
        self.ui.btnExe.setIconSize(QSize(32, 32))
        self.ui.btnExe.setIcon(QIcon(exe_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/compute.png"
        self.ui.btnPrint.setIconSize(QSize(32, 32))
        self.ui.btnPrint.setIcon(QIcon(exe_icon_path))

        switch_icon_path = frozen.app_path() + r"/res/icon/switch.png"
        self.ui.btnSwitch.setIconSize(QSize(32, 32))
        self.ui.btnSwitch.setIcon(QIcon(switch_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

    def mytest(self):
        self.ui.nameLine.setText("123")
        self.ui.docCb.setText("123")
        self.ui.ageLine.setText("123")
        self.ui.departCb.setText("123")

    def installEvent(self):
        for item in self.focuswidget:
            item.installEventFilter(self)

    def setFocusWidget(self):
        self.focuswidget = [self.ui.nameLine, self.ui.paraLine, self.ui.ageLine, self.ui.departCb, self.ui.docCb]
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
        if obj_name == "paraLine":
            self.keyboardtext.nameLabel.setText("参数")
        elif obj_name == "nameLine":
            self.keyboardtext.nameLabel.setText("姓名")
        elif obj_name == "ageLine":
            self.keyboardtext.nameLabel.setText("年龄")
        elif obj_name == "departCb":
            self.keyboardtext.nameLabel.setText("科室")
        else:
            self.keyboardtext.nameLabel.setText("送检医生")
        self.keyboardtext.showWindow()

    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    def resetBtn(self):
        self.ui.btnSwitch.hide()
        self.ui.btnExe.hide()
        self.ui.btnPrint.hide()
        self.ui.btnConfirm.show()
        self.ui.btnReturn.setGeometry(410, 10, 380, 80)

    """
    设置表格内容
    """
    def setTableView(self):
        # 设置行列
        # 需要改进
        if self.ui.modeBox_1.currentIndex() == -1:
            return
        # self.ui.photolabel.setText("表格生成中。。。")
        dict_mode = {
            "2x3": 1,
            "2x5": 2,
            "4x5": 3,
            "8x5": 4,
        }
        if dict_mode.get(self.ui.typeLabel.text()) == 1:
            self.row_exetable = 2
            self.column_exetable = 3
        elif dict_mode.get(self.ui.typeLabel.text()) == 2:
            self.row_exetable = 2
            self.column_exetable = 5
        elif dict_mode.get(self.ui.typeLabel.text()) == 3:
            self.row_exetable = 4
            self.column_exetable = 5
        else:
            self.row_exetable = 8
            self.column_exetable = 5

        self.pix_table_model = QStandardItemModel(self.row_exetable + int(self.row_exetable / 2), self.column_exetable)
        self.ui.exeTable.setModel(self.pix_table_model)

        self.ui.exeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.exeTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        str_num = self.reagent_matrix_info[self.reagent_type.index(self.ui.modeBox_1.currentText())]

        for i in range(0, self.row_exetable + int(self.row_exetable / 2)):
            if i % 3 == 0:
                for j in range(0, self.column_exetable):
                    content_cb = QComboBox(self)
                    content_cb.addItems(allergen)
                    num = int(str_num[j + (i % 3) * self.row_exetable])
                    content_cb.setCurrentIndex(num)
                    content_cb.setEditable(True)
                    _lineEdit = content_cb.lineEdit()
                    _lineEdit.setAlignment(Qt.AlignCenter)
                    # content_cb.setStyleSheet(self.cb_style_sheet)
                    self.ui.exeTable.setIndexWidget(self.pix_table_model.index(i, j), content_cb)

    """
    实现图片提取功能
    """
    def takePicture(self):
        cur_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        pic_path = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        self.ui.photoLabel.setText(cur_time)
        # try:
        #     gray_aver = self.mypicthread.takePicture(time_now)
        #     gray_row = len(gray_aver)
        #     gray_column = len(gray_aver[0])
        # except Exception as e:
        #     print(e)
        img_final = cv.imread(frozen.app_path() + r'/inf/img_out/img_final.jpeg')
        print(img_final)
        # 测试
        gray_aver = img_final[0]
        gray_row = 5
        gray_column = 8

        name_pic = time_now

        save_path = frozen.app_path() + r'/img/' + r'/' + pic_path + r'/' + name_pic + '.jpeg'
        dirs.makedir(save_path)
        flag_bool = cv.imwrite(save_path, img_final)
        self.ui.photoLabel.setScaledContents(False)  # 是否拉伸窗口

        # 测试
        self.ui.photoLabel.setStyleSheet("QLabel{"
                                         "border-image: url(%s/inf/img_out/img_final.jpeg); "
                                         "font: 20pt; "
                                         "color: rgb(255,0,0);}" % (frozen.app_path()))

        # self.ui.photoLabel.setStyleSheet("QLabel{"
        #                                  "border-image: url(%s/img/%s/%s.jpeg); "
        #                                  "font: 20pt; "
        #                                  "color: rgb(255,0,0);}" % (frozen.app_path(), pic_path, name_pic))  # 设置拍照图片显示

        flag = 0

        self.pic_para = 1

        for i in range(0, self.row_exetable + int(self.row_exetable / 2)):
            if i % 3 != 0:
                for j in range(0, self.column_exetable):
                    if i - flag < gray_row and j < gray_column:
                        # item = QStandardItem(str(gray_aver[i - flag][j]))
                        pix_num = int(gray_aver[i - flag][j])
                        pix_num = int(float(gray_aver[i - flag][j]) * self.pic_para)
                        pix_num = random.randint(15428,16428)
                        item = QStandardItem(str(pix_num))
                    else:
                        item = QStandardItem(str(0))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.pix_table_model.setItem(i, j, item)
            else:
                flag += 1

        self.insertMysql(name_pic, cur_time)  # 图片数据信息存入数据库

        # self.ftpServer(base64_data)   #上传图片到服务器

    """
    读取表格内容，同时以list形式保存到数据库
    """
    def readPixtable(self):
        reagent_matrix_info = []
        for i in range(self.row_exetable + int(self.row_exetable/2)):
            row_list = []
            for j in range(self.column_exetable):
                if i % 3 != 0:
                    index = self.pix_table_model.index(i,j)
                    data = self.pix_table_model.data(index)
                    row_list.append(str(data))
                else:
                    index = self.ui.exeTable.model().index(i, j)  # 获取单元格的 QModelIndex 对象
                    combo_box = self.ui.exeTable.indexWidget(index)  # 获取该单元格中的 QComboBox 对象
                    current_text = combo_box.currentText()  # 获取 QComboBox 当前选中的文本
                    row_list.append(str(current_text))
            reagent_matrix_info.append(row_list)
        return reagent_matrix_info

    """
    读取表格内容，同时以list形式保存到数据库
    """
    def readPixtableNum(self):
        str_num = ""
        for i in range(self.row_exetable + int(self.row_exetable / 2)):
            # row_list = []
            if i % 3 == 0:
                for j in range(self.column_exetable):
                    index = self.ui.exeTable.model().index(i, j)  # 获取单元格的 QModelIndex 对象
                    combo_box = self.ui.exeTable.indexWidget(index)  # 获取该单元格中的 QComboBox 对象
                    data_index = combo_box.currentIndex() + 1
                    # current_text = combo_box.currentText()  # 获取 QComboBox 当前选中的文本
                    str_num = str_num + str(data_index)
        return str_num

    """
    连接数据库，写入图片信息
    需要修改
    """
    def insertMysql(self, name_pic, cur_time):
        reagent_matrix_info = str(self.readPixtable())

        patient_id = random.randint(1000, 1999)

        # name_id = random.randint(1,199)
        # patient_name = self.name_file[name_id].get("name")
        # patient_age = self.name_file[name_id].get("age")
        # patient_gender = self.name_file[name_id].get("gender")

        patient_name = self.ui.nameLine.text()
        patient_age = self.ui.ageLine.text()
        id_num = self.genderCb.checkedId()
        if id_num == 0:
            patient_gender = "男"
        else:
            patient_gender = "女"

        # patient_gender = self.ui.genderCb.currentText()

        item_type = self.ui.modeBox_1.currentText()
        pic_name = name_pic

        # 时间进行切片
        time = cur_time.split()

        doctor = self.ui.docCb.text()
        depart = self.ui.departCb.text()
        age = self.ui.ageLine.text()
        gender = patient_gender
        # gender = self.ui.genderCb.currentText()
        name = self.ui.nameLine.text()

        matrix = self.ui.typeLabel.text()
        code_num = random.randint(1000, 2000)

        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = 'INSERT INTO patient_copy1(name, patient_id, age, gender) VALUES (%s,%s,%s,%s)'
        sql_2 = "INSERT INTO reagent_copy1(reagent_type, patient_id, reagent_photo, " \
                "reagent_time, reagent_code, doctor, depart, reagent_matrix, reagent_time_detail, " \
                "reagent_matrix_info, patient_name, patient_age, patient_gender) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [patient_name, patient_id, patient_age, patient_gender])
            cursor.execute(sql_2, [item_type, patient_id, pic_name, time[0],
                                   code_num, doctor, depart, matrix, time[1], reagent_matrix_info, name, age, gender])
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()
        # 释放内存
        cursor.close()
        connection.close()

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

        self.ui.modeBox_1.clear()
        # self.ui.modeBox_3.clear()
        self.ui.modeBox_1.addItems(self.reagent_type)
        self.ui.modeBox_1.setCurrentIndex(-1)
        self.ui.typeLabel.setText("")
        # self.ui.modeBox_3.addItems(self.reagent_type)
        # self.ui.modeBox_3.setCurrentIndex(-1)

        # self.ui.deleteCb.clear()
        # self.ui.deleteCb.addItems(self.reagent_type)
        # self.ui.editCb.clear()
        # self.ui.editCb.addItems(self.reagent_type)

        # 释放内存
        cursor.close()
        connection.close()

    def changeType(self):
        # super().changeType()
        if self.ui.modeBox_1.currentText() == '':
            return
        text = self.reagent_matrix[self.reagent_type.index(self.ui.modeBox_1.currentText())]
        self.ui.typeLabel.setText(text)

    def startProbeMem(self):
        self.myprobe = MyProbe()
        self.myprobe.update_progress.connect(self.memWarning)
        self.myprobe.start()

    def memWarning(self):
        m_title = "警告"
        m_info = "存储已经占满，请清理图片！"
        infoMessage(m_info, m_title)
        self.ui.btnData.setEnabled(False)
        # self.ui.btnHistory.setEnabled(False)
        return

    @Slot()
    def on_btnReturn_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            page_msg = 'homePage'
            self.next_page.emit(page_msg)
        elif self.ui.stackedWidget.currentIndex() == 1:
            self.resetBtn()
            self.ui.stackedWidget.setCurrentIndex(0)
        elif self.ui.stackedWidget.currentIndex() == 2:
            self.resetBtn()
            self.ui.stackedWidget.setCurrentIndex(0)
    @Slot()
    def on_btnConfirm_clicked(self):
        if self.ui.modeBox_1.currentIndex() == -1 or self.ui.nameLine == "" or self.ui.ageLine == "" \
                or self.ui.departCb == "" or self.ui.docCb == "":
            m_title = ""
            m_info = "请填写完信息！"
            infoMessage(m_info, m_title, 280)
            return

        self.setTableView()

        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.btnExe.show()
        self.ui.btnConfirm.hide()

    @Slot()
    def on_btnExe_clicked(self):
        m_title = ""
        m_info = "照片生成中..."
        infoMessage(m_info, m_title, 280)
        # 创建定时器
        self.change_timer = QTimer()
        self.change_timer.timeout.connect(self.btnExe_clicked())
        # 设置定时器延迟时间，单位为毫秒
        # 延迟2秒跳转
        delay_time = 2000
        self.change_timer.start(delay_time)

    def btnExe_clicked(self):
        self.ui.btnExe.hide()
        self.ui.btnSwitch.show()
        self.ui.btnPrint.show()
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.btnReturn.setGeometry(539, 10, 254, 80)
        self.takePicture()

    @Slot()
    def on_btnSwitch_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 1:
            self.ui.stackedWidget.setCurrentIndex(2)
        elif self.ui.stackedWidget.currentIndex() == 2:
            self.ui.stackedWidget.setCurrentIndex(1)
