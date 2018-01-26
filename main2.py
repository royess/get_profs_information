# -*- coding: UTF-8 -*-
# author=royellow
# date=2017-11-03

import requests
import re
import xlrd
import xlwt


class Prof:
    '''
    还可能支持的成员函数： 发送邮件 访问网址
    '''

    def __init__(self, filesname):
        self.name_en = filesname
        self.url = self.name = self.field = self.phone\
            = self.email = self.homepage = self.office = None

    def fillInfo(self):
        self.url = 'http://www.phy.pku.edu.cn/personnel/member/' \
                + prof_filename + '.xml'

        html = requests.get(self.url)
        html.encoding = 'gbk'
        text = html.text
        temp = []

        temp = re.findall(r'<Name>.+</Name>', text)
        if temp:
            self.name = temp[0][6:-7]
        else:
            self.name = None

        temp = re.findall('<Field>.+</Field>', text)
        if temp:
            self.field = temp[0][7:-8]
        else:
            self.field = None

        self.phone = None
        # hard to accomplish

        temp = re.findall('[ >:]\w+@pku.edu.cn', text)
        if not temp:
            self.email = re.findall('"\w+_at_pku.edu.cn', text)

        if temp:
            self.email = temp[0][1:]
        else:
            self.email = None
            # error

        temp = re.findall('<Homepage>.+</Homepage>', text)
        if temp:
            self.homepage = temp[0][10:-11]
        else:
            self.homepage = None

        temp = re.findall('<Office>.+</Office>', text)
        if temp:
            self.office = temp[0][8:-9]
        else:
            self.office = None

    def displayInfo(self):
        for i in [self.name_en, self.name, self.field,
                  self.phone, self.email, self.homepage, self.office]:
            print(i)

    def into_table(self, sheet, row_num, style):
        props = [self.name_en, self.name, self.field,
                  self.phone, self.email, self.homepage, self.office]
        for i in range(7):
            sheet.write(row_num, i, props[i], style)

def get_name_en():
    url_0 = 'http://www.phy.pku.edu.cn/personnel/faculty.xml'
    html_0 = requests.get(url_0)
    html_0.encoding = 'gbk'
    text_0 = html_0.text
    prof_urls = re.findall('<a href="member/.+.xml">', text_0)
    prof_filenames = [prof_url[16:-6] for prof_url in prof_urls]
    return prof_filenames


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    return style
# 别人写的函数

all_profs = []

for prof_filename in get_name_en():
    prof = Prof(prof_filename)
    prof.fillInfo()
    #prof.displayInfo(); print('\n')
    all_profs.append(prof)

book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('sheet 1')


row_0 = ['name_en', 'name', 'field', 'phone',
         'email', 'homepage', 'office']

for i in range(len(row_0)):
    sheet.write(0, i, row_0[i], set_style('Times New Roman', 220, True))

row_num = 1
for prof in all_profs:
    prof.into_table(sheet, row_num, style=set_style('Times New Roman', 220, True))
    row_num += 1

book.save('res.xls')






