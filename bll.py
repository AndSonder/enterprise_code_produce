from model import *
from pystrich.ean13 import EAN13Encoder
import qrcode
import random
import os



class EnterpriseCodeProduce:
    """
    企业编码产生器
    """
    @staticmethod
    def produce_random_code(times=6):
        """
        生成指定位数的随机数
        :return 生成的随机数，str类型
        """
        # 调用生成器生成指定数目的随机数
        return "".join((str(random.randint(1, 9)) for i in range(times)))

    def produce_nine_code(self, beginning_number):
        """
        产生9位系列产品的数字防伪码
        :param beginning_number: 系列产品编号
        :return: 生成的防伪码  str类型
        """
        # 调用生成器
        return str(beginning_number) + self.produce_random_code()

    @staticmethod
    def produce_twenty_five_code():
        """
        产生一个25位混合产品系列号
        :return: 产生的25位混合产品系列号  str类型
        """
        # 创建一个空字符串
        str_code = ""
        # 循环5次
        for i in range(5):
            # 得到5位数字字母混合码
            str_code += "".join((CodeModel.SRE_CODE[random.randint(0, 34)] for item in range(5))) + "-"
        return str_code
    
    def produce_data_analysis_code(self, data_analysis):
        """
        生成含有数据分析功能的防伪代码
        :param data_analysis: 数据分析编号
        :return: 生成的防伪码 str类型
        """
        # 调用函数生成一个6位随机编码
        self.__str_code = self.produce_random_code()

        list_index = self.__get_random_index()
        for item in range(len(data_analysis)):
            # 外调函数得到升序排列的索引;
            i = list_index[item]
            # 将数据分析编码随机的插入到生成的随机编码中
            self.__str_code = self.__str_code[0:i] + str(data_analysis)[item] + self.__str_code[i:]
        return str(self.__str_code)


    def __get_random_index(self):
        """
        得到升序排列的索引
        :return: 升序排列的列表
        """
        list_index = []
        for i in range(3):
            if i == 0:
                list_index.append(random.randint(0, 5))
            elif i == 1:
                list_index.append(random.randrange(list_index[i - 1] + 1, 7))
            else:
                list_index.append(random.randint(list_index[i - 1] + 1, 9))
        return list_index

    def produce_bar_and_QR_code(self, country_code, enterprise_code):
        """
        生成除校验码外的二维码/条形码
        :param country_code: 国家编号
        :param enterprise_code: 企业编号
        :return:生成的二维码/条形码 str类型
        """
        # 调用函数生成5位随机数,作为产品编码
        commodity_code = int(self.produce_random_code(5))
        self.__str_code = str(country_code) + str(enterprise_code) + str(commodity_code)
        return str(self.__str_code)


class EnterpriseCodeControl:
    """
    企业编码控制器
    """

    @staticmethod
    def get_bar_code(str_code):
        """
        生成防伪码的条形码
        :param str_code: 防伪码
        """
        encoder = EAN13Encoder(str_code)
        encoder.save("barcode\\" + str_code + ".png")

    @staticmethod
    def save_code(str_code, path):
        """
        将生成的防伪码保存到指定路径
        :param str_code:生成的防伪码
        :param path: 路径
        """
        str_code = str_code + "\n"
        with open(path, "a") as f:
            f.write(str_code)

    @staticmethod
    def get_QR_code(str_code):
        """
        生成二维码并保存到指定位置
        :param str_code: 防伪码
        """
        encoder = qrcode.make(str_code)
        encoder.save("qrcode\\" + str_code + ".png")

    @staticmethod
    def get_QR_code_from_input(name, content):
        """
        根据输入的内容生成二维码  可以生产代表网址的二维码
        :param content: 生成二维码代表的内容  str类型
        """
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1
        )  # 设置二维码的大小
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image()
        img.save("qrcode\\" + name + ".png")

    def batch_generator(self, count, method, path):
        """
        批量生成器，批量生成某种防伪码
        :param count: 需要打印的次数
        :param produce_something:打印调用的方法
        :param path: 保存路径
        """
        # 循环指定的数目
        for item in range(count):
            produce_code = method()
            self.save_code(produce_code, path)

    @staticmethod
    def get_check_code(str_code):
        """
        计算条形码/二维码的最后一位校验码,并将其合并为二维码/条形码
        :param str_code:出了最后一位的条形码/二维码
        :return:最后一位的校验码
        """
        even_sum = int(str_code[3] + str_code[5] + str_code[7] + str_code[9] + str_code[11])
        odd_sum = int(str_code[0] + str_code[2] + str_code[4] + str_code[6] + str_code[8])
        check_bit = (even_sum * 3 + odd_sum) % 10
        check_bit = int((10 - check_bit) % 10)
        str_code = str_code + str(check_bit)
        return str_code

    @staticmethod
    def print_address(folder, print_content):
        # 得到当前路径
        path = os.getcwd() + folder
        print(print_content, path)

    @staticmethod
    def check(file, method,message = None):
        """
        检查文件中是否有重复的防伪码
        :param file: 要检查的文件
        :param method: 写文件所用的方法
        """
        # 打开需要检查的文件
        with open(file, "r") as f:
            list_file = []
            # 循环检查生成的文件中有没有重复的
            for item in f:
                EnterpriseCodeControl.__check_is_exist(item, list_file, method,message)
        # 覆盖原文件
        f = open(file, "w+")
        for item in list_file:
            f.write(item + "\r\n")

    @staticmethod
    def __check_is_exist(item, list_file, method,message):
        """
        运用递归检查是否有重复防伪码，并将其替换为新的防伪码
        """
        # 如果防伪码不在list_file中则添加
        if item not in list_file:
            list_file.insert(-1, item)
        # 如果不在，运用递归添加一个新的不重复的防伪码
        else:
            if message == None:
                new_code = method()
                EnterpriseCodeControl.__check_is_exist(new_code, list_file, method,message)
            else:
                new_code = method(message)
                EnterpriseCodeControl.__check_is_exist(new_code, list_file, method, message)

