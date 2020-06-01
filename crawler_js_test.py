#!/usr/bin/env python3.6
# -*- coding:UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import json

dcap = dict(DesiredCapabilities.PHANTOMJS)
# 安卓手机
# dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
# win10 谷歌浏览器
dcap['phantomjs.page.settings.userAgent']=("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
driver = webdriver.PhantomJS(executable_path='F:/我的下载/Google/phantomjs-2.1.1-windows/bin/phantomjs.exe',desired_capabilities=dcap)
driver.set_page_load_timeout(30)

# Baidu
# 百度登录页面地址（二维码登录页面）
url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F&sms=5"
# 切换账号登录的文本标签
gotologin_xpath = '//*[@id="TANGRAM__PSP_3__footerULoginBtn"]'
# 用户名的输入文本框
user_xpath = '//*[@id="TANGRAM__PSP_3__userName"]'
# 密码的输入文本框
pwd_xpath = '//*[@id="TANGRAM__PSP_3__password"]'
# 登录的Button
login_xpath = '//*[@id="TANGRAM__PSP_3__submit"]'
# 验证手机号 -> 验证码的输入文本框
certify_phone_edittext_xpath = '//*[@id="TANGRAM__30__input_vcode"]'
# 获取手机验证码 的 提交按钮
certify_phone_bt_xpath = '//*[@id="TANGRAM__30__button_send_mobile"]'
# 验证手机号 的 提交按钮
certify_phone_submit_xpath = '//*[@id="TANGRAM__30__button_submit"]'

driver.get(url) # 使用Selenium driver 模拟加载百度登录页面
time.sleep(3) # 等待3s网页加载完毕，否则后面的 截图 或者 元素定位无效，导致报错。
driver.get_screenshot_as_file('./scraping.png') # 对模拟网页实时状态截图
gotologin = driver.find_element_by_xpath(gotologin_xpath) # 使用Selenium driver 定位到 切换账号登录 标签
gotologin.click() # 模拟点击 切换账号登录 标签
time.sleep(1) # 这里其实可以不用sleep函数，因为切换到账号登录的过程只是本地js程序执行，不需要和服务器交互。
driver.get_screenshot_as_file('./scraping_2.png') # 对模拟网页实时状态截图，可与click()之前的截图对比。

# baidu
baidu_user_textedit=driver.find_element_by_xpath(user_xpath)
baidu_pwd_textedit=driver.find_element_by_xpath(pwd_xpath)
baidu_login_textedit=driver.find_element_by_xpath(login_xpath)
# ActionChains是一个动作链，使用动作链与否，其优劣各位自己评判
actions = ActionChains(driver).click(baidu_user_textedit).send_keys("18165773128").click(baidu_pwd_textedit).send_keys("zxc12345").send_keys(Keys.RETURN)
# 设定动作链之后要调用perform()函数才生效
actions.perform()
# 等待3s后，再截个图看看当前是什么状态
time.sleep(3)
driver.get_screenshot_as_file('./scraping_3.png')

try:
    html = driver.page_source  # 获取网页的html数据
    with open("baidu_login_pre.html", "w", encoding="utf-8") as f:
        f.write(html)
except Exception as e:
    print("文件:baidu_login_pre.html 保存失败. ->", e)

    #	js = 'document.querySelector("#TANGRAM__PSP_3__verifyCode").style="";'  #js去掉上传文件“input”元素的属性，使之可见
    #	driver.execute_script(js)

try:
    certify_phone_edittext = driver.find_element_by_xpath(certify_phone_edittext_xpath)
    certify_phone_bt = driver.find_element_by_xpath(certify_phone_bt_xpath)
    certify_phone_submit = driver.find_element_by_xpath(certify_phone_submit_xpath)

    driver.get_screenshot_as_file('./scraping_3.1.png')
    if (certify_phone_edittext):
        certify_phone_bt.click()  # 获取验证码
        # 命令行提示用户输入你手机收到的验证码
        msg_certify = input("请输入手机收到的验证码：")
        if (msg_certify):
                certify_phone_edittext.click()
                certify_phone_edittext.send_keys(msg_certify)
                # certify_phone_edittext.send_keys(Keys.RETURN)
                # 提交验证码
                certify_phone_submit.click()
                driver.get_screenshot_as_file('./scraping_4.png')
                time.sleep(2)
                # 再次提交登录
                baidu_login_textedit.click()
                time.sleep(4)
                try:
                    html = driver.page_source  # 获取网页的html数据
                    with open("baidu_login_test.html", "w", encoding="utf-8") as f:
                        f.write(html)
                except Exception as e:
                    print("文件:baidu_login_test.html 保存失败. ->", e)
        else:
                print("没有输入验证码。")
except Exception as e:
    print("Exception: 手机验证码验证失败，此次登录未完成 -> ", e)


try:
    # 检查模拟登录后页面的 用户名 标签，若存在此标签则说明登录成功。
    login_check_xpath = '//*[@id="s_username_top"]/span'
    login_check = driver.find_element_by_xpath(login_check_xpath)
    if(driver.find_element_by_xpath(login_check_xpath)):
        print("Successful login in.")
        # soup=BeautifulSoup(html,'lxml')#对html进行解析
        try:
            html = driver.page_source  # 获取网页的html数据
            with open("baidu_login_aft.html", "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            print("文件:baidu_login_aft.html 保存失败. ->", e)
except Exception as e:
        print("Exception: Failed to login Baidu. -> ", e)
# 最后不要忘记关闭driver
driver.close() 


