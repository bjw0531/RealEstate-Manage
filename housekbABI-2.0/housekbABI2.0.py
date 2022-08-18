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

try:
    driver.implicitly_wait(0)
    driver.switch_to.frame("mainFrame")
    print("메인프레임 전환")
except:
    pass
finally:
    driver.implicitly_wait(4)


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

    # areatext 불러오기
    driver.find_element(By.ID, "area").send_keys(Keys.CONTROL + "A")
    driver.find_element(By.ID, "area").send_keys(Keys.CONTROL + "C")
    win32clipboard.OpenClipboard()
    areatext = win32clipboard.GetClipboardData()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

    driver.find_element(
        By.XPATH,
        "/html/body/table/tbody/tr/td[2]/table/tbody/tr[3]/td/form/table[4]/tbody/tr[7]/td[1]/div",
    ).click()

    areatext_splited = areatext.split()

    # 호 추출
    kor_ho = re.findall("[0-9]?[0-9][0-9][0-9]호", areatext)[0]
    ho = re.sub("호", "", kor_ho)
    floor = ho[:-2]

    # 동 추출
    dong = areatext_splited[0]
    # 시군구 코드 추출
    sigunguCd = sigunguCdconvert(dong)
    # 법정동 코드 추출
    bjdCd = dongconvert(dong)

    # 지번 추출
    address = areatext_splited[1]
    bunji = re.findall(r"\d+", address)

    # 번인지 번지인지
    if len(bunji) >= 1:
        bun = str(bunji[0])
    else:
        bun = "0000"

    if len(bunji) >= 2:
        ji = str(bunji[1])
    else:
        ji = "0000"

    bun = bun.zfill(4)
    ji = ji.zfill(4)

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
    print("표제부세션 요청 중..")
    session.표제부(sigunguCd, bjdCd, bun, ji)
    print("전유공용면적세션 요청 중..")
    session.전유공용면적(sigunguCd, bjdCd, bun, ji)
    print("층별개요세션 요청 중..")
    session.층별개요(sigunguCd, bjdCd, bun, ji)

    # 사용승인일 구하고 쓰기
    try:
        useaprday = 사용승인일(session.표제부세션)
        useaprday_dotted = useaprday[0:4] + "." + useaprday[4:6] + "." + useaprday[6:8]
        driver.find_element(By.ID, "build_access_date").clear()
        driver.find_element(By.ID, "build_access_date").send_keys(useaprday_dotted)
        print("사용승인일 입력(%s)" % useaprday_dotted)
    except:
        print("사용승인일 입력 \033[31m실패\033[0m")

    # 주차대수 구하기
    try:
        parking = 주차대수(session.표제부세션)
        driver.find_element(By.ID, "parking").clear()
        driver.find_element(By.ID, "parking").send_keys(parking)
        print("주차대수 입력(%s)" % parking)
    except:
        print("주차대수 입력 \033[31m실패\033[0m")

    # 체크박스 해제/선택
    try:
        error = 0
        publicmoney = Select(driver.find_element(By.ID, "public_money1"))
        전기 = driver.find_element(By.XPATH, '//input[@value="전기"]')
        가스 = driver.find_element(By.XPATH, '//input[@value="가스"]')
        수도 = driver.find_element(By.XPATH, '//input[@value="수도"]')
        유선 = driver.find_element(By.XPATH, '//input[@value="유선"]')
        인터넷 = driver.find_element(By.XPATH, '//input[@value="인터넷"]')
        publicmoney_list = [전기, 가스, 수도, 유선, 인터넷]

        for i in publicmoney_list:
            if i.is_selected():
                i.click()

        publicmoney_text = publicmoney.first_selected_option.text

        if publicmoney_text == "유선포함":
            전기.click()
            가스.click()
            수도.click()
            # 유선.click()
            인터넷.click()
        elif publicmoney_text == "수도포함":
            전기.click()
            가스.click()
            # 수도.click()
            유선.click()
            인터넷.click()
        elif publicmoney_text == "유선/수도포함":
            전기.click()
            가스.click()
            # 수도.click()
            # 유선.click()
            인터넷.click()
        elif publicmoney_text == "유선/수도/인터넷포함":
            전기.click()
            가스.click()
            # 수도.click()
            # 유선.click()
            # 인터넷.click()
        elif publicmoney_text == "모든공과금포함":
            # 전기.click()
            # 가스.click()
            # 수도.click()
            # 유선.click()
            # 인터넷.click()
            pass
        else:
            error = 1

        if error == 1:
            print("체크박스 체크 \033[31m실패\033[0m")
        else:
            print("체크박스 체크")
    except:
        print("체크박스 체크 \033[31m실패\033[0m")

    # 용도 가져오기
    try:
        purpose_select = Select(driver.find_element(By.NAME, "build_use_type"))
        purpose = 호실용도(session.전유공용면적세션, ho)
        if purpose == False:
            purpose = 층용도(session.층별개요세션, floor)
            if purpose == False:
                raise

        purpose = purposeconvert[purpose]
        if purpose == "단독주택":
            purpose_select.select_by_index(1)
        elif purpose == "공동주택":
            purpose_select.select_by_index(2)
        elif purpose == "업무시설":
            purpose_select.select_by_index(3)
        elif purpose == "제1종근린생활시설":
            purpose_select.select_by_index(4)
        elif purpose == "제2종근린생활시설":
            purpose_select.select_by_index(5)
        else:
            print("용도 알 수 없음 : %s" % purpose)
            raise
        print("용도 입력(%s)" % purpose)
    except:
        print("용도 입력 \033[31m실패\033[0m 용도 : %s" % purpose)

    # 면적 구하기
    try:
        area = 호실면적(session.전유공용면적세션, ho)
        if area != False:
            driver.find_element(By.ID, "size").clear()
            driver.find_element(By.ID, "size").send_keys(area)
            print("호실면적 입력(%s)" % area)
        else:
            raise
    except:
        print("호실면적 입력 \033[31m실패\033[0m")

    # 소재지 변경
    try:
        driver.find_element(By.ID, "traffice").clear()
        if purpose == "단독주택" or purpose == "공동주택":
            driver.find_element(By.ID, "traffice").send_keys(address)
            print("소재지 입력(%s)" % address)
        else:
            print("소재지 입력 X")
    except:
        print("소재지 입력 \033[31m실패\033[0m")

    # 즉시 입주 가능 변경
    try:
        driver.find_element(By.ID, "movein_day").clear()
        driver.find_element(By.ID, "movein_day").send_keys("즉시입주가능")
        print("즉시입주가능 입력")
    except:
        print("즉시입주가능 입력 \033[31m실패\033[0m")

    # 층 정보 변경

    # 총 층
    try:
        totalfloor = 총층수(session.표제부세션)
        driver.find_element(By.ID, "total_floor").clear()
        driver.find_element(By.ID, "total_floor").send_keys(totalfloor)
        print("총 층 입력(%s)" % totalfloor)
    except:
        print("총 층 입력 \033[31m실패\033[0m")

    # 현재 층
    try:
        driver.find_element(By.ID, "now_floor").clear()
        driver.find_element(By.ID, "now_floor").send_keys(floor)
        print("현재 층 입력(%s)" % floor)
    except:
        print("현재 층 입력 \033[31m실패\033[0m")

    print("완료\n\n\n\n")
