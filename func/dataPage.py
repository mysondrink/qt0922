import os
import random
import re
import sys
import traceback
import pymysql
import time
import datetime
import numpy as np

from inf.USBThread import CheckUSBThread
from func.infoPage import infoMessage
from gui.info import *
import frozen
from utils import dirs
from utils.report import MyReport
import cv2 as cv
from inf.pictureThread import pictureThread
from func.testinfo import MyTestInfo
from inf.print import Em5822_Print


class dataPage(Ui_Form, QWidget):
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
        self.pix_table_model = None
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
    @detail 未使用
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
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentIndex(3) # 取消图片显示
        self.ui.btnPic.hide()
        self.setBtnIcon()
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setTableWidget()
        self.ui.photoLabel.setText("")
        self.ui.picLabel.setText("")
    
    def closeEvent(self, event):
        self.setParent(None)
        event.accept()		# 表示同意了，结束吧

    """
    @detail 设置按钮图标
    """
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
    """
    @detail 获取信息
    @detail 信息来自testPage和historyPage页面，信息包括图片信息和数据库信息
    @param msg: 信号，发送来的信息
    """
    def getData(self, msg):
        print("data id", id(self))
        # print(msg['info'])
        # self.writeFile(msg['data'])
        # 测试
        start_time = time.time()
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
        self.pix_table_model_copy = QStandardItemModel(self.row_exetable + int(self.row_exetable / 2) + 2, self.column_exetable)
        self.ui.tableView.setModel(self.pix_table_model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.horizontalHeader().close()
        self.ui.tableView.verticalHeader().close()

        self.ui.tableView_2.setModel(self.pix_table_model_copy)
        self.ui.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_2.horizontalHeader().close()
        self.ui.tableView_2.verticalHeader().close()
        self.ui.tableView_2.setGridStyle(Qt.NoPen)
        self.ui.rightLabel.setText(self.test_time)
        self.ui.leftLabel.setText(self.test_time)

        # self.testinfo = MyTestInfo()
        # self.testinfo.setProgress(80)
        # self.testinfo.setWindowModality(Qt.ApplicationModal)
        # self.testinfo.show()
        
        # self.mypicturethread = pictureThread()
        # self.mypicturethread.finished.connect(self.showPicture)
        # self.mypicturethread.finished.connect(self.mypicturethread.deleteLater)
        # self.mypicturethread.start()

        # 测试
        # img_right = cv.imread('%s\\img\\%s\\%s-2.jpeg' % (frozen.app_path(), pic_path, name_pic))  # windows
        # img_left = cv.imread('%s\\img\\%s\\%s-1.jpeg' % (frozen.app_path(), pic_path, name_pic))  # windows
        # img_right = cv.imread('%s/img/%s/%s-2.jpeg' % (frozen.app_path(), pic_path, name_pic))  # linux
        # img_left = cv.imread('%s/img/%s/%s-1.jpeg' % (frozen.app_path(), pic_path, name_pic))  # linux

        # img_right = cv.resize(img_right, (350, 350))
        # img_left = cv.resize(img_left, (350, 350))

        # img_right = self.opencv2img(img_right)
        # img_left = self.opencv2img(img_left)

        # img_right = self.img2pix(img_right)
        # img_left = self.img2pix(img_left)

        # img_right = self.resizePhoto(img_right)
        # img_left = self.resizePhoto(img_left)
        # img_left, img_right = self.mypicturethread.getPixImg()
        # self.testinfo.closeWin()
        end_time = time.time()
        print("setPicture", end_time - start_time)

        start_time = time.time()
        self.pic_para = 1
        if self.info == 201:
            self.point_list = self.data['point_str']
            gray_row = self.data['gray_row']
            gray_column = self.data['gray_column']
            gray_aver = self.data['gray_aver'][1:]
            for i in range(self.row_exetable + int(self.row_exetable / 2)):
                if i % 3 != 0:
                    for j in range(self.column_exetable):
                        if i - flag < gray_row and j < gray_column:
                            # item = QStandardItem(str(gray_aver[i - flag][j]))
                            # pix_num = int(gray_aver[i - flag][j])
                            pix_num = int(float(gray_aver[i - flag][j]) * self.pic_para)
                            # pix_num = random.randint(15428, 16428)
                            item = QStandardItem(str(pix_num))
                        else:
                            item = QStandardItem(str(0))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.pix_table_model.setItem(i, j, item)
                else:
                    # num = i % 3
                    for j in range(0, self.column_exetable):
                        if j < gray_column:
                            # item = QStandardItem(reagent_matrix_info[num][j])
                            item = QStandardItem(reagent_matrix_info[flag][j])
                        else:
                            item = QStandardItem(str(0))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.pix_table_model.setItem(i, j, item)
                    flag += 1

            end_time = time.time()
            print("setTable", end_time - start_time)
            start_time = time.time()
            self.insertMysql(name_pic, cur_time)  # 图片数据信息存入数据库
            end_time = time.time()
            print("insertmysql", end_time - start_time)

            # self.ftpServer(base64_data)   #上传图片到服务器
        elif self.info == 202:
            self.allergy_info = reagent_matrix_info
            point_str = self.data['point_str']
            self.showDataView(point_str + ',' + reagent_matrix_info)
            # reagent_matrix_info = re.split(r",", reagent_matrix_info)[1:]
            # self.allergy_info = reagent_matrix_info
            # for i in range(self.row_exetable + int(self.row_exetable / 2)):
            #     for j in range(self.column_exetable):
            #         item = QStandardItem(reagent_matrix_info[i * self.column_exetable + j])
            #         item.setTextAlignment(Qt.AlignCenter)
            #         self.pix_table_model.setItem(i, j, item)

    """
    @detail 调整图片自适应label大小
    @param img_right: opencv图片
    """
    def resizePhoto(self, img_right):
        # 自适应label大小
        width, height, channels = img_right.shape  ##获取图片宽度
        long = width - height
        image_copy = cv.copyMakeBorder(img_right, 0, 0, int(long / 2), int(long / 2), cv.BORDER_CONSTANT, value=[0, 0, 0])

        new_long = self.ui.rightLabel.width()
        new_img_right = cv.resize(image_copy, (int(new_long), int(new_long)), interpolation=cv.INTER_AREA)

        new_img_right = self.opencv2img(new_img_right)
        new_img = self.img2pix(new_img_right)

        return new_img

    """
    @detail 将opencv图片转换成QImage图片
    @param img: opencv图片
    """
    def opencv2img(self, img):
        height, width, depth = img.shape
        cv_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        cv_img = QImage(cv_img.data, width, height, width * depth, QImage.Format_RGB888)
        return cv_img

    """
    @detail 将QImage图片转换成QPixmap图片
    @param img: QImage图片
    """
    def img2pix(self, img):
        img_pix = QPixmap.fromImage(img)
        return img_pix

    """
    @detail 连接数据库，写入图片信息
    @detail 需要修改
    @param name_pic: 保存图片的图片名
    @param cur_time: 测试时间
    """
    def insertMysql(self, name_pic, cur_time):
        reagent_matrix_info = str(self.readPixtable())
        point_str = self.data['point_str']
        self.showDataView(point_str + ',' + reagent_matrix_info)
        self.allergy_info = reagent_matrix_info
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
        points = self.data['point_str']
        gray_aver = self.data['gray_aver_str']
        nature_aver = self.data['nature_aver_str']
        
        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = 'INSERT IGNORE INTO patient_copy1(name, patient_id, age, gender) VALUES (%s,%s,%s,%s)'
        sql_2 = "INSERT IGNORE INTO reagent_copy1(reagent_type, patient_id, reagent_photo, " \
                "reagent_time, reagent_code, doctor, depart, reagent_matrix, reagent_time_detail, " \
                "reagent_matrix_info, patient_name, patient_age, patient_gender, points, gray_aver, nature_aver) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [patient_name, patient_id, patient_age, patient_gender])
            cursor.execute(sql_2, [item_type, patient_id, pic_name, cur_time[0],
                                   code_num, doctor, depart, matrix, cur_time[1], 
                                   reagent_matrix_info, name, age, patient_gender, 
                                   points, gray_aver, nature_aver])
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
    @detail 设置报告单页面
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
    @detail 读取表格内容，同时以list形式保存到数据库
    """
    def readPixtable(self):
        reagent_matrix_info = []
        for i in range(self.row_exetable + int(self.row_exetable / 2)):
            for j in range(self.column_exetable):
                index = self.pix_table_model.index(i, j)
                data = self.pix_table_model.data(index)
                reagent_matrix_info.append(str(data))
        return ",".join(reagent_matrix_info)

    """
    @detail u盘提示信息
    @param msg: U盘信息    
    """
    def getUSBInfo(self, msg):
        if msg == 202:
            self.usbthread.deleteLater()
            m_title = ""
            m_info = "下载完成！"
            infoMessage(m_info, m_title, 300)
        elif msg == 404:
            self.usbthread.deleteLater()
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)
        elif msg == 405:
            self.usbthread.deleteLater()
            m_title = ""
            m_info = "图片读取失败或未找到图片！"
            infoMessage(m_info, m_title)

    """
    @detail 下载信息到u盘
    @detail 下载内容包括图片、数据库信息
    @detail 弃用
    """
    def downLoadToUSB(self):
        self.download_timer.stop()
        # 两层
        # 指定目标目录
        target_dir = '/media/orangepi/'
        target_dir = r"/media/orangepi/" + os.listdir(target_dir)[0] + "/"
        # target_dir = '/media/orangepi/orangepi/'
        # 获取U盘设备路径
        try:
            u_name = target_dir + os.listdir(target_dir)[0] + "/"
            # u_name = r"/media/orangepi/orangepi/" + os.listdir(target_dir)[0] + "/"
        except Exception as e:
            # target_dir = '/media/orangepi/orangepi/'
            # u_name = r"/media/orangepi/orangepi/" + os.listdir(target_dir)[0] + "/"
            # m_title = ""
            # m_info = "U盘未插入或无法访问！"
            # infoMessage(m_info, m_title)
            # return
            self.sendException()
        # 检查U盘是否已插入
        timenow = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        save_dir = u_name + timenow + "/"
        dirs.makedir(save_dir)
        filename = str(len(os.listdir(save_dir)) + 1)
        save_path = save_dir + filename + ".txt"
        dirs.makedir(save_path)
        save_img_path_1 = save_dir + filename + "-1.jpeg"
        save_img_path_2 = save_dir + filename + "-2.jpeg"
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
                # img_origin = cv.imread('%s\\img\\%s\\%s-1.jpeg' % (frozen.app_path(), pic_path, name_pic)) # windows
                img_origin = cv.imread('%s/img/%s/%s-1.jpeg' % (frozen.app_path(), pic_path, name_pic)) # linux
                flag_bool = cv.imwrite(save_img_path_1, img_origin)

                # img_final = cv.imread('%s\\img\\%s\\%s-2.jpeg' % (frozen.app_path(), pic_path, name_pic)) # windows
                img_final = cv.imread('%s/img/%s/%s-2.jpeg' % (frozen.app_path(), pic_path, name_pic)) # linux
                flag_bool = cv.imwrite(save_img_path_2, img_final)
            except Exception as e:
                print(str(e))
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
               # 指定目标目录

    """
    @detail 读取下传文件
    @detail 测试代码
    """
    def writeFile(self, msg):
        # file_path = os.path.join(r'/', "example.txt")
        with open("./example.txt", "w") as f:
            f.write(str(msg))

    """
    @detail 数据展示
    """
    def showDataView(self, data):
        title_list = ["定位点", "", "", "", "定位点"]
        data_copy = re.split(r",", data)
        data_copy = title_list + data_copy
        row = self.pix_table_model_copy.rowCount()
        column = self.pix_table_model_copy.columnCount()
        for i in range(row):
            for j in range(column):
                pix_num = data_copy[i * column + j]
                item = QStandardItem(str(pix_num))
                item.setTextAlignment(Qt.AlignCenter)
                self.pix_table_model_copy.setItem(i, j, item)
        return

    """
    @detail 打印按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnPrint_clicked(self):
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_time = self.test_time
        Data_Base = [self.data['patient_name'], self.data['patient_gender'], self.data['patient_id'],
                    self.data['code_num'], '检测组合' + self.data['item_type'], test_time, time_now]
        gray_aver_str = self.data['gray_aver_str'].split(",")[1:]
        nature_aver_str = self.data['nature_aver_str'].split(",")[1:]
        array_gray_aver = np.array(gray_aver_str)
        array_nature_aver = np.array(nature_aver_str)
        matrix_gray_aver = array_gray_aver.reshape(9, 5)
        matrix_nature_aver = array_nature_aver.reshape(8, 5)
        Data_Nature = matrix_gray_aver
        Data_Light = matrix_nature_aver
        myEm5822_Print = Em5822_Print()
        
        myEm5822_Print.em5822_print(Data_Base, Data_Nature, Data_Light)
        m_title = ""
        m_info = "输出表格成功!"
        infoMessage(m_info, m_title, 300)

    """
    @detail 下载按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnDownload_clicked(self):
        name = self.data['name_pic']
        path = self.data['pic_path']
        data = self.data
        self.usbthread = CheckUSBThread(name, path, data, self.data['point_str'] + ',' + self.allergy_info)
        self.usbthread.update_json.connect(self.getUSBInfo)
        # 创建定时器
        self.download_timer = QTimer()
        self.download_timer.timeout.connect(self.usbthread.start)
        self.download_timer.timeout.connect(self.download_timer.stop)
        # 设置定时器延迟时间，单位为毫秒
        # 延迟2秒跳转
        delay_time = 2000
        self.download_timer.start(delay_time)
        m_title = ""
        m_info = "下载中..."
        infoMessage(m_info, m_title, 380)

    """
    @detail 数据按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnData_clicked(self):
        # self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget.setCurrentIndex(3)

    """
    @detail 图片按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnPic_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    """
    @detail 报告单按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnReport_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    """
    @detail 返回按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnReturn_clicked(self):
        if self.info == 201:
            page_msg = 'testPage'
            self.next_page.emit(page_msg)
        elif self.info == 202:
            page_msg = 'history'
            self.next_page.emit(page_msg)
