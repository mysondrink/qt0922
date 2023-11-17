import pymysql
import random
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class mymysql():
    def __init__(self) -> None:
        pass

    def insertMysql(self, name_pic, cur_time):
        # reagent_matrix_info = str(self.readPixtable())
        reagent_matrix_info = "reagent_matrix_info"

        patient_id = random.randint(1000, 1999)

        # name_id = random.randint(1,199)
        # patient_name = self.name_file[name_id].get("name")
        # patient_age = self.name_file[name_id].get("age")
        # patient_gender = self.name_file[name_id].get("gender")

        patient_name = "patient_name"
        patient_age = "patient_age"
        patient_gender = "patient_gender"

        item_type = "item_type"
        pic_name = name_pic

        # 时间进行切片
        time = cur_time.split()

        doctor = "doctor"
        depart = "depart"
        age = "age"
        gender = "gender"
        name = "name"

        matrix = "matrix"
        code_num = random.randint(1000, 2000)

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

def main():
    my_mysql = mymysql()
    for i in range(3):
        name_pic = "test" + str(i)
        cur_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        my_mysql.insertMysql(name_pic, cur_time)

if __name__=="__main__":
    main()


