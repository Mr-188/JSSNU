#-*-coding:gb2312-*-
import requests
from ping3 import ping
import socket
import sys
import os
import win32api
import win32con

#判断网络状态
def is_connect():
    
    #判断是否使用校园网
    if ping("192.168.67.1",src_addr=None):
        print("已经使用校园网")

        #判断是否认证校园网
        if ping("www.baidu.com",src_addr=None) == None:
            print("正在认证校园网")
            return False
        else:
            print("已经连接上校园网了，请注销后重试。")

            #判断用户是否选择注销
            if input("输入任意键开始注销,注销后重启程序，按0不注销")!='0':
                open_url()
                return True
            else:
                return True
    else:
        print("您使用的不是校园网哦！")
        return True

#打开注销网址
def open_url():
    os.system('"C:/Program Files/Internet Explorer/iexplore.exe" http://192.168.67.1/')

#获取ip地址
def get_host_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
    
#获取文件绝对路径
def path(config_name):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(os.path.abspath(__file__))
    Path = os.path.join(application_path, config_name)
    return Path

#读取用户信息
def message():
    #判断文件是否存在
    user = ""
    password = ""
    set = ""
    #读取文件,没有则创建
    if os.path.exists(path('user.txt')):
        with open(path('user.txt'),'r') as f:
            print('读取用户信息')
            user = f.readline()
            password = f.readline()
            set = f.readline()
            
    if user == '' or password == '' or set == '':
        print('用户信息不存在，请输入用户信息')
        print("请输入信息")
        #输入用户信息
        while user == '':
            user = input("请输入用户名：")
        while password == '':
            password = input("请输入密码：")
        while set == '':
            set = input("移动cmcc，电信njxy,请对应输入：")
        
        #将信息保存到文件
        with open(path('user.txt'),'w') as f:
            f.write(user)
            f.write('\n')
            f.write(password)
            f.write('\n')
            f.write(set)
            f.write('\n')
    ip = get_host_ip()
    #strip()去除字符串首尾的空格
    return user.strip(),password.strip(),set.strip(),ip


#设置开机自启动
def set_start():
    name = 'JSSUN'  # 要添加的项值名称
    # 注册表项名
    KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    # 异常处理
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,  KeyName, 0,  win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path("JSSNU.exe"))
        win32api.RegCloseKey(key)
    except:
        print('添加失败')
    print('添加成功！')

#发送请求
def post(user,password,set,ip):

    url = 'http://192.168.67.1:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account={}@{}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.2&v=3842'.format(user,set,password,ip)
    header = {"Accept": "*/*",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Connection": "keep-alive",
                "Referer": "http://192.168.67.1/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30"
    }
    data = {}
    reponce = requests.post(url,data=data,headers=header).status_code

    #判断是否登录成功
    if reponce == 200:
        print('连接成功')
    else:
        print('连接失败')

#主程序
def main():
    #添加自启动
    set_start()

    #判断网络
    if is_connect():
       return

    #获取信息
    user,password,set,ip= message()

    #发送请求
    post(user, password, set, ip)
   
    
if __name__ == '__main__':
    main()
