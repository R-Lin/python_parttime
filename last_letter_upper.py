# coding: gbk
import os
import re
import sys

if __name__ == '__main__':
    file_name = raw_input(r'请输入文件名: ')
    resul_file = os.path.join(os.path.dirname(file_name), 'result.txt')
    if not os.path.exists(file_name):
        print 'File not found'
        sys.exit()

    w_num = 0
    match_pattern = re.compile(r'.*([a-z])')
    replace_pattern = re.compile(r'(.*)[a-z](.*)')
    with open(file_name) as f1, open(resul_file, 'w') as f2:
        for line in f1:
            char = re.findall(match_pattern, line)
            if char:
                line = replace_pattern.sub('\\1' + char[0].upper() + '\\2', line)
                f2.write(line)
                w_num += 1
                if w_num % 500 == 0:
                    print '已改: %s' % w_num
    print '总共: %s' % w_num
    print '结果文件: %s' % resul_file
    a = raw_input('The End!')
