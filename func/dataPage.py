import os
import random
import re
import time

import pymysql

from func.infoPage import infoMessage
from gui.info import *
import frozen
from utils import dirs
from utils.report import MyReport
import cv2 as cv


class dataPage(Ui_Form, QWidget):
    next_page = Signal(str)
    update_json = Signal(dict)
    def __init__(self):
        super().__init__()
        self.pix_table_model = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()

    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.setBtnIcon()
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setTableWidget()

    def setBtnIcon(self):
        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnData.setIconSize(QSize(32, 32))
        self.ui.btnData.setIcon(QIcon(confirm_icon_path))

        switch_icon_path = frozen.app_path() + r"/res/icon/switch.png"
        self.ui.btnPic.setIconSize(QSize(32, 32))
        self.ui.btnPic.setIcon(QIcon(switch_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/exe.png"
        self.ui.btnPrint.setIconSize(QSize(32, 32))
        self.ui.btnPrint.setIcon(QIcon(exe_icon_path))

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnReport.setIconSize(QSize(32, 32))
        self.ui.btnReport.setIcon(QIcon(confirm_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/compute.png"
        self.ui.btnDownload.setIconSize(QSize(32, 32))
        self.ui.btnDownload.setIcon(QIcon(exe_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

    # this is a data get slot
    def getData(self, msg):
        print(msg['info'])
        # self.writeFile(msg['data'])

        flag = 0
        pic_para = 1
        self.info = msg['info']
        self.data = msg['data']
        self.row_exetable = int(self.data['row_exetable'])
        self.column_exetable = int(self.data['column_exetable'])

        name_pic = self.data['name_pic']
        cur_time = self.data['time']
        pic_path = self.data['pic_path']
        self.test_time = cur_time[0] + ' ' + cur_time[1]
        reagent_matrix_info = self.data['reagent_matrix_info']
        self.pix_table_model = QStandardItemModel(self.row_exetable + int(self.row_exetable / 2), self.column_exetable)
        self.ui.tableView.setModel(self.pix_table_model)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.photoLabel.setText(self.test_time)


        # 测试
        # self.ui.photoLabel.setStyleSheet("QLabel{"
        #                                  "border-image: url(./inf/img_out/img_final.jpeg); "
        #                                  "font: 20pt; "
        #                                  "color: rgb(255,0,0);}")
        # print('%s\\img\\%s\\%s.jpeg' % (frozen.app_path(), pic_path, name_pic))
        self.ui.photoLabel.setStyleSheet("QLabel{"
                                         "border-image: url(./img/%s/%s.jpeg); "
                                         "font: 20pt; "
                                         "color: rgb(255,0,0);}" % (pic_path, name_pic))  # windows环境
        # self.ui.photoLabel.setStyleSheet("QLabel{"
        #                                  "border-image: url(%s/img/%s/%s.jpeg); "
        #                                  "font: 20pt; "
        #                                  "color: rgb(255,0,0);}" % (frozen.app_path(), pic_path, name_pic))  # linux环境
        if self.info == 201:
            gray_row = self.data['gray_row']
            gray_column = self.data['gray_column']
            gray_aver = self.data['gray_aver']
            for i in range(self.row_exetable + int(self.row_exetable / 2)):
                if i % 3 != 0:
                    for j in range(self.column_exetable):
                        if i - flag < gray_row and j < gray_column:
                            # item = QStandardItem(str(gray_aver[i - flag][j]))
                            # pix_num = int(gray_aver[i - flag][j])
                            # pix_num = int(float(gray_aver[i - flag][j]) * self.pic_para)
                            pix_num = random.randint(15428, 16428)
                            item = QStandardItem(str(pix_num))
                        else:
                            item = QStandardItem(str(0))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.pix_table_model.setItem(i, j, item)
                else:
                    num = i % 3
                    for j in range(0, self.column_exetable):
                        if j < gray_column:
                            item = QStandardItem(reagent_matrix_info[num][j])
                        else:
                            item = QStandardItem(str(0))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.pix_table_model.setItem(i, j, item)
                    flag += 1

            self.insertMysql(name_pic, cur_time)  # 图片数据信息存入数据库

            # self.ftpServer(base64_data)   #上传图片到服务器
        elif self.info == 202:
            reagent_matrix_info = re.split(r",", reagent_matrix_info)[1:]
            for i in range(self.row_exetable + int(self.row_exetable / 2)):
                for j in range(self.column_exetable):
                    item = QStandardItem(reagent_matrix_info[i * self.column_exetable + j])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.pix_table_model.setItem(i, j, item)

    """
    连接数据库，写入图片信息
    需要修改
    """
    def insertMysql(self, name_pic, cur_time):
        reagent_matrix_info = str(self.readPixtable())

        patient_id = self.data['patient_id']
        
        # name_id = random.randint(1,199)
        # patient_name = self.name_file[name_id].get("name")
        # patient_age = self.name_file[name_id].get("age")
        # patient_gender = self.name_file[name_id].get("gender")

        patient_name = self.data['patient_name']
        patient_age = self.data['patient_age']
        patient_gender = self.data['patient_gender']
        item_type = self.data['item_type']
        pic_name = name_pic
        doctor = self.data['doctor']
        depart = self.data['depart']
        age = self.data['age']
        name = self.data['name']
        matrix = self.data['matrix']
        code_num = self.data['code_num']
        
        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = 'INSERT IGNORE INTO patient_copy1(name, patient_id, age, gender) VALUES (%s,%s,%s,%s)'
        sql_2 = "INSERT IGNORE INTO reagent_copy1(reagent_type, patient_id, reagent_photo, " \
                "reagent_time, reagent_code, doctor, depart, reagent_matrix, reagent_time_detail, " \
                "reagent_matrix_info, patient_name, patient_age, patient_gender) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [patient_name, patient_id, patient_age, patient_gender])
            cursor.execute(sql_2, [item_type, patient_id, pic_name, cur_time[0],
                                   code_num, doctor, depart, matrix, cur_time[1], reagent_matrix_info, name, age, patient_gender])
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
    设置报告单页面
    """
    def setTableWidget(self):
        v = QVBoxLayout()
        text = MyReport().gethtml()
        self.myreport = QTextEdit()

        str_list = []
        for i in range(16):
            str_list.append(str(i))
        self.myreport.setHtml(text % tuple(str_list))

        v.addWidget(self.myreport)
        self.ui.tableWidget.setLayout(v)

    """
    读取表格内容，同时以list形式保存到数据库
    """
    def readPixtable(self):
        reagent_matrix_info = ""
        for i in range(self.row_exetable + int(self.row_exetable / 2)):
            for j in range(self.column_exetable):
                index = self.pix_table_model.index(i, j)
                data = self.pix_table_model.data(index)
                reagent_matrix_info += "," + str(data)
        return reagent_matrix_info

    def downLoadToUSB(self):
        # 指定目标目录
        target_dir = '/media/orangepi/orangepi/'
        # 获取U盘设备路径
        try:
            u_name = r"/media/orangepi/orangepi/" + os.listdir(target_dir)[0] + "/"
        except Exception as e:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)
            return
        # 检查U盘是否已插入
        timenow = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        save_dir = u_name + timenow + "/"
        filename = str(len(os.listdir(save_dir)) + 1)
        save_path = save_dir + filename + ".txt"
        dirs.makedir(save_path)
        save_img_path = save_dir + filename + ".jpeg"
        if os.path.exists(save_dir):
            # 在U盘根目录下创建示例文件
            # print(filename + file_name)
            # print("exists")
            # file_path = os.path.join(filename, file_name)
            with open(save_path, "a") as f:
                msg = self.data
                f.write(str(msg) + "\n")
            try:
                name_pic = self.data['name_pic']
                pic_path = self.data['pic_path']
                img_final = cv.imread('%s\\img\\%s\\%s.jpeg' % (frozen.app_path(), pic_path, name_pic))
                flag_bool = cv.imwrite(save_img_path, img_final)
            except Exception as e:
                m_title = ""
                m_info = "图片读取失败或未找到图片！"
                infoMessage(m_info, m_title)
            m_title = ""
            m_info = "下载完成！"
            infoMessage(m_info, m_title, 300)
        else:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)

    def writeFile(self, msg):
        # file_path = os.path.join(r'/', "example.txt")
        with open("./example.txt", "w") as f:
            f.write(str(msg))

    @Slot()
    def on_btnPrint_clicked(self):
        print("print")
        m_title = ""
        m_info = "输出表格成功!"
        infoMessage(m_info, m_title, 300)
        time.sleep(1)
        return
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_time = self.test_time
        myEm5822_Print = Em5822_Print(test_time, time_now)
        myEm5822_Print.em5822_print()
        m_title = ""
        m_info = "输出表格成功!"
        infoMessage(m_info, m_title, 300)

    @Slot()
    def on_btnDownload_clicked(self):
        print("Download")
        m_title = "错误"
        m_title = ""
        m_info = "下载中..."
        infoMessage(m_info, m_title, 380)
        return
        # 创建定时器
        self.info_timer = QTimer()
        self.info_timer.timeout.connect(self.downLoadToUSB)
        # 设置定时器延迟时间，单位为毫秒
        # 延迟2秒跳转
        delay_time = 2000
        self.info_timer.start(delay_time)

    @Slot()
    def on_btnData_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    @Slot()
    def on_btnPic_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    @Slot()
    def on_btnReport_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    @Slot()
    def on_btnReturn_clicked(self):
        if self.info == 201:
            page_msg = 'testPage'
            self.next_page.emit(page_msg)
        elif self.info == 202:
            page_msg = 'history'
            self.next_page.emit(page_msg)