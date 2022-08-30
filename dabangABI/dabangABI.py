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


def check_background_image(xpath):
    elem = driver.find_element(By.XPATH, xpath).value_of_css_property("background")
    if "check_on" in elem:
        return True
    elif "check_off" in elem:
        return False


while True:
    try:
        print("|키 입력 대기 중|")
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
    dong_checkbox = driver.find_element(By.NAME, "isNoinfoDong")
    if dong_checkbox.get_property("checked") == False:
        dong_checkbox.click()

    ho = driver.find_element(By.NAME, "ho").get_attribute("value")
    floor = ho[:-2]

    # 동코드 시군구코드
    dongcode = dongconvert(dong)
    sigunguCd = sigunguCdconvert(dong)

    # 세션 만들기

    print("세션 만드는중..")
    print(
        f"""
- - - - - -
동 = {dong}  주소 = {address_trim}  
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

    # 용도 가져오기
    try:
        ho_purpose = 호실용도(session.전유공용면적세션, ho)
        floor_purpose = 층용도(session.층별개요세션, floor)

        if ho_purpose != False:
            purpose = ho_purpose

        elif floor_purpose != False:
            purpose = floor_purpose

        else:
            raise Exception("PurposeNotFound")

        # 용도 변환
        purpose = purposeconvert[purpose]

        print("용도 :", purpose)
    except:
        print("용도 가져오기 \033[31m실패\033[0m")

    # 용도에 맞게 드롭다운 메뉴 선택
    try:
        purpose_selectbox = Select(driver.find_element(By.NAME, "principalUseType"))

        if purpose == "단독주택":
            purpose_selectbox.select_by_index(1)
        elif purpose == "공동주택":
            purpose_selectbox.select_by_index(2)
        elif purpose == "제1종근린생활시설":
            purpose_selectbox.select_by_index(3)
        elif purpose == "제2종근린생활시설":
            purpose_selectbox.select_by_index(4)
        elif purpose == "업무시설":
            purpose_selectbox.select_by_index(5)
        else:
            print("용도 알 수 없음 : %s" % purpose)
            raise
        print("용도 입력(%s)" % purpose)
    except:
        print("용도 입력 \033[31m실패\033[0m 용도 : %s" % purpose)

    # 사용승인일 입력
    try:
        useaprday_selectbox = Select(
            driver.find_element(
                By.XPATH,
                "//h1[text()='건축물 승인']/../../section/div/div/select",
            )
        )
        useaprday_selectbox.select_by_index(1)

        useaprday_textbox = driver.find_element(
            By.XPATH,
            "//h1[text()='건축물 승인']/../../section/div/div/div/div/div/input",
        )

        useaprday = 사용승인일(session.표제부세션)

        useaprday_textbox.clear()
        useaprday_textbox.send_keys(useaprday)
        print("사용승인일 입력(%s)" % useaprday)
    except:
        print("사용승인일 입력 \033[31m실패\033[0m")

    # 즉시입주
    try:
        driver.find_element(By.XPATH, '(//p[text() = "즉시입주"])').click()
        print("즉시입주 선택")
    except:
        print("즉시입주 선택 \033[31m실패\033[0m")

    # 공급 면적 입력
    try:
        supplied_area = 공급면적(session.전유공용면적세션, ho)
        if supplied_area != False:
            driver.find_elements(By.NAME, "other")[1].clear()
            driver.find_elements(By.NAME, "other")[1].send_keys(supplied_area)
            print("공급면적 입력(%s)" % supplied_area)
        else:
            raise
    except:
        print("공급면적 입력 \033[31m실패\033[0m")

    # 전용 면적 입력
    try:
        own_area = 호실면적(session.전유공용면적세션, ho)
        if own_area != False:
            driver.find_elements(By.NAME, "room")[1].clear()
            driver.find_elements(By.NAME, "room")[1].send_keys(own_area)
            print("전용면적 입력(%s)" % own_area)
        else:
            raise
    except:
        print("전용면적 입력 \033[31m실패\033[0m")

    # 전체 층 / 해당 층
    try:
        total_floor = 총층수(session.표제부세션)

        total_floor_selectbox = Select(
            driver.find_element(
                By.XPATH,
                "//h1[text()='건물 층수']/../../section/div/select",
            )
        )
        total_floor_selectbox.select_by_index(int(total_floor))

        floor_selctbox = Select(
            driver.find_element(
                By.XPATH,
                "//h1[text()='건물 층수']/../../section/div/select[2]",
            )
        )
        floor_selctbox.select_by_index(int(floor) + 2)

        print("전체 %s 층 중 %s 층 입력" % (total_floor, floor))
    except:
        print("건물 층수 입력 \033[31m실패\033[37m")

    # 욕실 수
    try:
        bathroom_selectbox = Select(driver.find_element(by=By.NAME, value="bathNum"))
        bathroom_selectbox.select_by_index(1)
        print("욕실 수 1개 입력")
    except:
        print("욕실 수 입력 \033[31m실패\033[37m")

    # 난방 종류 선택
    try:
        boiler_selectbox = Select(
            driver.find_element(
                by=By.XPATH,
                value="//h1[text()='난방 종류']/../../section/select",
            )
        )
        boiler_selectbox.select_by_index(2)
        print("난방 종류 개별 난방 입력")
    except:
        print("난방 종류 입력 \033[31m실패\033[37m")

    # 엘리베이터
    try:
        elv = 승강기수(session.표제부세션)
        elv_yes = driver.find_elements(By.XPATH, '//*[text() = "있음"]')[2]
        elv_no = driver.find_elements(By.XPATH, '//*[text() = "없음"]')[2]

        if elv >= 1:
            elv_yes.click()
            print("엘리베이터 있음 입력(%d)" % elv)

        elif elv < 1:
            print("엘리베이터 없음 입력(%d)" % elv)

    except:
        print("엘리베이터 입력 \033[31m실패\033[37m")

    # 주차
    try:
        parking = 주차대수(session.표제부세션)

        if parking >= 1:
            driver.find_element(By.XPATH, '//*[text() = "가능"]').click()

            parking_count_textbox = driver.find_element(By.NAME, "parkingNum")

            parking_count_textbox.clear()
            parking_count_textbox.send_keys(str(parking))

            print("주차 가능 입력(%d대)" % parking)

        elif parking < 1:
            driver.find_element(By.XPATH, '//*[text() = "불가능"]').click()
            print("주차 불가능 입력(%d대)" % parking)

    except:
        print("주차 가능여부 입력 \033[31m실패\033[37m")

    # 공용관리비
    try:
        public_manage_list = ["청소비", "승강기유지비", "인터넷", "유선TV"]

        for i in public_manage_list:
            if check_background_image('//*[text() = "%s"]/../input' % i) == False:
                driver.find_element(By.XPATH, '//*[text() = "%s"]/../input' % i).click()
                print("%s 체크" % i)

        if check_background_image('(//p[text() = "기타"])[2]') == False:
            driver.find_element(By.XPATH, '(//p[text() = "기타"])[2]').click()
            print("기타 체크")

    except:
        print("공용관리비 체크 \033[31m실패\033[37m")

    # 개별사용료
    try:
        private_manage_list = ["난방비", "전기료", "가스사용료"]

        for i in private_manage_list:
            if check_background_image('//*[text() = "%s"]/../input' % i) == False:
                driver.find_element(By.XPATH, '//*[text() = "%s"]/../input' % i).click()
                print("%s 체크" % i)
    except:
        print("개별사용료 체크 \033[31m실패\033[37m")

    # 추가 옵션
    try:
        options = [
            "에어컨",
            "세탁기",
            "옷장",
            "TV",
            "신발장",
            "냉장고",
            "가스레인지",
            "전자도어락",
            "공동현관 보안",
            "인터폰",
        ]

        for i in options:
            if check_background_image('//*[text() = "%s"]/../input' % i) == False:
                driver.find_element(By.XPATH, '//*[text() = "%s"]/../input' % i).click()
                print("%s 체크" % i)

    except:
        print("추가옵션 체크 \033[31m실패\033[37m")

    # 중개 의뢰 방법
    try:
        select_method = Select(
            driver.find_element(
                by=By.XPATH,
                value="//h1[text()='중개 의뢰 방법']/../../section/div[2]/select",
            )
        )
        select_method.select_by_index(1)
        print("중개 의뢰 방법 선택")
    except:
        print("중개 의뢰 방법 선택 \033[31m실패\033[37m")

    # 마이홈 추가노출 선택
    try:
        driver.find_element(
            by=By.XPATH,
            value="//*[text()='미동의']",
        ).click()
        print("마이홈 추가노출 선택")
    except:
        print("마이홈 추가노출 선택 \033[31m실패\033[37m")

    print("완료\n\n\n\n\n\n")
