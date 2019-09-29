#!/usr/bin/env python3
#-*-coding:utf-8-*-

import time, sys
import redis
import socket
import queue
import pymongo
import threading
import argparse
from IPy import IP

class X_Scan(object):

    class Scan(threading.Thread):

        # 返回结果列表
        result = []

        def __init__(self, ip_queue=[], port=6379, timeout=3):

            threading.Thread.__init__(self)

            self.__ip_queue = ip_queue
            self.__port = port
            self.__timeout = timeout

        # 测试是否存在mongodb未授权访问漏洞
        # 2019.9.12 更新
        # 采用socket连接，新的连接字符待定（连不上），目前暂时采用网上的
        # 采用新函数 list_dbnames(失败)
        # 采用原函数 采用新的包 准确度待测试
        def mongodb_check(self, ip, port=27017, timeout=3):

            #global dbname
            
            # 问题：有的数据库有mongodb漏洞，但是m.database_names()返回不了dbname
            # 解决：暂时采用能连接上就判定为存在漏洞，需要手工稽查

            #try:
            #    m = pymongo.MongoClient(ip, port, socketTimeoutMS=3000)
            #    dbname = m.database_names()
            #    if dbname: return True
            # return True

            #except Exception as e:
            #    return False
            try:
                socket.setdefaulttimeout(timeout)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))

                 # 网页版        
                #s.send(b'\x3F\x00\x00\x00\x7E\x00\x00\x00\x00\x00\x00\x00\xD4\x07\x00\x00\x04\x00\x00\x00\x61\x64\x6D\x69\x6E\x2E\x24\x63\x6D\x64\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x18\x00\x00\x00\x10\x6C\x69\x73\x74\x44\x61\x74\x61\x62\x61\x73\x65\x73\x00\x01\x00\x00\x00\x00')
        
                # msf
                s.send(b'\x3f\x00\x00\x00\x14\x56\x8f\x9a\xff\xff\xff\xff\xd4\x07\x00\x00\x00\x00\x00\x00\x61\x64\x6d\x69\x6e\x2e\x24\x63\x6d\x64\x00\x00\x00\x00\x00\x01\x00\x00\x00\x18\x00\x00\x00\x10\x6c\x69\x73\x74\x44\x61\x74\x61\x62\x61\x73\x65\x73\x00\x01\x00\x00\x00\x00')

                # 自己版
                #s.send(b'\x3f\x00\x00\x00\x23\x48\x00\x00\x00\x00\x00\x00\xd4\x07\x00\x00\x04\x00\x00\x00\x61\x64\x6d\x69\x6e\x2e\x24\x63\x6d\x64\x00\x00\x00\x00\x00\xff\xff\xff\xff\x18\x00\x00\x00\x10\x6c\x69\x73\x74\x44\x61\x74\x61\x62\x61\x73\x65\x73\x00\x01\x00\x00\x00\x00')
                result = s.recv(1024)
                print(result)
                if 'not authorized' in str(result):
                    return False
                elif 'local' in str(result) and 'errmsg' not in str(result):  #增加一个“errmsg”字符串判断，避免1.9版本中的误报。
                    return True
                else:
                    return False

            except Exception as e:
                return False
        
        # 测试是否存在redis未授权访问漏洞
        def redis_check(self, ip, port=6379):

            try:
                r = redis.Redis(ip, port)
                r.config_get('dir')
                return True

            except Exception as e:
                return False

# 2019.9.11，run函数未更新,更新mencached_check
# 2019.9.23，run函数更新
#-----------------------------------------------------------------------------------------
        def Memcached_check(self, ip, port=11211, timeout=3):

            try:

                socket.setdefaulttimeout(timeout)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, int(port)))
                s.send(b"stats\r\n")
                result = s.recv(1024)

                if "STAT version" in str(result):
                    return True

            except Exception as e:
                return False
        
#-----------------------------------------------------------------------------------------

        # 执行
        def run(self):

            while True:

                if self.__ip_queue.empty():
                    break

                ip = self.__ip_queue.get(timeout = 0.5)
                port  = self.__port
                timeout = self.__timeout

                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(timeout)
                    print('[CONNECT] %3s' % ip)
                    result_code = s.connect_ex((ip, port)) #开放返回0

                    if result_code == 0:

                        if port == 6379:
                            if self.redis_check(ip):
                                # print('6379')
                                self.result.append(ip)
                        
                        elif port == 27017:
                            if self.mongodb_check(ip):
                                # print('27017')
                                self.result.append(ip)
                        
                        elif port == 11211:
                            if self.Memcached_check(ip):
                                # print('11211')
                                self.result.append(ip)
                
                except Exception as e:
                    print(e)

                finally:
                    s.close()
                    print('[FINISH] %3s' % ip)

# 将网段以ip地址的形式返回一个列表
def iplst(ip):
    result = []
    ipx = IP(ip)
    for x in ipx:
        result.append(str(x))
    return result

# 主函数，包括命令行的调用
def main():

    # 命令行
    parser = argparse.ArgumentParser(description="-Demo-")
    parser.add_argument('-i', '--ip', type=str)
    parser.add_argument('-p', '--port', type=str)
    args = parser.parse_args()

    ip = args.ip
    ip_queue = queue.Queue()
    ip_list = iplst(ip)

    port = int(args.port)

    start_time = time.time()
    x_scan = X_Scan()

    # 线程数量
    thread_num = 100

    threads = [] 

    for ip in ip_list:
        ip_queue.put(ip)

    for t in range(thread_num):
        threads.append(x_scan.Scan(ip_queue, port, timeout = 3))

    # 启动线程
    for thread in threads:
        thread.start()

    # 阻塞线程
    for thread in threads:
        thread.join()

    end_time = time.time()
    
    print('##########')
    print('[END TIME] %3ss' % (end_time - start_time,))
    print('##########')

    if x_scan.Scan.result:
        for x in x_scan.Scan.result:
            print('[EXIST] %3s' % x)
    else:
        print('[NOT EXIST]') 

# 使用 python Scanner.py -i 网段 -p 端口(端口为6379为redis稽查，27017为mongodb稽查，11211为memcached稽查)
# 使用方法，如 python Scanner.py -i 网段 -p 端口
if __name__ == '__main__':
    main()