import math
import operator
import time
import numpy as np
import cv2 as cv
import os
from PIL import Image

#   定位点圈定区域，可修改
roi_position = [
    [0, 700], [0, 2500]  # [startY, endY] [StartX, endX]
]


class Image_Processing:

    # --------------------------------------------------- #
    #   0 参数设置
    # --------------------------------------------------- #
    def __init__(self, roi_position):
        #   定位点的兴趣区间
        self.__roiPos = roi_position

    # --------------------------------------------------- #
    #   1.1 计算直线的垂足
    # --------------------------------------------------- #
    def __get_foot(self, start_point, middle_point, end_point):
        '''
                start_point     --输入直线的起始点，（x， y)
                middle_point    --输入直线外的中间点，用于计算垂足，（x， y）
                end_point       --输入直线的终止点，（x， y）
                return          --输出垂足点（x，y）
                '''
        #   初始化垂足点
        point_foot = [0, 0]
        #   当直线与X轴垂直
        if start_point[0] == end_point[0]:
            point_foot = [start_point[0], middle_point[1]]
            return point_foot
        #   当直线与X轴平行
        elif start_point[1] == end_point[1]:
            point_foot = [middle_point[0], start_point[1]]
            return point_foot
        #   计算斜率
        k = (end_point[1] - start_point[1]) * 1.0 / (end_point[0] - start_point[0])
        a = k
        b = -1.0
        c = start_point[1] - k * start_point[0]
        #   计算垂直点
        point_foot[0] = (b * b * middle_point[0] - a * b * middle_point[1] - a * c) / (a * a + b * b)
        point_foot[1] = (a * a * middle_point[1] - a * b * middle_point[0] - b * c) / (a * a + b * b)
        return point_foot

    # --------------------------------------------------- #
    #   1.2 图像旋转
    # --------------------------------------------------- #
    def __rotate_img(self, img, angle):
        '''
                    img     --输入图像
                    angle   --旋转角度
                    return  --返回图像
                    '''
        h, w = img.shape[:2]
        rotate_center = (w / 2, h / 2)
        #   获取旋转矩阵
        #   参数1为旋转中心点；
        #   参数2为旋转角度，正值-逆时针旋转；负值-顺时针旋转；
        #   参数3为各向同性的比例因子，1.0原图，2.0变成原来的2倍，0.5变成原来的0.5倍
        M = cv.getRotationMatrix2D(rotate_center, angle, 1.0)
        #   计算图像新边界
        new_w = int(h * np.abs(M[0, 1]) + w * np.abs(M[0, 0]))
        new_h = int(h * np.abs(M[0, 0]) + w * np.abs(M[0, 1]))
        #   调整旋转矩阵以考虑平移
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2

        rotated_img = cv.warpAffine(img, M, (new_w, new_h))
        return rotated_img

    # --------------------------------------------------- #
    #   1.3 试剂点位置转换,list->tuple
    # --------------------------------------------------- #
    def __gray_pos(self, img, data, reference):
        '''
                data        --相对于参考点，试剂点位置
                reference   --参考点实际位置
                return      --试剂点实际位置
                '''
        out_data = np.array(data)
        for i in range(np.array(data).shape[0]):
            for j in range(np.array(data).shape[1]):
                if data[i][j] == [0, 0]:
                    continue
                out_data[i][j] = np.array(data[i][j]) + np.array(reference)
        return out_data

    # --------------------------------------------------- #
    #   1.4 获取范围内灰度值总和
    # --------------------------------------------------- #
    def __sum_gray(self, img, x, y, radius):
        '''
                img     --图像转化为灰度数值
                x       --横轴坐标
                y       --纵轴坐标
                radius  --圈定区域半径
                return  --圈定区域灰度均值
                '''
        gray_number = 0  # 获取灰度像素个数
        gray_sum = 0  # 获取灰度像素数值总和
        gray_ThresholdValue = 35  # 灰度阈值
        x_InitialPoint = x - radius  # 横向初始值
        y_InitialPoint = y - radius  # 纵向初始值
        #   查看圈定灰度区域是否超过阈值
        if (x + radius) >= img.shape[0] or (y + radius) >= img.shape[1]:
            return 0
        else:
            # 遍历区域内符合要求的像素点
            for i in range(radius * 2 + 1):
                for j in range(radius * 2 + 1):
                    if img[x_InitialPoint + i, y_InitialPoint + j] >= gray_ThresholdValue:
                        gray_number += 1
                        gray_sum += img[x_InitialPoint + i, y_InitialPoint + j]
                    else:
                        continue
        return gray_sum  # 灰度值总和

    # ---------------------------------------------------#
    #   1.5 删除缓存图片
    # ---------------------------------------------------#
    def __clear_cache(self, path):
        os.remove(path)

    # --------------------------------------------------- #
    #   2.1 图像预处理
    # --------------------------------------------------- #
    def img_pre(self, path_read, num_dst):
        #   读取原始图像
        img_original = cv.imread(path_read)
        #   顺时针旋转90度
        (w, h) = img_original.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, -90, 1.0)
        img_original = cv.warpAffine(img_original, M, (w, h))
        #   圈定图像获取区域
        img_original = img_original[0:w, (h - 2500):h]
        # img_original = img_original[0:(w - 3000), (h - 2500):h]
        #   保留原始图像
        img = cv.cvtColor(img_original, cv.COLOR_RGB2GRAY)
        #   灰度化
        img_gray = cv.cvtColor(img_original, cv.COLOR_RGB2GRAY)
        #   二值化图像
        ret, img_thres = cv.threshold(img_gray, num_dst, 255, cv.THRESH_BINARY)
        #   图像腐蚀
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        img_dst1 = cv.erode(img_thres, kernel)
        #   图像膨胀
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (11, 11))
        img_dst2 = cv.dilate(img_dst1, kernel)

        return img, img_gray, img_dst2  # 原始图像,  二值化图像

    # --------------------------------------------------- #
    #   2.2 获取图像中定位点位置
    # --------------------------------------------------- #
    def img_pos_point(self, img_dst, img_gray, num, flag):
        # 参数设置
        num_down = 0
        len_down = 400  # 单次下移量
        circle_x = []
        circle_y = []
        for i in range(num):
            num_down = len_down * i  # 总下移量
            #   获取ROI感兴趣区间
            img_ROI = img_dst[(self.__roiPos[0][0] + num_down):(self.__roiPos[0][1] + num_down),
                      self.__roiPos[1][0]:self.__roiPos[1][1]]
            circle = cv.HoughCircles(img_ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
            #   当前ROI未找到定位点
            if (circle is None) or (circle.shape[1] < 3):
                continue
            #   当前ROI找到全部定位点
            elif circle.shape[1] >= 3:
                if flag == 1:
                    # 圈定ROI区域
                    cv.rectangle(img_gray, pt1=(self.__roiPos[1][0], self.__roiPos[0][0] + num_down + 100),
                                 pt2=(self.__roiPos[1][1], self.__roiPos[0][1] + num_down - 100), color=(0, 0, 0),
                                 thickness=20)
                #   定位点坐标+ROI定位区间
                for i in range(circle.shape[1]):
                    circle[0][i][0] = circle[0][i][0] + self.__roiPos[1][0]
                    circle[0][i][1] = circle[0][i][1] + self.__roiPos[0][0] + num_down
                #   定位点坐标划分为x，y
                for j in circle[0, :]:
                    cv.circle(img_gray, (int(j[0]), int(j[1])), int(j[2]), (0, 0, 0), 10)
                    circle_x.append(j[0])
                    circle_y.append(j[1])

                diff_x1 = np.diff(circle_y)
                if abs(diff_x1[0]) > 200 or abs(diff_x1[1]) > 200:
                    return 0, img_gray, 0, 0, 0
                return 1, img_gray, circle, circle_x, circle_y
        if flag == 1:
            # 圈定ROI区域
            cv.rectangle(img_gray, pt1=(self.__roiPos[1][0], self.__roiPos[0][0] + num_down),
                         pt2=(self.__roiPos[1][1], self.__roiPos[0][1] + num_down), color=(0, 0, 0),
                         thickness=20)
        # 未找到定位点
        return 0, img_gray, 0, 0, 0

    # --------------------------------------------------- #
    #   2.3 矫正图像角度
    # --------------------------------------------------- #
    def img_correct(self, img_gray, img_dst, circle, circle_x, circle_y):
        circle_point_x = []
        circle_point_y = []
        point = [0] * 5
        min_index, min_number = min(enumerate(circle_x), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(circle_x), key=operator.itemgetter(1))
        middle_index = None
        for i in range(3):
            if i == min_index or i == max_index:
                continue
            else:
                middle_index = i

        #   计算直线上的垂足点与中间点的角度，然后根据角度旋转图像
        angle = math.atan2(circle_y[max_index] - circle_y[min_index], circle_x[max_index] - circle_x[min_index])
        angle = angle * 180 / math.pi
        img_rota = self.__rotate_img(img_gray, angle)
        img_rota_dst = self.__rotate_img(img_dst, angle)

        #   二次定位点，参考点位置
        TJW = int(circle[0, :][middle_index][1])

        #   第二次寻找定位点，确定其位置
        img_ROI = img_rota_dst[(TJW - 200):(TJW + 200), 0:2500]
        circle_point = cv.HoughCircles(img_ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                       maxRadius=150)

        #   将二次定位划分成x，y
        if (circle is None) or (circle.shape[1] < 3):
            return img_rota, img_rota_dst, point, 0
        for i in circle_point[0, :]:
            circle_point_x.append(i[0])
            circle_point_y.append(i[1])

        #   寻找二次定位点的最大值和最小值
        min_new, min_number = min(enumerate(circle_point_x), key=operator.itemgetter(1))
        max_new, max_number = max(enumerate(circle_point_x), key=operator.itemgetter(1))
        mid_new = None
        for i in range(3):
            if i == min_new or i == max_new:
                continue
            else:
                mid_new = i

        # print(circle_point_x)
        #   找到试剂点x轴的坐标数值
        point[0] = int(circle_point_x[min_new])
        point[1] = int(circle_point_x[min_new] + (circle_point_x[mid_new] - circle_point_x[min_new]) / 2)
        point[2] = int(circle_point_x[mid_new])
        point[3] = int(circle_point_x[mid_new] + (circle_point_x[max_new] - circle_point_x[mid_new]) / 2)
        point[4] = int(circle_point_x[max_new])

        #   找到Y轴定位点以下区域
        reference_point = int(circle_point_y[mid_new] - 200 + TJW + 150)

        # cv.rectangle(img_rota, pt1=(point[0] - 150, reference_point), pt2=(point[0] + 150, 5000), color=(0, 0, 0),
        #              thickness=10)

        # print(reference_point)

        return img_rota, img_rota_dst, point, reference_point

    # --------------------------------------------------- #
    #   2.4 获取试剂点灰度值
    # --------------------------------------------------- #
    def img_get_gray(self, img_rota, img_rota_dst, gray_aver, point_x, re_point, radius):

        #   圈定试剂点5个区域
        t = 0
        ROI_0 = img_rota_dst[re_point:5000, (point_x[t] - 150):(point_x[t] + 150)]
        t = 1
        ROI_1 = img_rota_dst[re_point:5000, (point_x[t] - 150):(point_x[t] + 150)]
        t = 2
        ROI_2 = img_rota_dst[re_point:5000, (point_x[t] - 150):(point_x[t] + 150)]
        t = 3
        ROI_3 = img_rota_dst[re_point:5000, (point_x[t] - 150):(point_x[t] + 150)]
        t = 4
        ROI_4 = img_rota_dst[re_point:5000, (point_x[t] - 150):(point_x[t] + 150)]

        #   找出显示的试剂点
        circle_0 = cv.HoughCircles(ROI_0, cv.HOUGH_GRADIENT, 0.5, 100, param1=100, param2=8, minRadius=70,
                                   maxRadius=150)
        circle_1 = cv.HoughCircles(ROI_1, cv.HOUGH_GRADIENT, 0.5, 100, param1=100, param2=8, minRadius=70,
                                   maxRadius=150)
        circle_2 = cv.HoughCircles(ROI_2, cv.HOUGH_GRADIENT, 0.5, 100, param1=100, param2=8, minRadius=70,
                                   maxRadius=150)
        circle_3 = cv.HoughCircles(ROI_3, cv.HOUGH_GRADIENT, 0.5, 100, param1=100, param2=8, minRadius=70,
                                   maxRadius=150)
        circle_4 = cv.HoughCircles(ROI_4, cv.HOUGH_GRADIENT, 0.5, 100, param1=100, param2=8, minRadius=70,
                                   maxRadius=150)

        # print(circle_0)
        # print(circle_1)
        # print(circle_2)
        # print(circle_3)
        # print(circle_4)

        if (circle_0 is None) and (circle_1 is None) and (circle_2 is None) and (circle_3 is None) and (
                circle_4 is None):
            return gray_aver, img_rota, 0

        #   定位每个试剂点的Y轴坐标
        row_num = 0
        circle0 = []
        if circle_0 is not None:
            t = 0
            row_num += 1
            for i in circle_0[0, :]:
                if i[0] <= 180 and i[0] >= 120:
                    # cv.circle(img_rota, (int(i[0]) + point_x[t] - 150, int(i[1]) + re_point), int(i[2]), (0, 0, 0), 10)
                    circle0.append(i[1])

        circle1 = []
        if circle_1 is not None:
            t = 1
            row_num += 1
            for i in circle_1[0, :]:
                if i[0] <= 180 and i[0] >= 120:
                    # cv.circle(img_rota, (int(i[0]) + point_x[t] - 150, int(i[1]) + re_point), int(i[2]), (0, 0, 0), 10)
                    circle1.append(i[1])

        circle2 = []
        if circle_2 is not None:
            t = 2
            row_num += 1
            for i in circle_2[0, :]:
                if i[0] <= 180 and i[0] >= 120:
                    # cv.circle(img_rota, (int(i[0]) + point_x[t] - 150, int(i[1]) + re_point), int(i[2]), (0, 0, 0), 10)
                    circle2.append(i[1])

        circle3 = []
        if circle_3 is not None:
            t = 3
            row_num += 1
            for i in circle_3[0, :]:
                if i[0] <= 180 and i[0] >= 120:
                    # cv.circle(img_rota, (int(i[0]) + point_x[t] - 150, int(i[1]) + re_point), int(i[2]), (0, 0, 0), 10)
                    circle3.append(i[1])

        circle4 = []
        if circle_4 is not None:
            t = 4
            row_num += 1
            for i in circle_4[0, :]:
                if i[0] <= 180 and i[0] >= 120:
                    # cv.circle(img_rota, (int(i[0]) + point_x[t] - 150, int(i[1]) + re_point), int(i[2]), (0, 0, 0), 10)
                    circle4.append(i[1])

        # if ((len(circle0) >= 2) or (len(circle1) >= 2) or (len(circle2) >= 2) or (len(circle3) >= 2) or (len(circle4) >= 2)) is False:
        #     return gray_aver, img_rota , 0
        # print(circle0)
        # print(circle1)
        # print(circle2)
        # print(circle3)
        # print(circle4)

        #   找出所有试剂点中，最大值和最小值
        min_num = []
        max_num = []
        value = 0
        if len(circle0) >= 2:
            circle0.sort()
            value = circle0[1] - circle0[0]
            min_num.append(circle0[0])
            circle0.sort(reverse=True)
            max_num.append(circle0[0])

        if len(circle1) >= 2:
            circle1.sort()
            min_num.append(circle1[0])
            circle1.sort(reverse=True)
            max_num.append(circle1[0])

        if len(circle2) >= 2:
            circle2.sort()
            min_num.append(circle2[0])
            circle2.sort(reverse=True)
            max_num.append(circle2[0])

        if len(circle3) >= 2:
            circle3.sort()
            min_num.append(circle3[0])
            circle3.sort(reverse=True)
            max_num.append(circle3[0])

        if len(circle4) >= 2:
            circle4.sort()
            min_num.append(circle4[0])
            circle4.sort(reverse=True)
            max_num.append(circle4[0])

        if (len(min_num) < 1) or (len(max_num) < 1):
            return gray_aver, img_rota, 0

        min_num.sort()
        max_num.sort(reverse=True)

        if value < 270:
            value = 300
        server_num = (max_num[0] - min_num[0]) / value
        # print(server_num)
        server = int((max_num[0] - min_num[0]) / int(server_num + 0.5))

        point_y = []
        for i in range(8):
            point_y.append(min_num[0] + server * i)

        #   获取试剂点的灰度值
        img_array = np.transpose(np.array(img_rota))
        for i in range(5):
            for j in range(8):
                cv.circle(img_rota, (int(point_x[i]), int(point_y[j] + re_point)), 50, (0, 0, 0), 10)
                gray_aver[j][i] = self.__sum_gray(img_array, int(point_x[i]), int(point_y[j] + re_point), radius)

        # print(point_x)
        # print(point_y)

        return gray_aver, img_rota, 1

    # --------------------------------------------------- #
    #   3 图像处理全流程
    # --------------------------------------------------- #
    def process(self, path_read, path_write, reagent, radius):

        #   参数设置
        gray_aver = np.zeros(reagent)  # 输出参数
        #   2.1 图像预处理
        img_ori, img_gray, img_dst = self.img_pre(path_read, 120)
        #   保存原始图像
        cv.imwrite(path_write + 'img_0ori.jpeg', img_ori)
        #   保存二值化图像
        cv.imwrite(path_write + 'img_1dst.jpeg', img_dst)
        cv.imwrite(path_write + 'img_final.jpeg', img_ori)

        # self.__clear_cache(path_read)

        #   2.2 获取图像中定位点位置
        judge, img_gray, circle, circle_x, circle_y = self.img_pos_point(img_dst, img_gray, num=4, flag=1)
        #   保存ROI感兴趣区间
        cv.imwrite(path_write + 'img_2ROI.jpeg', img_gray)

        #   未检测定位点，退出
        if judge == 0:
            #   参数设置
            gray_aver = np.zeros(reagent)  # 输出参数
            #   2.1 图像预处理
            img_ori, img_gray, img_dst = self.img_pre(path_read, 80)
            #   2.2 获取图像中定位点位置
            judge_new, img_gray, circle, circle_x, circle_y = self.img_pos_point(img_dst, img_gray, num=4, flag=1)

            if judge_new == 0:
                print("未检测到定位点")
                cv.imwrite(path_write + 'img_final.jpeg', img_gray)
                return 0, gray_aver
        cv.imwrite(path_write + 'img_final.jpeg', img_gray)

        #   2.3 矫正图像角度
        img_rota, img_rota_dst, point_x, re_point = self.img_correct(img_gray, img_dst, circle, circle_x, circle_y)
        cv.imwrite(path_write + 'test.jpeg', img_rota_dst)

        gray_aver, img_rota, judge_1 = self.img_get_gray(img_rota, img_rota_dst, gray_aver, point_x, re_point, radius)
        #   未检测到试剂点
        if judge_1 == 0:
            img_ori, img_gray, img_dst = self.img_pre(path_read, 80)
            cv.imwrite(path_write + 'img_1dst.jpeg', img_dst)
            img_rota, img_rota_dst, point_x, re_point = self.img_correct(img_gray, img_dst, circle, circle_x, circle_y)
            gray_aver, img_rota, judge_1 = self.img_get_gray(img_rota, img_rota_dst, gray_aver, point_x, re_point,
                                                             radius)

        cv.imwrite(path_write + 'img_3out.jpeg', img_rota)
        cv.imwrite(path_write + 'img_final.jpeg', img_rota)

        # print(gray_aver)
        return 1, gray_aver


if __name__ == '__main__':
    imgPro = Image_Processing(
        roi_position=roi_position
    )

    imgPro.process(path_read='picture/2023_08_25_14_21_13.jpeg', path_write='./img_out/', reagent=(8, 5),
                   radius=40)
