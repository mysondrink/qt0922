# 报告单格式化
class MyReport():
    def __init__(self):
        self.html_content = '<!doctype html>\
                            <html>\
                            <head>\
                            <meta charset="utf-8">\
                            </head>\
                            <h1 align="center" style="font-size:20px;font-family:fangsong;">检疫报告单</h1>\
                            <h2 style="font-size:20px;font-family:fangsong;">项目：</h2>\
                            <hr />\
                            <table style="font-size:20px;font-family:fangsong;" border="0" width="800" cellspacing="0" align="center">\
                                <tr align="center">\
                                    <td>姓名：%s</td>\
                                    <td>病历号：%s</td>\
                                    <td>样本类型：%s</td>\
                                    <td>样本编号: %s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>性别：%s</td>\
                                    <td>床号：%s</td>\
                                    <td>采样事件：%s</td>\
                                    <td>条码号: %s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>年龄：%s</td>\
                                    <td>送检医师：%s</td>\
                                    <td>签收时间：%s</td>\
                                </tr>\
                                <tr align="center">\
                                    <td>科室：%s</td>\
                                    <td>备注：%s</td>\
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
                                <tr align="center">\
                                    <td>1.花生</td>\
                                    <td>+</td>\
                                    <td>-</td>\
                                    <td>弱阳</td>\
                                </tr>\
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
                                    <td>此检验报告只对此标本负责，请结合临床。<0.35IU/ml</td>\
                                </tr>\
                                <tr>\
                                    <td>检验日期：%s</td>\
                                    <td>报告时间：%s</td>\
                                    <td>检验者：%s</td>\
                                </tr>\
                            </table>\
                            <hr />\
                            <body>\
                            </body>\
                            </html>\
                            '
    def gethtml(self):
        return self.html_content