# 报告单格式化
class MyReport():
    def __init__(self):
        self.html_content = '<!doctype html>\
                            <html>\
                            <head>\
                            <meta charset="utf-8">\
                            </head>\
                            <h1 align="center" style="font-size:20px;font-family:fangsong;">过敏原检验报告单</h1>\
                            <hr />\
                            <table style="font-size:20px;font-family:fangsong;" border="0" width="800" cellspacing="0" align="center">\
                                <tr align="center">\
                                    <td>姓名：%s</td>\
                                    <td>性别：%s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>样本号：%s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>条码号：%s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>样本类型：%s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>测试时间：%s</td>\
                                </tr>\
                            </table>\
                            <hr />\
                            <table style="font-size:20px;font-family:fangsong;" border="0" width="800" cellspacing="0" align="center">\
                                <tr align="center">\
                                    <td>过敏原</td>\
                                    <td>结果</td>\
                                    <td>参考值</td>\
                                    <td>结果解释</td>\
                                </tr>\
                                %s\
                            </table>\
                            <hr />\
                            <table style="font-size:20px;font-family:fangsong;" border="0" width="800" cellspacing="0" align="center">\
                                <tr>\
                                    <td>注</td>\
                                </tr>\
                                <tr>\
                                    <td>“-”为阴性，＜0.35IU/mL</td>\
                                </tr>\
                                <tr>\
                                    <td>“+”为弱性，0.35IU/mL-3.5IU/mL</td>\
                                </tr>\
                                <tr>\
                                    <td>“++”为中性，3.5IU/mL-17.5IU/mL</td>\
                                <tr>\
                                    <td>“+++”为强阳，≥17.5IU/mL</td>\
                                </tr>\
                            </table>\
                            <hr />\
                            <table style="font-size:20px;font-family:fangsong;" border="0" width="800" cellspacing="0" align="center">\
                                <tr>\
                                    <td>打印时间：%s</td>\
                                </tr>\
                                <tr>\
                                    <td>此检验报告只对此标本负责，请结合临床。</td>\
                                </tr>\
                            </table>\
                            <hr />\
                            <body>\
                            </body>\
                            </html>\
                            '
        
    def gethtml(self, item_type, reagent_info, nature_aver_str):
                    #         if g_arr[i][j] < 60000:
                    #     n_arr[i][j] = "阴性"
                    #     n_arr_flag[i][j] = "-"
                    # elif g_arr[i][j] < 660000:
                    #     n_arr[i][j] = "弱阳性"
                    #     n_arr_flag[i][j] = "+"
                    # elif g_arr[i][j] < 1100000:
                    #     n_arr[i][j] = "中阳性"
                    #     n_arr_flag[i][j] = "++"
                    # elif g_arr[i][j] > 1100000:
                    #     n_arr[i][j] = "强阳性"
                    #     n_arr_flag[i][j] = "+++"
                    # else:
                    #     n_arr[i][j] = "error"
                    #     n_arr_flag[i][j] = "error"
        result_dict = {"阴性":"-","中阳性":"++", "强阳性":"+++","弱阳性":"+"}
        result_list_1 = [result_dict.get(i) for i in nature_aver_str.split(",")[5:]]
        result_list_2 = [i for i in nature_aver_str.split(",")[5:]]
        num = []
        reagent_info_list_1 = [i for i in reagent_info.split(",")]
        reagent_info_list_2 = [reagent_info_list_1[k:k+5] for k in [j for j in range(0, 55, 5)] if k % 15 == 0]
        reagent_info_list_3 = [i for i in sum(reagent_info_list_2, []) if i != '']
        if item_type == 'D':
            item_len = 14
            result_list_3 = [result_list_1[0]] + [j for j in [result_list_1[i] for i in range(0, len(result_list_1), 2) if i % 5 != 0] if j != None]
            result_list_4 = [result_list_2[0]] + [j for j in [result_list_2[i] for i in range(0, len(result_list_2), 2) if i % 5 != 0] if j != '0']
            # result_list_3 = [result_list_1[i] for i in range(1, len(result_list_1), 2) if i % 5 != 0]
            # result_list_4 = [result_list_2[i] for i in range(1, len(result_list_2), 2) if i % 5 != 0]
            # special
            index = 9
            result_list_3.insert(index, result_dict.get(result_list_1[index]))
            result_list_4.insert(index, result_list_2[index])
        else:
            item_len = 20
            result_list_3 = [j for j in [result_list_1[i] for i in range(0, len(result_list_1), 2)] if j != None]
            result_list_4 = [j for j in [result_list_2[i] for i in range(0, len(result_list_2), 2)] if j != '0'] 
        # 姓名，性别，样本号，条码号，样本类型，测试时间，【结果】，打印时间
        temp = '<tr align="center">\
                <td>%s</td>\
                <td>%s</td>\
                <td><0.35</td>\
                <td>%s</td>\
                </tr>'
        temp_str = ""
        for j in range(item_len):
            str_temp = temp
            temp_str = temp_str + str_temp % (reagent_info_list_3[j], result_list_3[j], result_list_4[j])
        return self.html_content, temp_str