"""
@Description：上传数据线程类
@Author：mysondrink@163.com
@Time：2024/1/19 15:36
"""
import sys
import traceback
from PySide2.QtCore import QThread, Signal
import pymysql
import pandas as pd
import numpy as np
import os

time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202


class UploadThread(QThread):
    update_json = Signal()
    finished = Signal()


    def __init__(self, file_path='./res/new_data.xlsx'):
        super().__init__()
        sys.excepthook = self.HandleException
        self.file_path = file_path

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

    def run(self):
        csv_data = []
        id_data = []
        reagent_data = []
        status_data = []
        input_table = pd.read_excel(self.file_path, sheet_name="Sheet2")
        input_table_rows = input_table.shape[0]
        # input_table_columns = input_table.shape[1]
        # input_table_header = input_table.columns.values.tolist()
        for i in range(input_table_rows):
            input_table_rows_values = input_table.iloc[[i]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            csv_data.append(input_table_rows_values_list)
            id_data.append(input_table_rows_values_list[1])
            reagent_data.append(input_table_rows_values_list[-2])
            status_data.append(input_table_rows_values_list[-1])
        self.insertMysql(id_data, status_data, *self.filterReagentData(reagent_data))
        # ["序号", "图片名称", "时间", "样本条码", "医生", "类别",
        #  "阵列", "病人名", "病人性别", "病人年龄", "数据", "status"]
        # [id_num, name_pic, cur_time, code_num, doctor, reagent_type,
        #  reagent_matrix, name, gender, age, reagent_matrix_info]

    def filterReagentData(self, data):
        reagent_info_list = []
        points_list = []
        gray_aver_list = []
        for i in data:
            temp = i.split(",")
            points_list.append(",".join(i for i in temp[0:5]))
            reagent_info_list.append(",".join(i for i in temp[5:]))
            b = temp[10:]
            c = [b[k:k+10] for k in [j for j in range(0, 55, 15)]]
            str_list = []
            for j in [i for i in c]:
                str_list = str_list + [i for i in j]
            gray_aver_list.append(",".join(str_list))
        return reagent_info_list, points_list, gray_aver_list

    def insertMysql(self, id_list, status_list, reagent_info_list, points_list, gray_aver_list):
        db = pymysql.connect(host="localhost", user="root", password="password", database="test")  # 本机数据库连接

        # 远程连接数据库
        # db = pymysql.connect(
        #     host='192.168.100.110',
        #     port=3306,
        #     user='root',
        #     passwd='123456',
        #     db='库名',
        #     charset='utf8'
        # )

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        for i, j in zip(id_list, range(len(id_list))):
            if status_list[j] == 0:
                break
            # MySQL语句
            sql = 'UPDATE reagent_copy1_copy1 SET reagent_matrix_info = %s , gray_aver = %s, points = %s ' \
                  'WHERE reagent_photo = %s'
            # print(sql)  # 查看SQL语句是否正确
            try:
                cursor.execute(sql, [reagent_info_list[j], gray_aver_list[j], points_list[j], i])  # 执行sql语句

                db.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
                print('新增' + str(j) + "数据")
            except Exception as e:
                print(e)
                db.rollback()  # 发生错误时回滚
                print("数据添加失败")

        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接
        self.finished.emit()

    def deleteFile(self):
        os.remove(self.file_path)
