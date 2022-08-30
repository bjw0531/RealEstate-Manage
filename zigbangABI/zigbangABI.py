# -*- coding: utf-8 -*-
from pynput import keyboard
from selenium.webdriver.support.ui import Select
import PublicDataReader as pdr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.common.exceptions import NoSuchElementException

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


def CheckAndClickCB(word):
    elem = driver.find_element(By.XPATH, word)
    TorF = elem.get_property("checked")
    if TorF == False:
        elem.click()


while True:
    try:
        with keyboard.Listener(on_press=on_press, on_release="") as listener:
            listener.join()
    except:
        continue

    # 스크롤 맨 위로
    driver.execute_script("scroll(0,0)")

    # 주소 가져오기
    address = driver.find_element(By.XPATH, '//p[@class="address"]/span').text
    address = address.replace("입력한 주소: 충남 ", "")
    address_splited = address.split()

    # 동 추출
    dong = address_splited[2]
    # 시군구 코드 추출
    sigunguCd = sigunguCdconvert(dong)
    # 동코드 추출
    dongcode = dongconvert(dong)

    # 번지 추출
    bunji = address_splited[3]
    bunji_splited = address_splited[3].split("-")

    if len(bunji_splited) == 2:
        bun = bunji_splited[0]
        ji = bunji_splited[1]
    elif len(bunji_splited) == 1:
        bun = bunji_splited[0]
        ji = "0000"

    bun = bun.zfill(4)
    ji = ji.zfill(4)

    # 거래유형 누르기 (월세)
    driver.find_element(By.XPATH, "//span[text()='월세']").click()

    # 호 가져오기
    ho = driver.find_element(By.NAME, "ho").get_property("defaultValue")
    if ho == "":
        print("호를 찾을 수 없습니다!")
        raise
    floor = ho[:-2]

    # '동구분이 없음' 체크
    CheckAndClickCB('//input[@name="noDong"]')

    # 세션 요청
    print("세션 만드는중..")
    print(
        f"""
- - - - - -
동 = {dong}  주소 = {bunji}  
번 = {bun}  지 = {ji}
층 = {floor}  호 = {ho}  
- - - - - -
        """
    )
    session = newsession()
    print("표제부세션 요청 중..")
    session.표제부(sigunguCd, dongcode, bun, ji)
    print("전유공용면적세션 요청 중..")
    session.전유공용면적(sigunguCd, dongcode, bun, ji)
    print("층별개요세션 요청 중..")
    session.층별개요(sigunguCd, dongcode, bun, ji)

    # 건물 용도 가져오기
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

    # 건물 용도 입력
    try:
        if purpose == "단독주택":
            driver.find_element(By.XPATH, '//span[text() = "단독주택"]').click()
        else:
            driver.find_element(By.XPATH, '//span[text() = "그 외"]').click()
            driver.find_element(By.NAME, "residence_type").clear()
            driver.find_element(By.NAME, "residence_type").send_keys(purpose)
        print("용도 입력(%s)" % purpose)
    except:
        print("용도 입력 \033[31m실패\033[0m 용도 : %s" % purpose)

    # 전체 층 / 현재 층
    try:
        # 총 층 구하기
        total_floor = 총층수(session.표제부세션)

        # 총 층 선택
        total_floor_selectbox = Select(driver.find_element(By.NAME, "building_floor"))
        total_floor_selectbox.select_by_index(int(total_floor))

        # 현재 층 선택
        floor_selctbox = Select(driver.find_element(By.NAME, "floor"))
        floor_selctbox.select_by_index(int(floor) + 1)

        print("전체 %s 층 중 %s 층 입력" % (total_floor, floor))
    except:
        print("건물 층수 입력 \033[31m실패\033[37m")

    # 전용 면적
    try:
        own_area = 호실면적(session.전유공용면적세션, ho)
        if own_area != False:
            driver.find_element(By.NAME, "size_m2").clear()
            driver.find_element(By.NAME, "size_m2").send_keys(own_area)
            print("전용면적 입력(%s)" % own_area)
        else:
            raise
    except:
        print("전용면적 입력 \033[31m실패\033[0m")

    # 화장실 수 (1개)
    try:
        bathroom_selectbox = Select(driver.find_element(By.NAME, "bathroom_count"))
        bathroom_selectbox.select_by_index(1)
        print("화장실 수 1개 입력")
    except:
        print("화장실 수 입력 \033[31m실패\033[37m")

    # 사용승인일
    try:

        useaprday_textbox = driver.find_element(By.NAME, "approve_date")

        useaprday = 사용승인일(session.표제부세션)

        useaprday_splited = useaprday[0:4] + "." + useaprday[4:6] + "." + useaprday[6:8]

        useaprday_textbox.clear()
        useaprday_textbox.send_keys(useaprday_splited)

        print("사용승인일 입력(%s)" % useaprday_splited)
    except:
        print("사용승인일 입력 \033[31m실패\033[0m")

    # 주차
    try:
        parking = 주차대수(session.표제부세션)

        if parking >= 1:
            driver.find_element(By.XPATH, '//span[text() = "가능"]').click()
            print("주차 가능 입력")

        elif parking < 1:
            driver.find_element(By.XPATH, '//span[text() = "불가능"]"]').click()
            print("주차 불가능 입력")
    except:
        print("주차 가능여부 입력 \033[31m실패\033[37m")

    # 엘리베이터
    try:
        elv = 승강기수(session.표제부세션)
        elv_yes = driver.find_element(By.XPATH, '//span[text() = "있음"]')
        elv_no = driver.find_element(By.XPATH, '//span[text() = "없음"]')

        if elv >= 1:
            elv_yes.click()
            print("엘리베이터 있음 입력")

        elif elv < 1:
            elv_no.click()
            print("엘리베이터 없음 입력")

    except:
        print("엘리베이터 입력 \033[31m실패\033[37m")

    # 관리비 포함 항목 (수도,인터넷,TV)
    try:
        public_manage_list = ["수도", "인터넷", "TV"]
        public_manage_dict = {"수도": "03", "인터넷": "04", "TV": "05"}
        public_manage_value = driver.find_element(
            By.NAME, "manage_cost_inc"
        ).get_property("value")

        for i in public_manage_list:
            if not public_manage_dict[i] in public_manage_value:
                driver.find_element(By.XPATH, '//span[text() = "%s"]' % i).click()
                print("%s 체크" % i)

    except:
        print("공용관리비 체크 \033[31m실패\033[37m")

    # 옵션 (에어컨,냉장고,세탁기,가스레인지,옷장,신발장,싱크대)
    try:
        options_list = ["에어컨", "냉장고", "세탁기", "가스레인지", "옷장", "신발장", "싱크대"]
        options_dict = {
            "에어컨": "01",
            "냉장고": "02",
            "세탁기": "03",
            "가스레인지": "04",
            "옷장": "10",
            "신발장": "11",
            "싱크대": "12",
        }
        options_value = driver.find_element(By.NAME, "options").get_property("value")

        for i in options_list:
            if not options_dict[i] in options_value:
                driver.find_element(By.XPATH, '//span[text() = "%s"]' % i).click()
                print("%s 체크" % i)

    except:
        print("추가옵션 체크 \033[31m실패\033[37m")

    # 입주가능일 (즉시입주)
    try:
        driver.find_element(By.XPATH, '//span[text()="즉시 입주"]').click()
        print("즉시입주 입력")
    except:
        print("즉시입주 입력 \033[31m실패\033[37m")

    # 상세 설명 입력
    try:
        description = """
★~안녕하세요~~~^^

★~정말 저렴하게 나온 집이에요~
금방 나갈수 있으니 서둘러 주시구요~
바로 이사 가능하구요~
보증금 조절 또한 가능~
언제든지 부담없이 보러와주세요~


# 주차대수 : 총 %s대
# 사용승인일 : %s
# 방수/욕실수 : 1개/1개
""" % (
            str(parking),
            str(useaprday),
        )

        driver.find_element(By.NAME, "description").clear()
        driver.find_element(By.NAME, "description").send_keys(description)
        print("상세설명 입력")
    except:
        print("상세설명 입력 \033[31m실패\033[37m")

    # 담당자 추가
    try:
        # 삭제하기 버튼 있는지 확인
        try:
            driver.find_element(By.XPATH, "//*[text()='삭제하기']/.")
        except NoSuchElementException:
            driver.find_element(By.XPATH, "//*[text()='+ 담당자 추가']/.").click()
            agent_selectbox = Select(driver.find_element(By.NAME, "agent_no"))
            agent_selectbox.select_by_index(2)
            print("담당자 추가")

    except:
        print("담당자 추가 \033[31m실패\033[37m")

    # 중개 의뢰 받을 방법 설정 (전화)
    try:
        driver.find_element(By.XPATH, "//*[text()='전화로 확인']").click()
        print("중개 의뢰 방법 입력")
    except:
        print("중개 의뢰 방법 입력 \033[31m실패\033[37m")

    # 규정 동의
    try:
        agree_term_checkbox = driver.find_element(By.NAME, "agree_term")
        agree_term_ischecked = agree_term_checkbox.get_property("checked")

        if agree_term_ischecked == False:
            agree_term_checkbox.click()
            print("규정 동의")
    except:
        print("규정 동의 \033[31m실패\033[37m")

    print("완료\n\n\n\n\n\n")
