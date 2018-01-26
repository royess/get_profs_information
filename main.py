# -*- coding: UTF-8 -*-
# author=royellow
# date=2017-11-03

import requests
import re


class Prof:

    '''
    还可能支持的成员函数： 发送邮件 访问网址
    '''

    def __init__(self, name_en, name, field,
                 phone, email, homepage, office):
        self.name_en = name_en
        self.name = name
        self.field = field
        self.phone = phone
        self.email = email
        self.homepage = homepage
        self.office = office


    def displayInfo(self):
        for i in [self.name_en, self.name, self.field,
                 self.phone, self.email, self.homepage, self.office]:
            print(i)


def get_all_profs():
    url_0 = 'http://www.phy.pku.edu.cn/personnel/faculty.xml'
    html_0 = requests.get(url_0)
    html_0.encoding = 'gbk'
    text_0 = html_0.text
    prof_urls =
    prof_filenames = [prof_url[16:-6] for prof_url in prof_urls ]

    all_profs = []

    for prof_filename in prof_filenames:
        url_1 = 'http://www.phy.pku.edu.cn/personnel/member/'\
                + prof_filename +'.xml'

        html_1 = requests.get(url_1)
        html_1.encoding = 'gbk'
        text_1 = html_1.text

        prof_name = re.findall(r'<Name>.+</Name>', text_1)
        if prof_name:
            prof_name = prof_name[0][6:-7]
        else:
            prof_name = None

        prof_field = re.findall('<Field>.+</Field>', text_1)
        if prof_field:
            prof_field = prof_field[0][7:-8]
        else:
            prof_field = None

        prof_phone = None
        # hard to accomplish

        prof_email = re.findall('[ >:]\w+@pku.edu.cn',text_1)

        if not prof_email:
            prof_email = re.findall('"\w+_at_pku.edu.cn', text_1)

        if prof_email:
            prof_email = prof_email[0][1:]
        else:
            prof_email = None
            # error

        prof_homepage = re.findall('<Homepage>.+</Homepage>', text_1)
        if prof_homepage:
            prof_homepage = prof_homepage[0][10:-11]
        else:
            prof_homepage = None

        prof_office = re.findall('<Office>.+</Office>', text_1)
        if prof_office:
            prof_office = prof_office[0][8:-9]
        else:
            prof_office = None


        prof = Prof(prof_filename, prof_name, prof_field,prof_phone,
                             prof_email, prof_homepage, prof_office)

        all_profs.append(prof)

    return all_profs


for prof in get_all_profs():
    prof.displayInfo()
    print('\n')







