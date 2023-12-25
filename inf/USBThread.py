from PySide2.QtCore import QThread, Signal, QDateTime
import sys
import traceback
import os
import cv2 as cv

import frozen as frozen
from utils import dirs

time_to_sleep = 2
trylock_time = -1
failed_code = 404
succeed_code = 202


class CheckUSBThread(QThread):
    update_json = Signal(int)
    update_log = Signal(str)

    """
    @detail 初始化线程，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self, name, path, parent=None):
        super().__init__(parent)
        sys.excepthook = self.HandleException
        self.name_pic = name
        self.pic_path = path

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
    @detail u盘下载运行函数
    @detail 进行u盘下载
    """
    def run(self):
        try:
            self.downLoadToUSB()
        except Exception as e:
            self.sendException()
            self.update_json.emit(failed_code)

    """
    @detail 下载信息到u盘
    @detail 下载内容包括图片、数据库信息
    """
    def downLoadToUSB(self):
        # 指定目标目录
        target_dir = '/media/orangepi/orangepi/'
        # 获取U盘设备路径
        try:
            u_name = r"/media/orangepi/orangepi/" + os.listdir(target_dir)[0] + "/"
        except Exception as e:
            self.sendException()
            self.update_json.emit(failed_code)
            return
        # 检查U盘是否已插入
        timenow = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        save_dir = u_name + timenow + "/"
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
                # name_pic = self.data['name_pic']
                # pic_path = self.data['pic_path']
                img_origin = cv.imread('%s\\img\\%s\\%s-1.jpeg' % (frozen.app_path(), self.pic_path, self.name_pic)) # windows
                # img_final = cv.imread('%s/img/%s/%s-1.jpeg' % (frozen.app_path(), pic_path, name_pic)) # linux
                flag_bool = cv.imwrite(save_img_path_1, img_origin)

                img_final = cv.imread('%s\\img\\%s\\%s-2.jpeg' % (frozen.app_path(), self.pic_path, self.name_pic)) # windows
                # img_final = cv.imread('%s/img/%s/%s-2.jpeg' % (frozen.app_path(), pic_path, name_pic)) # linux
                flag_bool = cv.imwrite(save_img_path_2, img_final)
            except Exception as e:
                self.sendException()
                self.update_json.emit(failed_code + 1)
            self.update_json.emit(succeed_code)
        else:
            self.update_json.emit(failed_code)