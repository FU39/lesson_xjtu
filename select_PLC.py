# -*- coding = utf-8 -*-
# Author: 
# @Time : 2023/7/19 21:00
# @File : select_PLC.py
# @Software: pythonProject
import operator
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

delay = 0.6
refresh_time = 0.7
username = "xxx"
password = "xxx"
# 启动 chromedriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1920x1080')
# 创建 WebDriver 对象，指明使用chrome浏览器驱动
# driver = webdriver.Chrome(executable_path='d:\selenium\chromedriver.exe',chrome_options = options) # linux版本，无图形
driver = webdriver.Chrome()


def self_click(xpath, driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        temp = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", temp)
        driver.switch_to.window(driver.window_handles[-1])
    except:
        print("出错，未定位到元素")


def self_input(xpath, input_element, driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).send_keys(input_element)
    except:
        print("出错，未定位到元素")


def relocate():
    time.sleep(delay)
    search_window = driver.current_window_handle  # 此行代码用来定位当前页面


if __name__ == "__main__":
    driver.get("http://due.xjtu.edu.cn/")
    self_click("/html/body/div[5]/div[1]/div[3]/div[4]/table/tbody/tr[2]/td[1]/a/img")

    relocate()

    self_input('//*[@id="form1"]/input[1]', username)
    self_input('//*[@id="form1"]/input[2]', password)
    self_click('//*[@id="account_login"]')

    relocate()

    self_click('/html/body/div[4]/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[1]/div/input')
    self_click('//*[@id="buttons"]/button[2]')
    self_click('//*[@id="courseBtn"]')

    relocate()
    times = 0

    while True:
        times += 1
        self_click('//*[@id="recommendBody"]/div[@coursenumber="AUTO542505"]')
        course = driver.find_element(By.XPATH, '//*[@id="recommendBody"]/div[@coursenumber="AUTO542505"]/div[2]').text
        html = driver.find_element(By.XPATH, "//*").get_attribute("outerHTML")
        # print(html)
        bs = BeautifulSoup(html, 'lxml')
        course_html = bs.find('div', id="202320241AUTO54250501_courseDiv")
        is_full_try = re.findall('isfull="\d{1}"', str(course_html))
        is_full = re.findall('\d{1}', str(is_full_try))
        is_choose_try = re.findall('ischoose="1"|ischoose="null"', str(course_html))
        is_choose = re.findall('1|null', str(is_choose_try))
        print('\r'+course, "尝试次数", times, "已选?", is_choose[0], sep=' ', end='')
        if operator.eq(is_full, ['0']) and operator.eq(is_choose, ['null']):
            self_click('//*[@id="202320241AUTO54250501_courseDiv"]')
            self_click('//*[@id="202320241AUTO54250501_courseDiv"]/div[2]/div[2]/button[1]')
            print('\n'+"success")
            break
        time.sleep(refresh_time)
        driver.refresh()
        relocate()
