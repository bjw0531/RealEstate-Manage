# -*- coding: utf-8 -*-
from pynput import keyboard
import win32clipboard
from selenium.webdriver.support.ui import Select
import re
import PublicDataReader as pdr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.keys import Keys


from data import *
from BuildingInfoParser import *


os.system("cls")
print("Starting ...\n")
print("  ┏━")
print("   ※ 작업용 크롬이 켜지면 시작합니다.")
print("                                    ━┛")


options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
serviceKey = """boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D"""
bd = pdr.Building(serviceKey, debug=True)
os.system("cls")


def on_press(key):
    try:
        if key.char == "`":
            # Stop listener
            return False
    except AttributeError:
        pass


while True:
    try:
        with keyboard.Listener(on_press=on_press, on_release="") as listener:
            listener.join()
    except:
        continue

    # 주소 가져오기
    address = driver.find_element(
        by=By.XPATH, value='//p[contains(text(),"지    번")]'
    ).text
    address_trim = address.replace("지    번 : ", "")
    address_split = address_trim.split()

    # 동 번지 구하기
    dong = address_split[3]
    bunji = address_split[4]

    if "-" in bunji:
        bunji_split = bunji.split()
        bun = bunji_split[0]
        ji = bunji_split[1]
    else:
        bun = bunji
        ji = "0000"

    bun = bun.zfill(4)
    ji = ji.zfill(4)

    # 동 체크박스 체크하고 호, 층 가져오기
    is_dong = driver.find_element(
        By.XPATH,
        '//*[@id="content"]/div[4]/div/div/div[2]/section/div[1]/div[2]/label/input',
    ).get_attribute("name")

    if is_dong == "dong":
        driver.find_element(By.NAME, "isNoinfoDong").click()

    ho = driver.find_element(By.NAME, "ho").get_attribute("value")
    floor = ho[:-2]

    # 동코드 시군구코드
    dongcode = dongconvert[dong]
    sigunguCd = sigunguCdconvert[dong]

    # 세션 만들기

    print("세션 만드는중..")
    print(
        f"""
- - - - - -
동 = {dong}  주소 = {address}  
번 = {bun}  지 = {ji}
층 = {floor}  호 = {ho}  
- - - - - -
        """
    )

    session = newsession()
    print("표제부 세션 요청 중..")
    session.표제부(sigunguCd, dongcode, bun, ji)
    print("전유공용면적 세션 요청 중..")
    session.전유공용면적(sigunguCd, dongcode, bun, ji)
    print("층별개요 세션 요청 중..")
    session.층별개요(sigunguCd, dongcode, bun, ji)
