import os
import shutil
import datetime

from gui.history import *
page_dict = {'page': 0, 'page_2': 1, 'page_3': 2, 'page_4': 3}
from func.infoPage import infoMessage
import pymysql
import math
import frozen
from utils.report import MyReport
from inf.print import Em5822_Print


header_list = ["试剂卡编号", "采样时间",  "病人编号" , "病人姓名"]

class historyPage(Ui_Form, QWidget):
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
        self.ui.dateBox.setCalendarPopup(True)
        self.ui.dateBox.setDateTime(QDateTime.currentDateTime())

        self.setBtnIcon()

        self.resetBtn_3()
        self.ui.btnDownload.hide()
        self.ui.btnPrint.hide()
        self.ui.btnReport.hide()
        self.setReagentCb()
        self.setTableWidget()

    def setBtnIcon(self):
        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        pre_icon_path = frozen.app_path() + r"/res/icon/pre.png"
        self.ui.btnPre.setIconSize(QSize(32, 32))
        self.ui.btnPre.setIcon(QIcon(pre_icon_path))

        next_icon_path = frozen.app_path() + r"/res/icon/next.png"
        self.ui.btnNext.setIconSize(QSize(32, 32))
        self.ui.btnNext.setIcon(QIcon(next_icon_path))

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnReport.setIconSize(QSize(32, 32))
        self.ui.btnReport.setIcon(QIcon(confirm_icon_path))

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnDetail.setIconSize(QSize(32, 32))
        self.ui.btnDetail.setIcon(QIcon(confirm_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/compute.png"
        self.ui.btnDownload.setIconSize(QSize(32, 32))
        self.ui.btnDownload.setIcon(QIcon(exe_icon_path))

        exe_icon_path = frozen.app_path() + r"/res/icon/exe.png"
        self.ui.btnPrint.setIconSize(QSize(32, 32))
        self.ui.btnPrint.setIcon(QIcon(exe_icon_path))

    def resetBtn(self):
        self.ui.btnReport.setText('报告单')
        self.ui.btnReport.hide()
        self.ui.btnDownload.hide()
        self.ui.btnPrint.hide()
        self.ui.stackedWidget.setCurrentIndex(1)

    def resetBtn_2(self):
        self.ui.btnNext.show()
        self.ui.btnPre.show()
        self.ui.btnDetail.show()
        self.ui.btnReturn.setGeometry(601, 10, 187, 80)

    def resetBtn_3(self):
        self.ui.btnNext.hide()
        self.ui.btnPre.hide()
        self.ui.btnDetail.hide()

    """
    添加数据至表格显示
    """
    def setHistoryTable(self, cur_page):
        if cur_page == 1:
            self.current_page += 1
        elif cur_page == 2:
            if self.current_page == 0:
                m_title = "错误"
                m_title = ""
                m_info = "已经是第一页!"
                infoMessage(m_info, m_title)
                return
            self.current_page -= 1
        elif cur_page == 3:
            if self.current_page == self.total_page - 1:
                m_title = "错误"
                m_title = ""
                m_info = "已经是最后一页!"
                infoMessage(m_info, m_title)
                return
            self.current_page += 1
        min_page = self.current_page * self.page_size
        self.min_size = self.row_histable - min_page if self.page_size > self.row_histable - min_page else self.page_size
        max_page = self.min_size + self.current_page * self.page_size

        column_histable = len(header_list)
        self.select_table_model = QStandardItemModel(self.page_size, column_histable)

        for i in range(column_histable):
            self.select_table_model.setHeaderData(i, Qt.Horizontal, header_list[i])

        header_view = self.ui.historyTable.horizontalHeader()
        header_view.setStyleSheet("font: 20pt;background-color:#05abc2;")
        ver_view = self.ui.historyTable.verticalHeader()
        ver_view.setStyleSheet("font: 20pt;background-color:#05abc2;")

        self.ui.historyTable.setModel(self.select_table_model)
        self.ui.historyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.ui.historyTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中

        self.ui.historyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.historyTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 插入表格
        # 需要改进
        for i in range(min_page, max_page):
            for j in range(column_histable):
                if j == 1:
                    item = QStandardItem(self.time_list[i])
                elif j == 2:
                    item = QStandardItem(self.patient_id_list[i])
                elif j == 3:
                    # item = QStandardItem(self.patient_name_list[i])
                    item = QStandardItem(self.name_list[i])
                else:
                    item = QStandardItem(self.reagent_id_list[i])
                item.setTextAlignment(Qt.AlignCenter)
                self.select_table_model.setItem(i - self.current_page * self.page_size, j, item)
                # self.select_table_model.setItem(i, j, item)
        for i in range(self.min_size, self.page_size):
            for j in range(column_histable):
                item = QStandardItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.select_table_model.setItem(i, j, item)

        # self.ui.historyTable.currentChanged(self.changePhoto) # 选中时改变图片
        # self.ui.historyTable.selectionModel().currentChanged.connect(self.changePhoto)
        # self.ui.btnDetail.clicked.connect(self.changePhoto)

    """
    查询数据库数据
    需要改进
    """
    def selectMysql(self, time, item_type):
        global header_list
        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = "SELECT * FROM reagent_copy1 WHERE reagent_type = %s AND reagent_time = %s;"

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [item_type, time])
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()

        # 设置历史数据图表
        self.row_histable = cursor.rowcount
        self.column_histable = len(header_list)
        self.page_size = 5  # 每组最大
        self.total_page = math.ceil(self.row_histable / self.page_size)
        self.current_page = -1

        self.time_list = []
        self.patient_id_list = []
        self.reagent_id_list = []
        self.patient_name_list = []
        self.reagent_info = []

        self.name_list = []


        """
        按照数据库数据排序，对数据进行处理
        第四行和第十行为采样时间
        第二行为病人号码
        第五行为试剂卡编号
        """
        for x in cursor.fetchall():
            self.time_list.append(x[3].strftime("%Y-%m-%d") + " " + x[9])
            self.patient_id_list.append(str(x[1]))
            self.reagent_id_list.append(str(x[4]))
            self.reagent_info.append(x[10])
            self.name_list.append(x[11])

        sql = "SELECT * FROM patient_copy1;"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()

        self.patien_info_list = []
        for x in cursor.fetchall():
            self.patien_info_list.append(x)


        for i in self.patient_id_list:
            for j in self.patien_info_list:
                if int(i) == j[3]:
                    self.patient_name_list.append(j[0])

        self.setHistoryTable(1)
        # 释放内存
        cursor.close()
        connection.close()

    """
    实现历史数据图片展示，选中时改变图片
    """
    def changePhoto(self):
        # 点击空白不显示
        current = self.ui.historyTable.currentIndex()
        if current.row() >= self.min_size:
            return

        # self.statusBar().showMessage('选中第{}行'.format(current.row() + 1))

        num = current.row() + self.page_size * self.current_page
        pic_num = self.reagent_id_list[num]

        connection = pymysql.connect(host="127.0.0.1", user="root", password="password", port=3306, database="test",
                                     charset='utf8')
        # MySQL语句
        sql = "SELECT reagent_photo, reagent_type FROM reagent_copy1 WHERE reagent_id = %s"

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [pic_num])
            for i in cursor.fetchall():
                # img_list = ["A","B","C","D"]
                # num = int(i[1])
                # 设置拍照图片显示
                # self.ui.photoLabel.setPixmap(QPixmap("./img/%s/b'%s'.bmp"%(img_list[num], i[0])))
                # self.ui.picLabel.setStyleSheet("QLabel{"
                #                                  "border-image: url(%s/img/%s/b'%s'.bmp); "
                #                                  "font: 20pt; "
                #                                  "color: rgb(255,0,0);}"%(frozen.app_path(), self.time_list[num][:10], i[0]))
                a = frozen.app_path()
                b = self.time_list[num][:10]
                c = i[0]

                # self.ui.picLabel.setPixmap(QPixmap("./img/%s/%s.jpeg"%(b, c)))  # windows环境

                self.ui.picLabel.setStyleSheet("QLabel{"
                                         "border-image: url(%s/img/%s/%s.jpeg); "
                                         "font: 20pt; "
                                         "color: rgb(255,0,0);}"%(a, b, c)) # linux环境
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

        # self.ui.modeBox_1.clear()
        self.ui.modeBox_3.clear()
        # self.ui.modeBox_1.addItems(self.reagent_type)
        # self.ui.modeBox_1.setCurrentIndex(-1)
        # self.ui.typeLabel.setText("")
        self.ui.modeBox_3.addItems(self.reagent_type)
        self.ui.modeBox_3.setCurrentIndex(-1)

        # self.ui.deleteCb.clear()
        # self.ui.deleteCb.addItems(self.reagent_type)
        # self.ui.editCb.clear()
        # self.ui.editCb.addItems(self.reagent_type)

        # 释放内存
        cursor.close()
        connection.close()

    # 设置UI页面
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

    def downLoadToUSB(self):
        # 指定目标目录
        target_dir = '/media/xiao/'

        # 获取U盘设备路径
        try:
            filename = r"/media/xiao/" + os.listdir(target_dir)[0]
        except Exception as e:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)
            return

        # 检查U盘是否已插入
        if os.path.exists(filename):
            # 在U盘根目录下创建示例文件
            file_path = os.path.join(filename, "example.txt")
            with open(file_path, "w") as f:
                msg = "检疫报告单-输出" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                f.write(msg)
            m_title = ""
            m_info = "下载完成！"
            infoMessage(m_info, m_title, 300)
        else:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title)

    @Slot()
    def on_btnConfirm_clicked(self):
        if self.ui.modeBox_3.currentIndex() == -1:
            m_title = ""
            m_info = "未选择试剂卡规格！"
            infoMessage(m_info, m_title, 300)
        else:
            self.resetBtn_2()
            self.ui.btnConfirm.hide()
            self.ui.stackedWidget.setCurrentIndex(1)

            time = "%s-%s-%s" % (
                self.ui.dateBox.date().year(), self.ui.dateBox.date().month(), self.ui.dateBox.date().day())
            # time = self.ui.dateBox.currentText()
            item_type = self.ui.modeBox_3.currentText()
            self.selectMysql(time, item_type)

    @Slot()
    def on_btnPre_clicked(self):
        self.setHistoryTable(2)

    @Slot()
    def on_btnNext_clicked(self):
        self.setHistoryTable(3)

    @Slot()
    def on_btnDetail_clicked(self):
        if self.ui.historyTable.currentIndex().row() == -1:
            m_title = "错误"
            m_title = ""
            m_info = "未选择试剂卡！"
            infoMessage(m_info, m_title, 300)
            return
        else:
            self.resetBtn_3()
            # self.ui.btnReturn.setGeometry(539, 10, 254, 80)
            self.ui.btnReturn.setGeometry(601, 10, 187, 80)
            self.ui.btnReport.show()
            self.ui.btnDownload.show()
            self.ui.btnPrint.show()
            self.ui.stackedWidget.setCurrentIndex(2)
            self.changePhoto()

    @Slot()
    def on_btnPrint_clicked(self):
        reagent_id = self.ui.historyTable.currentIndex().row() + self.page_size * self.current_page

        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # detailwin = childWindow(self.reagent_info[reagent_id], self.time_list[reagent_id], time_now)
        # reagent_info = self.reagent_info[reagent_id]
        test_time = self.time_list[reagent_id]

        myEm5822_Print = Em5822_Print(test_time, time_now)
        myEm5822_Print.em5822_print()
        m_title = ""
        m_info = "输出表格成功!"
        infoMessage(m_title, m_info, 300)

    @Slot()
    def on_btnReport_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 2:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btnReport.setText('图像')
        else:
            self.ui.stackedWidget.setCurrentIndex(2)
            self.ui.btnReport.setText('报告单')

    @Slot()
    def on_btnReturn_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            page_msg = 'homePage'
            self.next_page.emit(page_msg)
        elif self.ui.stackedWidget.currentIndex() == 1:
            self.resetBtn_3()
            self.ui.btnReturn.setGeometry(410, 10, 380, 80)
            self.ui.btnConfirm.show()
            self.ui.stackedWidget.setCurrentIndex(0)
        elif self.ui.stackedWidget.currentIndex() == 2:
            self.resetBtn()
            self.resetBtn_2()
        elif self.ui.stackedWidget.currentIndex() == 3:
            self.resetBtn()
            self.resetBtn_2()

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
