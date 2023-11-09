# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
# 主库
# ----------------------------------------------------------------------------#
import sys
from PIL import Image
import os
import datetime
import time
# import frozen as frozen

# ----------------------------------------------------------------------------#
# 设备库
# ----------------------------------------------------------------------------#
import gxipy as gx
import serial
import serial.tools.list_ports


class Image_Acquire:

    # ---------------------------------------------------#
    #   0 参数设置
    # ---------------------------------------------------#
    def __init__(self, path_cache, path_save):
        #   图像缓存路径
        self.pathCa = path_cache
        #   图像存储路径
        self.pathSa = path_save
        #   设置摄像头分辨率
        Width_max = 5496
        Height_max = 3672
        self.Width_set = 2744  # 5496/2
        self.Height_set = 2500  # 3672/2
        self.OffsetX_set = [8, self.Width_set + 8]
        self.OffsetY_set = [200]
        #   设置缓存图片路径
        self.img_path = [self.pathCa + 'img0.jpeg', self.pathCa + 'img1.jpeg']
        # ---------------------------------------------------#
        #   0.1 摄像头配置初始化
        # ---------------------------------------------------#
       

        # ---------------------------------------------------#
        #   0.2 串口配置初始化
        # ---------------------------------------------------#
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            print("无串口设备。")
        else:
            print("可用的串口设备如下：")
            for comport in ports_list:
                print(list(comport)[0], list(comport)[1])
        self.ser = serial.Serial("/dev/ttyUSB0", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值
        # self.ser = serial.Serial("COM5", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值

    # ---------------------------------------------------#
    #   1 删除缓存图片
    # ---------------------------------------------------#
    def __clear_cache(self):
        for i in os.listdir(self.pathCa):
            os.remove(self.pathCa + "%s" % i)
        print("缓存图片全部删除")

    # ---------------------------------------------------#
    #   2 检测缓存图片
    # ---------------------------------------------------#
    def __img_check(self):
        if len(os.listdir(self.pathCa)) == 2:
            print("图片获取完毕")
            return 1
        else:
            return 0

    # ---------------------------------------------------#
    #   3 获取缓存图片
    # ---------------------------------------------------#
    def img_cache(self):
        self.__clear_cache()
        flag = 0
        # 枚举设备。
        # dev_info_list 是设备信息列表，列表的元素个数为枚举到的设备个数，列表元素是字典，
        # 其中包含设备索引（index）、ip 信息（ip）等设备信息
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            sys.exit(1)
        # 打开设备，获取设备基本信息列表
        strSN = dev_info_list[0].get("sn")
        # 通过序列号打开设备
        cam = device_manager.open_device_by_sn(strSN)
        # 配置摄像头
        cam.Width.set(self.Width_set)
        cam.Height.set(self.Height_set)
        cam.OffsetY.set(self.OffsetY_set[0])
        cam.ExposureTime.set(60000.0)
        while (True):
            write_len = self.ser.write("$810001D".encode('utf-8'))
            #cam.stream_off()
            # 设置偏移值
            cam.OffsetX.set(self.OffsetX_set[flag % 2])
            # 开启采集
            cam.stream_on()
            # 获取一幅图像
            raw_img = cam.data_stream[0].get_image(timeout=3000)
            write_len = self.ser.write("$810011C".encode('utf-8'))
            cam.stream_off()
            # 图像转化
            RGB_img = raw_img.convert("RGB")
            if RGB_img is None:
                continue
            print(flag, '1成功')
            # 将图像数据创建numpy 数组
            numpy_img = RGB_img.get_numpy_array()
            if numpy_img is None:
                continue
            print(flag, '2成功')
            # 显示并保存图像
            img = Image.fromarray(numpy_img, "RGB")
            img.save(self.pathCa + "img%s.jpeg" % flag)
            flag += 1
            print(flag, '3成功')
            if flag == 2 and self.__img_check():
                write_len = self.ser.write("$810011C".encode('utf-8'))
                cam.close_device()
                break
            elif flag > 2:
                flag = 0

    # ---------------------------------------------------#
    #   4 拼接缓存图片
    # ---------------------------------------------------#
    def img_merge(self, name):
        # 获取首张图片
        img = Image.open(self.img_path[0])
        # 获取尺寸
        width, height = img.size
        # 九宫格设置
        target_shape = (2 * width, height)
        target_shape_new = (2 * width, 2 * width)
        # 创建画布
        background = Image.new('L', target_shape)
        background_new = Image.new('L', target_shape_new)
        # 图像拼接
        for i, img_num in enumerate(self.img_path):
            # 读取图像
            image = Image.open(img_num)
            # 改变为统一尺寸
            image = image.resize((width, height))
            # 定位
            location = (i * width, 0 * height)
            # 放置
            background.paste(image, location)
            background_new.paste(background, (0,0))
        # 保存图像
        # background.save(self.pathSa + "%s.jpeg" % name)
        background_new.save(self.pathSa + "%s.jpeg" % name)
        img.close()
        self.__clear_cache()

    # ---------------------------------------------------#
    #   5 串口初始化验证
    # ---------------------------------------------------#
    def serial_init(self):
        write_len = self.ser.write("$4100011".encode('utf-8'))
        data = self.ser.read_all()
        print(data)

    # ---------------------------------------------------#
    #   6 摄像头初始化验证
    # ---------------------------------------------------#
    def camera_init(self):
        print(2)

    # ---------------------------------------------------#
    #   7 获取完整图像
    # ---------------------------------------------------#
    def img_acquire(self, name):
        self.img_cache()
        self.img_merge(name)


if __name__ == '__main__':
    #   参数提供
    path = "./picture/"
    now = datetime.datetime.now()
    time_now = now.strftime("%Y_%m_%d_%H_%M_%S")

    #   初始化
    imgAcq = Image_Acquire(path_cache="./pic_cache/", path_save=path)

    imgAcq.serial_init()
    #   程序调用
    imgAcq.img_acquire(name=time_now)
