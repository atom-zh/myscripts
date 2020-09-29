#_*_ coding:utf-8 _*_
import requests,time

s=requests.session()

data = [
  ('opr', 'pwdLogin'),
  ('Username', 'st_merge1'),
  ('Passwd', '123456'),
  ('rememberPwd', '0'),
]
while True:
    time.sleep(100)
    res=s.post("http://192.168.10.11:8080/login",data)
    print res.status_code


import time from selenium import
webdriver username = "yourusername" # 请替换成你的用户名 
password = "yourpassword" # 请替换成你的密码 
driver=webdriver.Chrome（) # 选择Chrome浏览器 
driver.get（‘http://vip.jd.com‘) # 打开京东会员网站 
time.sleep（1) driver.find_element_by_link_text（‘账户登录‘).click（) # 点击“账户登录” 
driver.find_element_by_id（‘loginname‘).click（) # 点击用户名输入框 
driver.find_element_by_id（‘loginname‘).send_keys（username) # 自动敲入用户名 
driver.find_element_by_id（‘nloginpwd‘).click（) # 点击密码输入框 
driver.find_element_by_id（‘nloginpwd‘).send_keys（password) # 自动敲入密码 
driver.find_element_by_id（‘loginsubmit‘).click（) # 点击“登录”按钮 
time.sleep（1) 
driver.find_element_by_id（‘signIn‘).click（) # 点击“签到” 
driver.close（)