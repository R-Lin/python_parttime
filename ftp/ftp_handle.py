# coding:utf8
import os
import sys
import time
import socket
import linecache
import ConfigParser
from ftplib import FTP

cp = ConfigParser.ConfigParser()
cp.read('ftp.conf')
conf_dict = dict(cp.items('ftp'))
while 1:
    try:
        ftp = FTP(conf_dict['ip'], timeout=10)
    except socket.gaierror:
        print u'FTP连接失败, 10秒后重试'
        time.sleep(10)
    else:
        hostname = socket.gethostname()
        if not os.path.exists(conf_dict['filename']):
            print u'文件名: %s 找不到' % conf_dict['filename'].decode('gbk')
            sys.exit(0)

        if 'logged in' in ftp.login(conf_dict['username'], conf_dict['password']):
            print u'登录成功'
            file_list = ftp.nlst()
            if hostname not in file_list:
                ftp.mkd(socket.gethostname())
            file_list = ftp.nlst()
            print file_list
            ftp.cwd(hostname)
            print ftp.storbinary('STOR 1.txt', open('1.txt', 'rb'))
            ftp.quit()
