# JSSNU

[TOC]

## 软件作用

每次开机都会帮你自动认证校园网。

## 文件结构

![文件结构](C:\Users\16844\AppData\Roaming\Typora\typora-user-images\image-20220407112804290.png)

**user.txt 为自动生成的用户信息，删掉可重新初始化。JSSNU.exe 为主程序。JSSNU.md 为使用文档，使用 Typora 编写，建议用 Markdown 语法编辑器打开。JSSNU.md 为使用文档的PDF版。JSSNU.py 为源码。**

## 使用教程

### 初次使用

#### 已经认证校园网

![已经连通校园网](C:\Users\16844\AppData\Roaming\Typora\typora-user-images\image-20220407101939661.png)

需要先注销后再重新打开此程序，按任意键后回车即可跳转到注销网站。点击注销后重启程序跳转到[【未认证校园网】](#未认证校园网)

如果不方便断网则输入0按回车或者直接关闭程序。

#### 未认证校园网

根据提示输入正确的信息即可，依次为学号，身份证后六位，服务商信息。

![输入信息](D:\Desktop\image-20220407110426252.png)

### 非初次使用

#### 已认证校园网

什么都不用做，开机会自动帮你联网。

#### 未认证校园网

手动连接校园网后跳转到[已认证校园网](#已认证校园网)。

## 源码解释

### is_connect

> 类型：bool
>
> 输入：无
>
> 返回：True 不满足网络条件 False 满足网络条件
>
> 作用：判断网络状态
>
> 调用：[open_url](#open_url)

```python
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
```

### open_url

> 类型：Void
>
> 输入：无
>
> 返回：无
>
> 作用：打开注销网站
>
> 调用：无

```python
#打开注销网址
def open_url():
    os.system('"C:/Program Files/Internet Explorer/iexplore.exe" http://192.168.67.1/')

```

### get_host_ip

> 类型 String
>
> 输入：无
>
> 返回：ip地址
>
> 作用：获取ip地址
>
> 调用：无

```python
#获取ip地址
def get_host_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
```

### path

> 类型：String
>
> 输入：config_name 文件名
>
> 输出：Path 该文件的绝对路径
>
> 作用：获取程序的绝对路径，方便添加自启动和读写文件。
>
> 调用：无

```python
#获取文件绝对路径
def path(config_name):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(os.path.abspath(__file__))
    Path = os.path.join(application_path, config_name)
    return Path
```

### message

> 类型：String
>
> 输入：无
>
> 输出：user 用户名 password 密码 set 服务商信息 ip ip地址
>
> 作用：获取用户信息
>
> 调用：[path](#path) [get_host_ip](#get_host_ip)

```python
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

```

### set_start

> 类型：Void
>
> 输入：无
>
> 输出：无
>
> 作用：将程序添加进注册表以达到开机自启
>
> 调用：[path](#path)

```python
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
```

### post

> 类型：String
>
> 输入：user 用户名 password 密码 set 服务商 ip IP地址
>
> 输出：“连接成功” 连接成功 “连接失败” 连接失败
>
> 作用：向服务器发送post请求代替人为点击登录发送。
>
> 调用：无

```python
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
```

###  main

> 类型：Void
>
> 输入：无
>
> 输出：无
>
> 作用：调用各个函数
>
> 调用：[set_start](#set_start) [is_connect](#is_connect) [message](#message) [post](#post)

```python
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
    
```

