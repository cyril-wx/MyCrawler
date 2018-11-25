#!/usr/bin/env python3.6

# -*- coding:UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests

from bs4 import BeautifulSoup
import json
import sys
curpath=sys.path[0]
print (curpath)

driver = webdriver.PhantomJS(executable_path='/Users/cyril/Desktop/Coding/Python/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.set_page_load_timeout(30)

# CSDN
#url="https://passport.csdn.net/passport_fe/login.html"
#user_xpath='//*[@id="all"]'
#pwd_xpath='//*[@id="password-number"]'
#login_xpath='//*[@id="app"]/div/div/div/div[2]/div[2]/form/div/div[6]/div/button'

# Baidu
url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F&sms=5"
gotologin_xpath = '//*[@id="TANGRAM__PSP_3__footerULoginBtn"]'
user_xpath = '//*[@id="TANGRAM__PSP_3__userName"]'
pwd_xpath = '//*[@id="TANGRAM__PSP_3__password"]'
login_xpath = '//*[@id="TANGRAM__PSP_3__submit"]'
certify_phone_edittext_xpath = '//*[@id="TANGRAM__30__input_vcode"]'
certify_phone_bt_xpath = '//*[@id="TANGRAM__30__button_send_mobile"]'
certify_phone_submit_xpath = '//*[@id="TANGRAM__30__button_submit"]'

driver.get(url)
time.sleep(3)
driver.get_screenshot_as_file('./scraping.png')

''' # CSDN
user_textedit=driver.find_element_by_xpath(user_xpath)
pwd_textedit=driver.find_element_by_xpath(pwd_xpath)
login_textedit=driver.find_element_by_xpath(login_xpath)

gotologin = driver.find_element_by_xpath(login_textedit)

 # CSDN
actions = ActionChains(driver).click(user_textedit).send_keys("18273494490").click(pwd_textedit).send_keys("zxc12345").send_keys(Keys.RETURN)
actions.perform()
'''

gotologin = driver.find_element_by_xpath(gotologin_xpath)
gotologin.click()


driver.get_screenshot_as_file('./scraping_2.png')

# baidu
baidu_user_textedit=driver.find_element_by_xpath(user_xpath)
baidu_pwd_textedit=driver.find_element_by_xpath(pwd_xpath)
baidu_login_textedit=driver.find_element_by_xpath(login_xpath)
# baidu
actions = ActionChains(driver).click(baidu_user_textedit).send_keys("18273494490").click(baidu_pwd_textedit).send_keys("Cyril2018").send_keys(Keys.RETURN)
actions.perform()
time.sleep(3)
driver.get_screenshot_as_file('./scraping_3.png')

html=driver.page_source #获取网页的html数据
soup=BeautifulSoup(html,'lxml')#对html进行解析
with open("baidu_login.html","w") as f:
	f.write(html)

try:
#	js = 'document.querySelector("#TANGRAM__PSP_3__verifyCode").style="";'  #js去掉上传文件“input”元素的属性，使之可见
#	driver.execute_script(js)


	certify_phone_edittext = driver.find_element_by_xpath(certify_phone_edittext_xpath)	
	certify_phone_bt = driver.find_element_by_xpath(certify_phone_bt_xpath)
	certify_phone_submit = driver.find_element_by_xpath(certify_phone_submit_xpath)

	driver.get_screenshot_as_file('./scraping_3.1.png')
	if (certify_phone_edittext):
		certify_phone_bt.click() #获取验证码
		msg_certify = input("请输入手机收到的验证码：")
		if(msg_certify):
			certify_phone_edittext.click()
			certify_phone_edittext.send_keys(msg_certify)
			certify_phone_submit.click()
			time.sleep(2)
			driver.get_screenshot_as_file('./scraping_4.png')
			html=driver.page_source #获取网页的html数据
			soup=BeautifulSoup(html,'lxml')#对html进行解析
			with open("baidu_login_aft.html","w") as f:
				f.write(html)
		else:
			print("没有输入验证码。")
		
except Exception as e:
	print("Excetion->", e)
	pass



driver.close()

