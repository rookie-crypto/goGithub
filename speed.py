import os
import re
import sys
import threading

def update_url(file):
    """
    匹配临时文件中的URL，更新该临时文件以每行显示一条IP的方式
    :param file: 临时文件路径
    """
    with open(file,'r',encoding='utf-8') as f:
        ipList = set(re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",f.read()))

    with open(file,'w',encoding='utf-8') as f:
        for ip in ipList:
            f.write(ip+'\n')

    print("URL FILE UPDATE SUCCESS.")


def ping_check(ips,platform):
    """

    多线程支持
        根据传入的IP地址调用系统ping命令，判断延迟后返回最优IP
    :param ips: IP列表
    :param platform: linux or win32
    :return: 排序结果
    """
    resTime = {}
    threads = []

    def ping_handle(ip, resTime):
        """
        子线程：获取单个IP的响应时间
        :param ip:
        :param resTime:
        """
        tempTime = 0
        count = 0  # 实际ping次数

        # 不同平台的ping命令及正则匹配略有不同
        if platform == 'linux':
            result = os.popen('ping -c 3 -W 0.2 ' + ip)
            for item in result.read().splitlines()[1:3]:
                try:
                    tempTime += float(re.findall('.*time=(.*) ms', item)[0])
                    count += 1
                except Exception as err:
                    pass
        elif platform == 'win32':
            result = os.popen('ping -n 3 -w 20 ' + ip)
            for item in result.read().splitlines()[2:4]:
                try:
                    tempTime += float(re.findall('.*时间=(.*)ms', item)[0])
                    count += 1
                except Exception as err:
                    pass
        if count != 0:
            tempTime /= count
        resTime[ip] = tempTime

    # 多线程操作
    for ip in ips:
        ping_handler = threading.Thread(target=ping_handle,args=(ip,resTime))
        ping_handler.start()
        threads.append(ping_handler)
    for t in threads:
        t.join()

    resTime = sorted(resTime.items(),key=lambda x:x[1])
    # print(resTime)
    for i in range(len(resTime)-1,-1,-1):
        if resTime[i][1] == 0:
            resTime.remove(resTime[i])
    # 数据展示
    count = 1
    for item in resTime:
        print("{0:>3}: {1:<20}{2:.2f}ms".format(count,item[0],item[1]))
        count += 1
    # 排序返回
    return resTime

def update_linux_host(ip,domain):
    """
    LINUX更新本地HOST文件 [必须是管理员权限]
    :param ip:
    :param domain:
    """
    # 清除原始数据
    cmd = os.popen("sed -i '/%s/d' /etc/hosts" %(domain))
    cmd.close()
    # 写入新数据
    cmd = os.popen("echo %s %s >> /etc/hosts" %(ip,domain))
    cmd.close()
    # 核查是否写入成功
    with open('/etc/hosts','r',encoding='utf-8') as f:
        if f.readlines()[-1].strip() == ip + ' ' + domain:
            print("HOST UPDATE SUCCESS\n")
        else:
            print("HOST UPDATE FAILED\n")

def update_win_host(ip,domain):
    """
    Win更新本地HOST文件 [必须是管理员权限]
    :param ip:
    :param domain:
    """
    fr = open('C:\\Windows\\System32\\drivers\\etc\\hosts','r',encoding='utf-8')
    data = fr.read()
    fr.close()
    # 若内容存在则替换
    if domain in data:
        fw = open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w',encoding='utf-8')
        for line in data.splitlines():
            if domain in line:
                line = ip + '\t' + domain
            fw.write(line+'\n')
        fw.close()
    # 若不存在则添加
    else:
        fa = open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'a',encoding='utf-8')
        fa.write('\n'+ ip + '\t' + domain)
        fa.close()
    # 判断是否添加成功
    fr = open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'r',encoding='utf-8')
    data = fr.read()
    fr.close()
    if ip + '\t' + domain in data:
        print("HOST UPDATE SUCCESS\n")
    else:
        print("HOST UPDATE FAILED\n")

if __name__ == '__main__':
    # 设置域名与域名对应IP文件
    PATH = 'github.txt'
    DOMAIN = 'github.com'
    ipList = []

    update_url(PATH)

    with open(PATH, 'r',encoding='utf-8') as f:
        for line in f:
            ipList.append(line.strip())

    result = ping_check(ipList,platform=sys.platform)
    print("\nRECOMMEND: ")
    # 展示最优三条
    for i in range(3):
        print("%s\t%.2fms" %(result[i]  [0],result[i][1]))
    # 默认将第一条建议设置为DNS解析
    if sys.platform == 'linux':
        update_linux_host(result[0][0],DOMAIN)
    elif sys.platform == 'win32':
        update_win_host(result[0][0],DOMAIN)
