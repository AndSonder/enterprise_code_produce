"""
企业编码管理界面
"""
from bll import *
import os


class EnterpriseCodeView:
    def __init__(self):
        self.__create = EnterpriseCodeProduce()
        self.__message = EnterpriseCodeControl()

    def __display_menu(self):
        """
        打印出视图菜单
        """
        print("""
        **********************************************************
                            企业编码生成系统
        **********************************************************
            1.生成6位数字防伪编码（324654型）
            2.生成9位系列产品数字防伪编码（876-456346型）
            3.生成25位混合产品序列号（BAS49-A99AE-ASDA7- IUY7A型）
            4.生成含有数字分析功能的防伪码
            5.EAN-13条形码批量输出
            6.普通二维码批量输出
            7.内容二维码输出（单个）(可以是网址也可以是其他内容）
            0.退出系统
        ==========================================================
        说明：通过数字键选择菜单
        ==========================================================
        """)

    def __select_menu(self):
        """
        选择菜单
        """
        item = input("请输入您的选择：")
        if item == "1":
            self.__print_menu(1)
            self.__get_code(6, self.__create.produce_random_code)
        elif item == "2":
            self.__print_menu(2)
            self.__get_code02(self.__create.produce_nine_code, 9)
        elif item == "3":
            self.__print_menu(3)
            self.__get_code(25, self.__create.produce_twenty_five_code)
        elif item == "4":
            self.__print_menu(4)
            self.__get_code02(self.__create.produce_data_analysis_code, 0)
        elif item == "5":
            self.__print_menu(5)

            count, country_code, enterprise_code = self.__input_message()
            self.__get_many_dar_or_QR_code(count, country_code, enterprise_code, "barcode")
        elif item == "6":
            self.__print_menu(6)
            count, country_code, enterprise_code = self.__input_message()
            self.__get_many_dar_or_QR_code(count, country_code, enterprise_code, "qrcode")
        elif item == "7":
            self.__print_menu(7)
            self.__get_QR_code()
        elif item == "0":
            print("感想您的使用")
            # 退出程序
            os._exit(1)

        else:
            print("请输入正确的数字")

    @staticmethod
    def __input_message():
        count = int(input("请输入条形码的数量"))
        country_code = input("请输入国家代码")
        enterprise_code = input("请输入企业代码")
        return count, country_code, enterprise_code

    def main(self):
        """
            界面视图入口
        """
        while True:
            self.__display_menu()
            self.__select_menu()

    def __get_code(self, number, method):
        """
        生成防伪码,可生成6位和25位防伪码
        :param number: 生成防伪码的位数
        :param method: 所用的方法
        """
        # 输入要生成的防伪码数量
        count = int(input("请输入数量"))
        # 调用方法生成并保存防伪码
        self.__message.batch_generator(count, method, "codepath\\%d_code.txt" % number)
        # 打印文件所在地址
        self.__message.print_address("\\codepath\\%d_code.txt" % number, "您的%d位数防伪码已经保存到" % number)
        # 检查文件中是否有重复代码
        self.__message.check("codepath\\%d_code.txt" % number, method)

    def __get_code02(self, method, number):
        """
        生成防伪码
        可生成9位防伪码，带有数字分析功能的防伪码，EAN-13条形码
        :param method: 所用的方法
        :param number: 生成防伪码的位数
        """
        # 输入要生成的防伪码数量
        count = int(input("请输入数量"))
        # 输入信息
        message = input("请输入相关信息")
        # 对输入的信息个数筛选
        message = self.__message_text(message, number)
        for item in range(count):
            str_code = method(message)
            # 保存防伪码
            self.__message.save_code(str_code, "codepath\\%d_code.txt" % number)
        # 检查生成的防伪码中有没有重复的
        self.__message.check("codepath\\%d_code.txt" % number, method, message)
        # 打印文件所在地址
        self.__message.print_address("\\codepath\\%d_code.txt" % number, "您的%d位数防伪码已经保存到" % number)

    @staticmethod
    def __message_text(message, number):
        """
        检验输入的信息是否合格
        :param message: 输入的信息
        """
        while True:
            if number == 9:
                if message.isdigit() and len(message) == 3:
                    break
                else:
                    message = input("请输入正确的相关信息")
            elif number == 0:
                if message.isalpha() and len(message) == 3:
                    break
                else:
                    message = input("请输入正确的相关信息")
        return message

    def __get_many_dar_or_QR_code(self, count, country_code, enterprise_code, select_code):
        """
        生成批量条形码和二维码
        :param count: 生成的数量
        :param country_code: 国家代码 690到695都是中国大陆的代码
        :param enterprise_code: 企业代码
        """
        list_code = []
        # 循环生成指定数量的条形码或二维码
        for i in range(count):
            # 循环保证生成的条形码或二维码不重复
            while True:
                str_code = self.__create.produce_bar_and_QR_code(country_code, enterprise_code)
                if str_code not in list_code:
                    list_code.append(str_code)
                    break
            bar_or_QR_code = self.__message.get_check_code(str_code)
            # 选择是生成条形码还是二维码
            if select_code == "barcode":
                self.__message.get_bar_code(bar_or_QR_code)
            elif select_code == "qrcode":
                self.__message.get_QR_code(bar_or_QR_code)
        # 打印文件所在地址
        self.__message.print_address("\\" + select_code, "您的条形码已经保存到了")

    def __get_QR_code(self):
        """
        将输入内容转化为二维码
        """
        name = input("请输入内容的名称")
        print("温馨提示：在输入网址时请在复制过来的网址最后加一个\哦")
        content = input("请输入你要转化为二维码的内容")
        # 调用函数将网址生成为二维码并保存
        self.__message.get_QR_code_from_input(name, content)
        # 打印文件所在地址
        self.__message.print_address("\\qrcode", "您的条形码已经保存到了")

    @staticmethod
    def __print_menu(select):
        if select == 1:
            print("""
        **********************************************************
                 进入生成6位数字防伪编码（324654型）界面
        ==========================================================                         
         """)
        elif select == 2:
            print("""
        **********************************************************
             进入生成9位系列产品数字防伪编码（876-456346型） 界面
        ==========================================================                         
        """)
        elif select == 3:
            print("""
        **********************************************************
          进入生成25位混合产品序列号（BAS49-A99AE-ASDA7- IUY7A型）界面
        ==========================================================                         
        """)
        elif select == 4:
            print("""
       **********************************************************
                    进入生成含有数字分析功能的防伪码界面
       ==========================================================                         
        """)
        elif select == 5:
            print("""
       **********************************************************
                进入EAN-13条形码批量输出界面
       ==========================================================                         
       """)
        elif select == 6:
            print("""
       **********************************************************
                进入普通二维码批量输出界面
       ==========================================================                         
       """)
        elif select == 7:
            print("""
       **********************************************************
                进入内容二维码输出（单个）界面
       ==========================================================                         
       """)


if __name__ == "__main__":
    re = EnterpriseCodeView()
    re.main()
