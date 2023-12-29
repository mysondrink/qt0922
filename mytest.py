import pymysql
import random
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os

class mymysql():
    def __init__(self) -> None:
        pass

    def insertMysql(self, name_pic, cur_time):
                # 指定目标目录
        target_dir = '/media/orangepi/orangepi/'

        # 获取U盘设备路径
        try:
            filename = r"/media/orangepi/orangepi/" + os.listdir(target_dir)[0] + "/"
        except Exception as e:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            print(m_info)
            return

            # 检查U盘是否已插入
        if os.path.exists(filename):
            # 在U盘根目录下查找指定文件
            file_path = os.path.join(filename, "example.txt")
            if os.path.exists(file_path):
                # 读取文件内容并打印到控制台
                f = open(file_path, 'r', encoding="utf-8")
                lines = f.readlines()
                for i in range(len(lines)):
                    num = float(lines[i])
                    print(num)
                m_title = ""
                m_info = "上传成功"
                # infoMessage(m_info, m_title, 300)
                print(m_info)
            else:
                # print("文件不存在")
                m_title = ""
                m_info = "文件不存在!"
                # infoMessage(m_info, m_title, 300)
                print(m_info)
        else:
            # print("U盘未插入或无法访问")
            m_title = ""
            m_info = "U盘未插入或无法访问!"
            # infoMessage(m_info, m_title, 240)
            print(m_info)

def main():
    my_mysql = mymysql()
    my_mysql.insertMysql()

if __name__=="__main__":
    main()


