# -*- coding = utf-8 -*-
# Author: 
# @Time : 2023/7/19 21:30
# @File : select_piano.py
# @Software: pythonProject
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
        return "出错，未定位到元素"


def self_input(xpath, input_element, driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).send_keys(input_element)
    except:
        return "出错，未定位到元素"


def self_input_enter(xpath, input_element, driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).send_keys(input_element, Keys.ENTER)
    except:
        return "出错，未定位到元素"


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
    time.sleep(1)
    relocate()

    self_click('/html/body/div[4]/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[1]/div/input')
    self_click('//*[@id="buttons"]/button[2]')
    self_click('//*[@id="courseBtn"]')
    relocate()

    times = 0
    run = True

    while run:
        self_click('//*[@id="aPublicCourse"]')
        relocate()

        self_input_enter('//*[@id="publicSearch"]', "钢琴")
        relocate()

        times += 1
        print("尝试次数: {}".format(times), end=' ')
        for i in range(1, 4):
            course = driver.find_element(
                By.XPATH,
                '//*[@id="publicBody"]/div[{}]/div[@class="cv-title-col"]'.format(i)
            ).text
            is_full = re.findall("已满", course)
            is_conflict = re.findall("冲突", course)
            if is_full or is_conflict:
                print(course + "[0{}]".format(i), end=' ')
            else:
                self_click('//*[@id="publicBody"]/div[{}]/div[@class="cv-setting-col "]/a'.format(i))
                self_click('//*[@id="cvDialog"]/div[2]/div[2]/div[1]')
                print('\n' + course + "[0{}]".format(i), "success")
                run = False
                break
        print("")
        time.sleep(refresh_time)
        driver.refresh()
        relocate()
