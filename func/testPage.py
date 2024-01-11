import os
import time
import sys
import traceback

from func.testinfo import MyTestInfo
from gui.test import *
from inf.testThread import TestThread
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

allergen = [' ', '柳树', '普通豚草', '艾蒿', '屋尘螨']

class testPage(Ui_Form, QWidget):
    next_page = Signal(str)
    update_json = Signal(dict)
    update_log = Signal(str)

    """
    @detail 初始化加载界面信息，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()
        sys.excepthook = self.HandleException
        self.genderCb = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()

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
    @detail 在正常抛出异常时使用
    """
    def sendException(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.update_log.emit(err_msg)

    """
    @detail 设置界面相关信息
    """
    def InitUI(self):
        self.ui.btnExe.hide()
        self.ui.btnPrint.hide()
        self.ui.btnDownload.hide()
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

        # self.ui.modeBox_1.currentIndexChanged.connect(self.changeType)
        self.ui.modeBox_1.setCurrentIndex(4)
        self.ui.typeLabel.setText('8x5')
        # self.mypicthread = MyPicThread()
        # self.mypicthread.finished.connect(self.takePicture)
        self.ui.exeTable.horizontalHeader().close()
        self.ui.exeTable.verticalHeader().close()

        self.setFocusWidget()
        self.installEvent()
        self.setAllergenCb()
        self.setReagentCb()
        self.mytest()
        self.setBtnIcon()

    """
    @detail 设置按钮图标
    """
    def setBtnIcon(self):
        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/exe.png"
        self.ui.btnExe.setIconSize(QSize(32, 32))
        self.ui.btnExe.setIcon(QIcon(exe_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/exe.png"
        self.ui.btnPrint.setIconSize(QSize(32, 32))
        self.ui.btnPrint.setIcon(QIcon(exe_icon_path))

        switch_icon_path = frozen.app_path() + r"/res/icon/switch.png"
        self.ui.btnSwitch.setIconSize(QSize(32, 32))
        self.ui.btnSwitch.setIcon(QIcon(switch_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/compute.png"
        self.ui.btnDownload.setIconSize(QSize(32, 32))
        self.ui.btnDownload.setIcon(QIcon(exe_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

    """
    @detail 测试信息
    """
    def mytest(self):
        self.ui.nameLine.setText("123")
        self.ui.docCb.setText("123")
        self.ui.ageLine.setText("123")
        self.ui.departCb.setText("123")

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
        self.focuswidget = [self.ui.nameLine, self.ui.paraLine, self.ui.ageLine, self.ui.departCb, self.ui.docCb]
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

    """
    @detail 获取键盘的文本信息
    @detail 槽函数
    @param msg: 信号，键盘文本信息
    """
    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    """
    @detail 重置按钮信息，当发生页面跳转时触发
    """
    def resetBtn(self):
        self.ui.btnSwitch.hide()
        self.ui.btnExe.hide()
        self.ui.btnPrint.hide()
        self.ui.btnDownload.hide()
        self.ui.btnConfirm.show()
        self.ui.btnReturn.setGeometry(410, 10, 380, 80)

    def setAllergenTableView(self):
        f_name = self.ui.modeBox_1.currentText()
        path = frozen.app_path() + r"\\res\\allergen\\"
        f = open(path + f_name, "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
        allergen = []
        for i in lines:
            allergen.append(i.rstrip())
        row = 9
        column = 5
        self.allergen_table_model = QStandardItemModel(row, column)
        self.ui.tableView.setModel(self.allergen_table_model)
        self.ui.tableView.horizontalHeader().close()
        self.ui.tableView.verticalHeader().close()
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for k in range(column):
            if k % 2 == 0:
                color = QColor(255, 255, 127)
                item = QStandardItem()
                item.setData(color, Qt.BackgroundColorRole)
                self.allergen_table_model.setItem(0, k, item)
        num = 0
        for i in range(1, row):
            for j in range(column):
                if (i * row + j) % 2 != 0:
                    color = QColor(0, 255, 0)
                    print(allergen[num])
                    item = QStandardItem(allergen[num])
                    item.setData(color, Qt.BackgroundColorRole)
                    self.allergen_table_model.setItem(i, j, item)
                    num = num + 1
    def setAllergenCb(self):
        # 指定要读取的路径
        path = frozen.app_path() + r"\\res\\allergen\\"
        # path = r"/res/allergen/"
        # 获取指定路径下的所有文件名
        filenames = os.listdir(path)
        self.ui.modeBox_1.clear()
        # 输出所有文件名
        for filename in filenames:
            # self.ui.modeBox_3.clear()
            self.ui.modeBox_1.addItem(filename)
            self.ui.modeBox_1.setCurrentIndex(-1)

    """
    @detail 设置表格内容，主要是过敏原信息
    """
    def setTableView(self):
        # 测试
        self.ui.typeLabel.setText("8x5")
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

        # str_num = self.reagent_matrix_info[self.reagent_type.index(self.ui.modeBox_1.currentText())]
        # 测试
        str_num = self.reagent_matrix_info[self.reagent_type.index("58")]

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
    @detail 实现图片提取功能，获取得到的img_final图片和图片pixel信息
    @param msg: 信号，测试完后发出的时间信息
    """
    def takePicture(self, msg):
        cur_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        # time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        pic_path = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        time_now = msg

        # self.ui.photoLabel.setText(cur_time)

        # try:
        #     gray_aver = self.mypicthread.getGrayAver()
        #     gray_row = len(gray_aver)
        #     gray_column = len(gray_aver[0])
        # except Exception as e:
        #     print(e)
        img_final = cv.imread(frozen.app_path() + r'/inf/img_out/img_final.jpeg')
        img_origin = cv.imread(frozen.app_path() + r'/inf/img_out/img_0ori.jpeg')
        # 测试
        gray_aver = img_final[0]
        gray_row = 8
        gray_column = 5

        name_pic = time_now
        name_pic = "1"

        save_path = frozen.app_path() + r'/img/' + r'/' + pic_path + r'/' + name_pic + '-1.jpeg'
        dirs.makedir(save_path)
        flag_bool = cv.imwrite(save_path, img_origin)
        save_path = frozen.app_path() + r'/img/' + r'/' + pic_path + r'/' + name_pic + '-2.jpeg'
        dirs.makedir(save_path)
        flag_bool = cv.imwrite(save_path, img_final)

        self.testinfo.closeWin()
        page_msg = 'dataPage'
        self.next_page.emit(page_msg)

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
        test_time = cur_time.split()

        doctor = self.ui.docCb.text()
        depart = self.ui.departCb.text()
        age = self.ui.ageLine.text()
        gender = patient_gender
        name = self.ui.nameLine.text()

        matrix = self.ui.typeLabel.text()
        code_num = random.randint(1000, 19999)
        reagent_matrix_info = self.readPixtableNum()
        data_json = dict(patient_id=patient_id, patient_name=patient_name,
                         patient_age=patient_age, patient_gender=patient_gender,
                         item_type=item_type, pic_name=pic_name,
                         time=test_time, doctor=doctor,
                         depart=depart, age=age,
                         gender=gender, name=name,
                         matrix=matrix, code_num=code_num,
                         gray_aver=gray_aver, gray_row=gray_row,
                         gray_column=gray_column, pic_path=pic_path,
                         name_pic=name_pic, row_exetable=self.row_exetable,
                         column_exetable=self.column_exetable, reagent_matrix_info=reagent_matrix_info)
        info_msg = 201
        self.update_json.emit(dict(info=info_msg, data=data_json))
        return
        # 原代码，在本页面进行数据的展示
        self.ui.photoLabel.setScaledContents(False)  # 是否拉伸窗口

        # 测试
        self.ui.photoLabel.setStyleSheet("QLabel{"
                                         "border-image: url(./inf/img_out/img_final.jpeg); "
                                         "font: 20pt; "
                                         "color: rgb(255,0,0);}")

        # self.ui.photoLabel.setStyleSheet("QLabel{"
        #                                  "border-image: url(%s/img/%s/%s.jpeg); "
        #                                  "font: 20pt; "
        #                                  "color: rgb(255,0,0);}" % (frozen.app_path(), pic_path, name_pic))  # 设置拍照图片显示

        flag = 0

        self.ui.btnExe.hide()
        self.ui.btnSwitch.show()
        self.ui.btnPrint.show()
        self.ui.btnDownload.show()
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.btnReturn.setGeometry(601, 10, 187, 80)

        self.pic_para = 1

        for i in range(0, self.row_exetable + int(self.row_exetable / 2)):
            if i % 3 != 0:
                for j in range(0, self.column_exetable):
                    if i - flag < gray_row and j < gray_column:
                        # item = QStandardItem(str(gray_aver[i - flag][j]))
                        pix_num = int(gray_aver[i - flag][j])
                        pix_num = int(float(gray_aver[i - flag][j]) * self.pic_para)
                        pix_num = random.randint(15428, 16428)
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
    @detail 读取表格内容，同时以list形式保存到数据库
    @detail 弃用
    """
    def readPixtable(self):
        reagent_matrix_info = []
        for i in range(self.row_exetable + int(self.row_exetable / 2)):
            row_list = []
            for j in range(self.column_exetable):
                if i % 3 != 0:
                    index = self.pix_table_model.index(i, j)
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
    @detail 读取表格内容，同时以list形式保存
    @detail 弃用
    """
    def readPixtableNum(self):
        reagent_matrix_info = []
        for i in range(self.row_exetable + int(self.row_exetable / 2)):
            if i % 3 == 0:
                row_list = []
                for j in range(self.column_exetable):
                            index = self.ui.exeTable.model().index(i, j)  # 获取单元格的 QModelIndex 对象
                            combo_box = self.ui.exeTable.indexWidget(index)  # 获取该单元格中的 QComboBox 对象
                            current_text = combo_box.currentText()  # 获取 QComboBox 当前选中的文本
                            row_list.append(str(current_text))
                reagent_matrix_info.append(row_list)
        return reagent_matrix_info

    """
    @detail 连接数据库，写入图片信息
    @detail 需要修改
    @detail 弃用
    @param name_pic: 保存图片的图片名
    @param cur_time: 测试时间
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
        test_time = cur_time.split()

        doctor = self.ui.docCb.text()
        depart = self.ui.departCb.text()
        age = self.ui.ageLine.text()
        gender = patient_gender
        # gender = self.ui.genderCb.currentText()
        name = self.ui.nameLine.text()

        matrix = self.ui.typeLabel.text()
        code_num = random.randint(1000, 19999)

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
            cursor.execute(sql_2, [item_type, patient_id, pic_name, test_time[0],
                                   code_num, doctor, depart, matrix, test_time[1], reagent_matrix_info, name, age, gender])
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()
        # 释放内存
        cursor.close()
        connection.close()

    """
    @detail 读取数据库，获取试剂卡规格的信息
    """
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

        # self.ui.deleteCb.clear()
        # self.ui.deleteCb.addItems(self.reagent_type)
        # self.ui.editCb.clear()
        # self.ui.editCb.addItems(self.reagent_type)

        # 释放内存
        cursor.close()
        connection.close()

    """
    @detail 显示试剂卡规格信息
    @detail 槽函数
    """
    def changeType(self):
        # super().changeType()
        if self.ui.modeBox_1.currentText() == '':
            return
        text = self.reagent_matrix[self.reagent_type.index(self.ui.modeBox_1.currentText())]
        self.ui.typeLabel.setText(text)

    """
    @detail 系统存储检测
    @detail 弃用
    """
    def startProbeMem(self):
        self.myprobe = MyProbe()
        self.myprobe.update_progress.connect(self.memWarning)
        self.myprobe.finished.connect(self.myprobe.deleteLater())
        self.myprobe.start()

    """
    @detail 系统存储检测信息反馈
    @detail 弃用
    """
    def memWarning(self):
        m_title = "警告"
        m_info = "存储已经占满，请清理图片！"
        infoMessage(m_info, m_title)
        return

    """
    @detail 下载信息到u盘
    @detail 下载内容包括图片、数据库信息
    @detail 弃用
    """
    def downLoadToUSB(self):
        # 指定目标目录
        target_dir = '/media/orangepi/orangepi/'
        # 获取U盘设备路径
        try:
            filename = r"/media/orangepi/orangepi/" + os.listdir(target_dir)[0] + "/"
        except Exception as e:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)
            return
        # 检查U盘是否已插入
        timenow = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        save_path = filename + timenow + "/" + self.pic_num + ".txt"
        save_dir = filename + timenow + "/"
        # save_path = filename + self.searchtime + "/" + self.pic_num + ".txt"
        # save_dir = filename + self.searchtime + "/"
        dirs.makedir(save_path)
        if os.path.exists(save_dir):
            # 在U盘根目录下创建示例文件
            # print(filename + file_name)
            # print("exists")
            # file_path = os.path.join(filename, file_name)
            with open(save_path, "a") as f:
                msg = self.userinfo
                f.write(str(msg) + "\n")
            m_title = ""
            m_info = "下载完成！"
            infoMessage(m_info, m_title, 300)
        else:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)

    """
    @detail 返回按钮操作
    @detail 槽函数
    """
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
        elif self.ui.stackedWidget.currentIndex() == 3:
            self.resetBtn()
            self.ui.stackedWidget.setCurrentIndex(0)

    """
    @detail 确认按钮操作
    @detail 槽函数
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
    """

    """
    @detail 确认按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnConfirm_clicked(self):
        if self.ui.modeBox_1.currentIndex() == -1 or self.ui.nameLine == "" or self.ui.ageLine == "" \
                or self.ui.departCb == "" or self.ui.docCb == "":
            m_title = ""
            m_info = "请填写完信息！"
            infoMessage(m_info, m_title, 280)
            return

        self.setTableView()
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.btnExe.show()
        self.ui.btnConfirm.hide()
        self.setAllergenTableView()

    """
    @detail 检测按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnExe_clicked(self):
        self.testinfo = MyTestInfo()
        self.testinfo.setWindowModality(Qt.ApplicationModal)
        self.testinfo.show()
        # 测试
        # self.info_timer = QTimer()
        # self.info_timer.timeout.connect(self.takePicture)
        # self.info_timer.start(2000)
        # self.testThread = TestThread()
        # self.testThread.update_json.connect(self.takePicture)
        # self.testThread.start()
        # self.mypicthread = MyPicThread()
        self.takePicture(1)
        # self.mypicthread.start()

    """
    @detail 切换按钮操作
    @detail 槽函数
    @detail 弃用
    """
    @Slot()
    def on_btnSwitch_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 1:
            self.ui.stackedWidget.setCurrentIndex(2)
        elif self.ui.stackedWidget.currentIndex() == 2:
            self.ui.stackedWidget.setCurrentIndex(1)

    """
    @detail 下载按钮操作
    @detail 槽函数
    @detail 弃用
    """
    @Slot()
    def on_btnDownload_clicked(self):
        m_title = "错误"
        m_title = ""
        m_info = "下载中..."
        infoMessage(m_info, m_title, 380)
        # 创建定时器
        self.change_timer = QTimer()
        self.change_timer.timeout.connect(self.downLoadToUSB())
        # 设置定时器延迟时间，单位为毫秒
        # 延迟2秒跳转
        delay_time = 2000
        self.change_timer.start(delay_time)
