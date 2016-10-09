# coding: gbk
import Tkinter as tk
import tkMessageBox
import tkFont
import re
import time
from tkFileDialog import askopenfile


class FileHandle:
    def __init__(self):
        self.root = tk.Tk()
        self.read_file = ''
        self.letter_pos = ''
        self.root.title(u'����-���Ե�½AppleID')
        ft = tkFont.Font(family='Fixdsys', size=15, weight=tkFont.BOLD)
        tk.Label(self.root, text=u'׼������', font=ft).grid(row=0, sticky=tk.W)
        new_frame = tk.Frame(self.root)
        new_frame.grid(row=2, column=0, sticky=tk.W)
        tk.Label(new_frame, text=u'��ѡ�� AppleID�ļ� :').grid(row=0, column=0)
        tk.Button(new_frame, text=u'���', command=self.browser_file).grid(row=0, column=3, columnspan=3)
        self.file_chose = tk.Label(self.root, text=u'��ѡ���ļ�: ��δѡ���ļ�')
        self.file_chose.grid(row=3, sticky=tk.W)
        tk.Label(self.root, text='-' * 100).grid(row=4, column=0, sticky=tk.W)

        # ����
        new_frame2 = tk.Frame(self.root)
        new_frame2.grid(row=5, column=0, sticky=tk.W)
        self.ip_set = tk.Label(new_frame2, text=u'��������:��IP', font=ft)
        self.ip_set.grid(row=0, column=0, columnspan=8, sticky=tk.W)
        self.username = tk.StringVar()
        self.passwd = tk.StringVar()
        self.num1 = tk.StringVar()
        self.passue = tk.StringVar()
        self.num2 = tk.StringVar()
        self.dial = tk.StringVar()

        tk.Label(new_frame2, text=u'�˺�: ').grid(row=1, column=0, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.username).grid(row=1, column=1, sticky=tk.W)
        tk.Label(new_frame2, text=u'  ÿ����(��): ').grid(row=1, column=3, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.num1, width=3).grid(row=1, column=4, sticky=tk.W)
        tk.Label(new_frame2, text=u'  ��ͣ(��): ').grid(row=1, column=5, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.passue, width=4).grid(row=1, column=6, sticky=tk.W)

        tk.Label(new_frame2, text=u'����: ').grid(row=2, column=0, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.passwd).grid(row=2, column=1, sticky=tk.W)
        tk.Label(new_frame2, text=u'  ÿ����(��): ').grid(row=2, column=3, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.num2, width=3).grid(row=2, column=4, sticky=tk.W)
        tk.Label(new_frame2, text=u'  ����(��): ').grid(row=2, column=5, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.dial, width=4).grid(row=2, column=6, sticky=tk.W)
        tk.Button(new_frame2, text=u'����', font=ft, command=self.dial_call).grid(row=1, column=7, rowspan=2, columnspan=2, sticky=tk.W)

        # # �ָ������
        self.thrading_num = tk.StringVar()
        self.delimiter = tk.StringVar()

        tk.Label(self.root, text='-' * 100).grid(row=7, sticky=tk.W)
        tk.Label(self.root, text=u'�������', font=ft).grid(column=0, columnspan=3, sticky=tk.W)

        new_frame3 = tk.Frame(self.root)
        new_frame3.grid(row=9, sticky=tk.W)

        tk.Label(new_frame3, text=u'�ļ��ָ���:').grid(row=2, column=0, sticky=tk.W)
        tk.Entry(
            new_frame3, textvariable=self.delimiter,
            width=10
        ).grid(row=2, column=1, sticky=tk.W)
        tk.Label(new_frame3, text=u'   �����߳���:  ').grid(row=2, column=2, sticky=tk.W)
        tk.Entry(new_frame3,  textvariable=self.thrading_num, width=3).grid(row=2, column=4, sticky=tk.W)
        tk.Button(new_frame3, text=u'ִ��', font=ft).grid(row=2, column=6, sticky=tk.E)

        # tk.Label(new_frame2, text=u'�滻��').grid(row=0, column=2, sticky=tk.W)
        # # tk.Entry(new_frame2, textvariable=self.after_delimiter).grid(row=0, column=3, sticky=tk.W)
        # # tk.Checkbutton(new_frame2, text=u'���������׺', variable=self.email_suffix_check).grid(row=1, column=0, sticky=tk.W)
        # # tk.Entry(new_frame2, textvariable=self.email_suffix).grid(row=1, column=1, sticky=tk.W)
        # self.delimiter = tk.StringVar()
        #
        # # ��鹦�����
        # self.check_emil = tk.IntVar()
        # self.check_pass_len = tk.IntVar()
        # self.pass_len = tk.StringVar()
        #
        # new_frame3 = tk.Frame(self.root)
        # new_frame3.grid(row=7, sticky=tk.W)
        #
        # new_frame4 = tk.Frame(self.root)
        # new_frame4.grid(row=8, sticky=tk.W)
        #
        # # ִ��
        # tk.Button(new_frame4, text=u'ִ��', font=ft, command=self.run).grid(sticky=tk.W)
        # self.proses = tk.Label(new_frame4, text=u'')
        # self.proses.grid(row=5, column=1, sticky=tk.W)
        # self.proses['text'] = '123'

    def dial_call(self):
        self.ip_set['text'] = u'��������:����, ����ɵ��'

    def browser_file(self):
        self.read_file = askopenfile()
        if self.read_file:
            self.file_chose['text'] = u'��ѡ���ļ�: %s' % self.read_file.name
            return self.read_file.name

    def run(self):
        rtc = self.form_check()
        if rtc:
            runtime = time.clock()
            write_file_name = self.read_file.name + '_py_ok_.txt'
            with open(write_file_name, 'w+') as f:
                letter_list = re.compile(r'[^a-z]*?([a-z]).*')
                first_letter = re.compile(r'[^a-z]*?([a-z]).*')
                first_letter_replace = re.compile(r'([^a-z]*?)[a-z](.*)')
                last_letter = re.compile(r'.*([a-z])')
                last_letter_replace = re.compile(r'(.*)[a-z](.*)')
                delimiter = re.compile(
                    re.sub(r'\s', r'\\s', self.delimiter_dic.get('b_delimiter', ''))
                   )
                real_deal_num = 0
                for num, line in enumerate(self.read_file, 1):
                    line = line.strip()
                    try:
                        if self.check_exchange.get():
                            line = re.sub(
                                delimiter,
                                self.delimiter_dic['a_delimiter'],
                                line
                            )
                        result = line.split(
                            self.delimiter_dic['delimiter']
                            )
                        if len(result) != 2 or not result[1]:
                            continue
                        else:
                            username, passwd = result
                            if self.email_suffix_check.get():
                                username += self.email_suffix.get()

                            if self.check_emil.get():
                                if '@' not in username:
                                    continue
                            if self.check_pass_len.get():
                                if len(passwd) < int(self.pass_len.get()):
                                    continue

                            if self.rad_var.get():
                                # print self.rad_var.get()
                                try:
                                    if self.letter_pos == 0:
                                        letter = re.findall(first_letter, passwd)[0]
                                        passwd = first_letter_replace.sub('\\1' + letter.upper() + '\\2', passwd)
                                    elif self.letter_pos == -1:
                                        letter = re.findall(last_letter, passwd)[0]
                                        passwd = last_letter_replace.sub('\\1' + letter.upper() + '\\2', passwd)
                                    elif self.letter_pos == 2:
                                        letter_list = re.findall(letter_list, passwd)
                                except IndexError:
                                    pass
                            line = self.delimiter_dic['delimiter'].join((username, passwd))
                            if line:
                                real_deal_num += 1
                            # print line
                            f.write(line + '\n')
                    except IndexError:
                        pass

            self.read_file.seek(0)
            self.proses['text'] = u'������%s ������, %s ��������Ч' % (num, real_deal_num)
            tkMessageBox.showinfo(message='�������, ��ʱ: %s' % (time.clock() - runtime) )
        else:
            print 'cuo'
    def main(self):
        self.root.mainloop()
if __name__ == '__main__':
    f = FileHandle()
    f.main()