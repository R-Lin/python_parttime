# coding:utf8
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
        self.root.title(u'文本处理程序')
        ft = tkFont.Font(family='Fixdsys', size=15, weight=tkFont.BOLD)
        tk.Label(self.root, text=u'准备工作', font=ft).grid(row=0, sticky=tk.W)
        new_frame = tk.Frame(self.root)
        new_frame.grid(row=2, column=0, sticky=tk.W)
        tk.Label(new_frame, text=u'请输入文件:').grid(row=0, column=0)
        tk.Button(new_frame, text=u'浏览', command=self.browser_file).grid(row=0, column=3, columnspan=3)
        self.file_chose = tk.Label(self.root, text=u'已选择文件: 尚未选择文件')
        self.file_chose.grid(row=3, sticky=tk.W)
        tk.Label(self.root, text='-' * 100).grid(row=4)
        tk.Label(self.root, text=u'处理规则', font=ft).grid(column=0, columnspan=3, sticky=tk.W)

        # 分隔符相关
        self.check_exchange = tk.IntVar()
        self.before_delimiter = tk.StringVar()
        self.after_delimiter = tk.StringVar()
        self.delimiter_dic = {}

        self.email_suffix_check = tk.IntVar()
        self.email_suffix = tk.StringVar()
        new_frame2 = tk.Frame(self.root)
        new_frame2.grid(row=6, sticky=tk.W)

        tk.Checkbutton(new_frame2, text=u'替换分隔符', variable=self.check_exchange).grid(row=0, column=0, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.before_delimiter).grid(row=0, column=1, sticky=tk.W)
        tk.Label(new_frame2, text=u'替换成').grid(row=0, column=2, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.after_delimiter).grid(row=0, column=3, sticky=tk.W)
        tk.Checkbutton(new_frame2, text=u'增加邮箱后缀', variable=self.email_suffix_check).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.email_suffix).grid(row=1, column=1, sticky=tk.W)
        self.delimiter = tk.StringVar()
        tk.Label(new_frame2, text=u'请输入文件分隔符:').grid(row=2, column=0, sticky=tk.W)
        tk.Entry(
            new_frame2, textvariable=self.delimiter,
        ).grid(row=2, column=1, sticky=tk.W)

        # 检查功能相关
        self.check_emil = tk.IntVar()
        self.check_pass_len = tk.IntVar()
        self.pass_len = tk.StringVar()

        new_frame3 = tk.Frame(self.root)
        new_frame3.grid(row=7, sticky=tk.W)

        tk.Checkbutton(
            new_frame3, text=u'检查账号是否邮箱', variable=self.check_emil,
        ).grid(row=2, column=0, sticky=tk.W)
        tk.Checkbutton(
            new_frame3, text=u'排除密码长度(小于不等于):', variable=self.check_pass_len,
        ).grid(row=2, column=1, sticky=tk.W)
        tk.Entry(
            new_frame3, width=10, textvariable=self.pass_len
        ).grid(row=2, column=2, sticky=tk.W)

        new_frame4 = tk.Frame(self.root)
        new_frame4.grid(row=8, sticky=tk.W)
        self.rad_var = tk.IntVar()
        tk.Radiobutton(
            new_frame4, variable=self.rad_var, value=0, text=u'字符不处理',
            command=self.root_refactor
        ).grid(row=3, column=0, sticky=tk.W)
        tk.Radiobutton(
            new_frame4, variable=self.rad_var, value=1, text=u'首位字母大写',
            command=self.root_refactor
        ).grid(row=3, column=1, sticky=tk.W)
        tk.Radiobutton(
            new_frame4, variable=self.rad_var, value=-1, text=u'最后字母大写',
            command=self.root_refactor
        ).grid(row=3, column=2, sticky=tk.W)

        self.other_letter = tk.StringVar()
        tk.Entry(new_frame4, textvariable=self.other_letter, width=2).grid(row=3, column=4, sticky=tk.W)
        tk.Radiobutton(
            new_frame4, variable=self.rad_var, value=2, text=u'其他顺序位:', command=self.root_refactor
        ).grid(row=3, column=3, sticky=tk.W)
        tk.Label(new_frame4, text='-' * 100).grid(columnspan=6)

        # 执行
        tk.Button(new_frame4, text=u'执行', font=ft, command=self.run).grid(sticky=tk.W)
        self.proses = tk.Label(new_frame4, text=u'')
        self.proses.grid(row=5, column=1, sticky=tk.W)
        self.proses['text'] = '123'

    def root_refactor(self):
        if self.rad_var.get() == 1:
            self.letter_pos = 0
        else:
            self.letter_pos = self.rad_var.get()
        print self.letter_pos

    def form_check(self):
        rtc = 0
        if not self.read_file:
            tkMessageBox.showerror(message='请选择文件')
            return 0

        elif not self.delimiter.get():
            tkMessageBox.showerror(message='分割符为空')
            return 0

        elif self.check_pass_len.get():
            if not (self.pass_len and self.pass_len.get().isdigit()):
                tkMessageBox.showerror(message='密码长度为无效值')
                return 0
            else:
                rtc = 1
        else:
            rtc = 1
        if self.rad_var.get() == 2:
            if not (self.other_letter.get() and self.other_letter.get().isdigit()):
                tkMessageBox.showerror(message='替换顺序位为无效值')
                return 0
            else:
                self.letter_pos = self.other_letter.get()
                rtc = 1

        if self.check_exchange.get() == 1:
            if not (self.before_delimiter.get() and self.after_delimiter.get()):
                tkMessageBox.showerror(message='请指定需要替换或者被替换的分隔符')
                return 0
            else:
                self.delimiter_dic['b_delimiter'] = self.before_delimiter.get()
                self.delimiter_dic['a_delimiter'] = self.after_delimiter.get()
                rtc = 1

        if self.email_suffix_check.get():
            if not self.email_suffix.get():
                tkMessageBox.showerror(message='邮箱后缀不能为空')
                return 0
            else:
                rtc = 1
        self.delimiter_dic['delimiter'] = self.delimiter.get()
        return rtc

    def browser_file(self):
        self.read_file = askopenfile()
        if self.read_file:
            self.file_chose['text'] = u'已选择文件: %s' % self.read_file.name
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
            self.proses['text'] = u'共处理%s 条数据, %s 条数据有效' % (num, real_deal_num)
            tkMessageBox.showinfo(message='处理完成, 耗时: %s' % (time.clock() - runtime) )
        else:
            print 'cuo'

    def main(self):
        self.root.mainloop()

if __name__ == '__main__':
    windows = FileHandle()
    windows.main()
