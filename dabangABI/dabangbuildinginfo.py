# -*- coding: utf-8 -*-

from decimal import Decimal
from email.headerregistry import HeaderRegistry
from logging import raiseExceptions
import site
from ssl import Purpose
import string
from turtle import pu
from bs4 import BeautifulSoup as bs
import requests
from tkinter import *
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
import os
import re
import random
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import keyboard
import sys
import win32clipboard
import chromedriver_autoinstaller
import time
import winsound
import math


os.system("cls")
print("Starting ...\n")
print("  ┏━")
print("   ※ 작업용 크롬이 켜지면 시작합니다.")
print("                                    ━┛")

# 크롬드라이버
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
wait = WebDriverWait(driver, 5)
hangul_re = re.compile(r"[ㄱ-ㅣ가-힣]")
korean = re.compile("[\u3131-\u3163\uac00-\ud7a3]+")
dongconverter = {
    "성정동": "10200",
    "백석동": "10300",
    "두정동": "10400",
    "성성동": "10500",
    "차암동": "10600",
    "쌍용동": "10700",
    "원성동": "10700",
    "청수동": "10900",
    "삼룡동": "11000",
    "청당동": "11100",
    "봉명동": "11300",
    "신방동": "11600",
    "신부동": "11800",
}
sigunguconverter = {
    "성정동": "44133",
    "백석동": "44133",
    "두정동": "44133",
    "성성동": "44133",
    "차암동": "44133",
    "쌍용동": "44133",
    "원성동": "44131",
    "청수동": "44131",
    "삼룡동": "44131",
    "청당동": "44131",
    "봉명동": "44131",
    "신방동": "44131",
    "신부동": "44131",
}
purposeconvert = {
    "단독주택": "단독주택",
    "다가구주택": "단독주택",
    "다중주택": "단독주택",
    "오피스텔": "업무시설",
    "업무시설": "업무시설",
    "고시원": "제2종근린생활시설",
    "다세대주택": "공동주택",
    "도시형생활주택": "공동주택",
    "사무소": "제2종근린생활시설",
    "사무실": "제2종근린생활시설",
    "원룸형주택": "공동주택",
    "아파트": "공동주택",
    "제2종근린생활시설": "제2종근린생활시설",
    "연립주택": "공동주택",
    "제1종근린생활시설": "제1종근린생활시설",
}
regex = "\(.*\)|\s-\s.*"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
}

# 코드 시작
os.system("cls")
driver.switch_to.window(driver.window_handles[0])

while True:
    while True:
        while True:
            key = keyboard.read_key()
            if key == "`":
                break
            else:
                pass

        # 주소 가져오기
        address = None
        try:
            address = driver.find_element(
                by=By.XPATH, value='//p[contains(text(),"지    번")]'
            ).text
            # 띄어쓰기 기준 문자열 나누기
            address = address.split()
            # 동과 번지 가져오기
            site_bunji = address[-1]
            site_dong = address[-2]
            # element 기다리지 않기
            driver.implicitly_wait(0)
            # 호수 가져오기 / 값이 없으면 다른 칸에서 가져오기 그래도 없으면 오류 출력
            try:
                site_ho = driver.find_element(
                    by=By.XPATH, value='//*[@id="content"]/div[4]/div/div/div[2]/section/div[1]/div[2]/label[2]/input',).get_attribute("value")
                if site_ho == "":
                    raise
            except:
                try:
                    site_ho = driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="content"]/div[4]/div/div/div[2]/section/div[1]/div[2]/label/input',
                    ).get_attribute("value")
                    if site_ho == "":
                        raise
                except:
                    print("오류:호수를 찾을 수 없습니다.")
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    break

            print("주소 : " + site_dong, site_bunji, site_ho + "호")
        except:
            # 오류 나면 출력
            print("오류:주소를 알 수 없습니다")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            os.system("cls")
            break

        # 동 칸이 있으면 체크박스 체크 없으면 패스
        if (
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[4]/div/div/div[2]/section/div[1]/div[2]/label[1]/p',
            ).text
            == "호"
        ):
            pass
        elif (
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[4]/div/div/div[2]/section/div[1]/div[2]/label[1]/p',
            ).text
            == "동"
        ):
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[4]/div/div/div[2]/section/div[1]/label/input',
            ).click()
            print("체크박스를 체크했습니다.")
        else:
            print("체크박스 확인에 실패하였습니다.")

        # 번지 추출
        bunji = None

        # - 가 없을때 번 추출
        bun = None
        bun = site_bunji

        # - 가 있으면 지를 나누어서 저장
        if "-" in site_bunji:
            ji = site_bunji[site_bunji.find("-") + 1:]
            bun = site_bunji[: site_bunji.find("-")]

        # - 가 없으면 지를 0000으로 저장
        else:
            ji = "0000"

        # 번/지를 4자리로 만들기
        bun = bun.zfill(4)
        ji = ji.zfill(4)

        # 동코드와 시군구 코드로 변환시키기
        dongcode = dongconverter[site_dong]
        sigunguCd = sigunguconverter[site_dong]

        # 표제부 html 요청
        html = None
        print("요청중입니다(표제부) (" + sigunguCd, dongcode, bun, ji + ")")
        html = requests.get(
            "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo?serviceKey=boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D&sigunguCd="
            + sigunguCd
            + "&bjdongCd="
            + dongcode
            + "&platGbCd=0&bun="
            + bun
            + "&ji="
            + ji
            + "&numOfRows=1000&pageNo=1"
        )

        # 접속 성공/실패 출력
        if html.status_code == 200:
            print("접속 \033[32m성공\033[37m")
            winsound.MessageBeep(type=-1)
        else:
            print("접속 \033[31m실패\033[37m")
            raise

        # bs 선언
        soup = None
        soup = bs(html.text, "lxml")

        # 즉시입주 체크
        driver.find_element(
            by=By.XPATH,
            value='//*[@id="content"]/div[6]/div/div/div[2]/section/div/div/label[2]/p',
        ).click()

        # 호실용도 > 층용도 > 주용도 가져오기
        purpose = None
        try:
            print("요청중입니다(전유공용면적) (" + sigunguCd, dongcode, bun, ji, site_ho + ")")
            ho_purposebs = None
            ho_purposebs = requests.get(
                "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo?serviceKey=boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D&numOfRows=1000&pageNo=1&sigunguCd="
                + sigunguCd
                + "&bjdongCd="
                + dongcode
                + "&platGbCd=0&bun="
                + bun
                + "&ji="
                + ji
                + "&hoNm="
                + site_ho
            )
            if ho_purposebs.status_code == 200:
                print("접속 \033[32m성공\033[37m")
                winsound.MessageBeep(type=-1)
            else:
                print("접속 \033[31m실패\033[37m")
                raise

            ho_purposebs = bs(ho_purposebs.text, "lxml")

            purpose = (
                ho_purposebs.find("expospubusegbcd", string="1")
                .parent.find("etcpurps")
                .get_text()
            )
            print("호실 용도 : " + purpose)
        except:
            try:
                print(
                    "요청중입니다(전유공용면적) (" + sigunguCd,
                    dongcode,
                    bun,
                    ji,
                    site_ho + "호" + ")",
                )
                ho_purposebs = None
                ho_purposebs = requests.get(
                    "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo?serviceKey=boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D&numOfRows=1000&pageNo=1&sigunguCd="
                    + sigunguCd
                    + "&bjdongCd="
                    + dongcode
                    + "&platGbCd=0&bun="
                    + bun
                    + "&ji="
                    + ji
                    + "&hoNm="
                    + site_ho
                    + "호"
                )
                if ho_purposebs.status_code == 200:
                    print("접속 \033[32m성공\033[37m")
                    winsound.MessageBeep(type=-1)
                else:
                    print("접속 \033[31m실패\033[37m")
                    raise

                ho_purposebs = bs(ho_purposebs.text, "lxml")

                purpose = (
                    ho_purposebs.find("expospubusegbcd", string="1")
                    .parent.find("etcpurps")
                    .get_text()
                )
                print("호실 용도 : " + purpose)
            except:
                try:
                    print("요청중입니다(층별 개요) (" + sigunguCd, dongcode, bun, ji + ")")
                    floor_purposebs = requests.get(
                        "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrFlrOulnInfo?serviceKey=boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D&bjdongCd="
                        + dongcode
                        + "&platGbCd=0&bun="
                        + bun
                        + "&ji="
                        + ji
                        + "&numOfRows=10&pageNo=1&sigunguCd="
                        + sigunguCd
                    )

                    # 접속 성공 시 메세지
                    if floor_purposebs.status_code == 200:
                        print("접속 \033[32m성공\033[37m")
                        winsound.MessageBeep(type=-1)
                    else:
                        print("접속 \033[31m실패\033[37m")
                        raise

                    floor_purposebs = bs(floor_purposebs.text, "lxml")

                    if len(site_ho) == 3:
                        site_ho_floor = site_ho[0]
                    elif len(site_ho) == 4:
                        site_ho_floor = site_ho[0:1]

                    purpose = (
                        floor_purposebs.find(
                            "flrnonm", string=site_ho_floor + "층")
                        .parent.find("mainpurpscdnm")
                        .get_text()
                    )
                    print("층 용도 : " + purpose)
                except:
                    purpose = soup.find("etcpurps").get_text()

        # 특수기호 제거
        purpose = re.sub(regex, "", purpose)
        purpose = re.sub(" ", "", purpose)

        # 용도에 맞게 드롭다운 메뉴 선택
        selectbox = Select(driver.find_element(
            by=By.NAME, value="principalUseType"))

        if "," not in purpose:
            try:
                purpose_sorted = purposeconvert[purpose]
            except:
                purpose_sorted = purpose

            if purpose_sorted == "단독주택":
                selectbox.select_by_index(1)
                print("주용도 : 단독주택")

            elif purpose_sorted == "공동주택":
                selectbox.select_by_index(2)
                print("주용도 : 공동주택")

            elif purpose_sorted == "제1종근린생활시설":
                selectbox.select_by_index(3)
                print("주용도 : 제1종근린생활시설")

            elif purpose_sorted == "제2종근린생활시설":
                selectbox.select_by_index(4)
                print("주용도 : 제2종근린생활시설")

            elif purpose_sorted == "업무시설":
                selectbox.select_by_index(5)
                print("주용도 : 업무시설")

            else:
                print("주용도 : " + purpose_sorted)

        elif "," in purpose:
            # 콤마가 있다면 직접 입력
            selectbox.select_by_index(0)
            selectbox.select_by_index(6)
            driver.find_element(
                by=By.NAME, value="principalUse").send_keys(purpose)
            print("주용도 : " + purpose)
        else:
            # 오류 출력
            print("건축물 주용도를 선택할 수 없습니다.")
            print("(주용도 : " + purpose + ")")
            raise

        # 건축물 사용승인일
        try:
            if (
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[4]/div/div/div[3]/section/div/div[1]/select',
                ).get_attribute("name")
                == "principalUseType"
            ):
                raise
            else:
                selectbox1 = Select(
                    driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="content"]/div[4]/div/div/div[3]/section/div/div[1]/select',
                    )
                )

        except:
            selectbox1 = Select(
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[4]/div/div/div[4]/section/div/div[1]/select',
                )
            )

        # 드롭다운 메뉴에서 사용승인일 클릭
        try:
            selectbox1.select_by_index(1)
            print("사용승인일 선택 \033[32m성공\033[37m")
        except:
            # 오류 출력
            print("사용승인일 선택 \033[31m실패\033[37m")
            break

        # 사용승인일 가져오고 입력
        try:
            useaprday = soup.find("useaprday").get_text()
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[4]/div/div/div[4]/section/div/div[1]/div/div/div/input',
            ).clear()
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[4]/div/div/div[4]/section/div/div[1]/div/div/div/input',
            ).send_keys(useaprday)
            print("사용승인일 입력 \033[32m성공\033[37m")
            print("사용승인일 : " + useaprday)
        except:
            try:
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[4]/div/div/div[4]/section/div/div[1]/div/div/div/input',
                ).clear()
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[4]/div/div/div[4]/section/div/div[1]/div/div/div/input',
                ).send_keys(useaprday)
            except:
                print("사용승인일 입력 \033[31m실패\033[37m")
                print("사용승인일 : " + useaprday)

        # 전용 면적
        try:
            print("요청중입니다(전유공용면적) (" + sigunguCd, dongcode, bun, ji, site_ho + ")")
            html_purpose = None
            html_purpose = requests.get(
                "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo?serviceKey=boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D&numOfRows=1000&pageNo=1&sigunguCd="
                + sigunguCd
                + "&bjdongCd="
                + dongcode
                + "&platGbCd=0&bun="
                + bun
                + "&ji="
                + ji
                + "&hoNm="
                + site_ho
                + "",
                headers=headers,
            )
            if html_purpose.status_code == 200:
                print("접속 \033[32m성공\033[37m")
                winsound.MessageBeep(type=-1)
            else:
                print("접속 \033[31m실패\033[37m")
                raise

            # 면적 가져오기
            soup_purpose = bs(html_purpose.text, "lxml")
            indcut = soup_purpose.find("expospubusegbcd", string="1").parent
            areafind = str(indcut).find("<area/>")
            indcut = str(indcut)[areafind + 7:]
            finalsplit = str(indcut).find("<")
            indcut = indcut[:finalsplit]
            area = indcut

            # 공급 면적 가져오기
            # 면적들 반환해서 리스트 만들기
            arealist = []
            a = soup_purpose.find("expospubusegbcd").parent
            while True:
                try:
                    arealist.append(a.contents[1])
                    a = a.next_sibling
                except:
                    break

            # 면적 리스트 float형으로 변환
            arealist_float = []
            for i in arealist:
                arealist_float.append(float(i))

            area_big = sum(arealist_float)

            area_big_flooring = str(math.floor(float(area_big) * 100) / 100.0)
            area_big = str(area_big)

            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[2]/label[2]/input',
            ).clear()
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[2]/label[2]/input',
            ).send_keys(area)
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[1]/label[2]/input',
            ).clear()
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[1]/label[2]/input',
            ).send_keys(area_big)

            print("전용면적 입력 \033[32m성공\033[37m(" +
                  area, area_big_flooring + ")")

        except:
            try:
                print("전용면적 입력 \033[31m실패\033[37m")
                print(
                    "재접속 시도(전유공용면적) (" + sigunguCd,
                    dongcode,
                    bun,
                    ji,
                    site_ho + "호" + ")",
                )

                html_purpose = None
                html_purpose = requests.get(
                    "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo?serviceKey=boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D&numOfRows=1000&pageNo=1&sigunguCd="
                    + sigunguCd
                    + "&bjdongCd="
                    + dongcode
                    + "&platGbCd=0&bun="
                    + bun
                    + "&ji="
                    + ji
                    + "&hoNm="
                    + site_ho
                    + "호"
                )
                if html_purpose.status_code == 200:
                    print("접속 \033[32m성공\033[37m")
                    winsound.MessageBeep(type=-1)
                else:
                    print("접속 \033[31m실패\033[37m")
                    raise

                # 슬라이싱해서 면적 가져오기
                soup_purpose = bs(html_purpose.text, "lxml")
                indcut = soup_purpose.find(
                    "expospubusegbcd", string="1").parent
                areafind = str(indcut).find("<area/>")
                indcut = str(indcut)[areafind + 7:]
                finalsplit = str(indcut).find("<")
                indcut = indcut[:finalsplit]
                area = indcut

                # 공급 면적 가져오기
                # 면적들 반환해서 리스트 만들기
                arealist = []
                a = soup_purpose.find("expospubusegbcd").parent
                while True:
                    try:
                        arealist.append(a.contents[1])
                        a = a.next_sibling
                    except:
                        break

                # 면적 리스트 float형으로 변환
                arealist_float = []
                for i in arealist:
                    arealist_float.append(float(i))

                area_big = sum(arealist_float)

                area_big_flooring = str(math.floor(
                    float(area_big) * 100) / 100.0)
                area_big = str(area_big)

                driver.find_element(
                    by=By.NAME,
                    value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[2]/label[2]/input',
                ).clear()
                driver.find_element(
                    by=By.NAME,
                    value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[2]/label[2]/input',
                ).send_keys(area)
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[1]/label[2]/input',
                ).clear()
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[7]/div/div/div[1]/section/div[1]/label[2]/input',
                ).send_keys(area_big)

                print("전용면적 입력 \033[32m성공\033[37m(" +
                      area, area_big_flooring + ")")
            except:
                print("전용면적 입력 \033[31m실패\033[37m")

        # 건물 층수
        try:
            # 총 층 가져오고 선택
            totalfloor = soup.find("grndflrcnt").get_text()
            select_floor = Select(
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[7]/div/div/div[2]/section/div/select[1]',
                )
            )
            select_floor.select_by_index(int(totalfloor))

            # 호에서 층 추출
            if len(site_ho) == 3:
                site_ho_floor = site_ho[0]
            elif len(site_ho) == 4:
                site_ho_floor = site_ho[0:1]

            # 해당 층 선택
            select_floor_current = Select(
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[7]/div/div/div[2]/section/div/select[2]',
                )
            )
            select_floor_current.select_by_index(int(site_ho_floor) + 2)

            print("건물 층수 : 전체", totalfloor + "층 중", site_ho_floor + "층")
        except:
            print("건물 층수 입력 \033[31m실패\033[37m")

            totalfloor = None
            totalfloor = soup.find("grndflrcnt").get_text()

        # 욕실 수
        try:
            select_bathroom = Select(
                driver.find_element(by=By.NAME, value="bathNum"))
            select_bathroom.select_by_index(1)
            print("욕실 수 입력 \033[32m성공\033[37m")
        except:
            print("욕실 수 입력 \033[31m실패\033[37m")

        # 난방 종류 선택
        try:
            select_boiler = Select(
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[7]/div/div/div[5]/section/select',
                )
            )
            select_boiler.select_by_index(2)
            print("난방 종류 입력 \033[32m성공\033[37m")
        except:
            print("난방 종류 입력 \033[31m실패\033[37m")

        # 엘레베이터
        elv = int(soup.find("emgenuseelvtcnt").get_text())
        elv = elv + int(soup.find("rideuseelvtcnt").get_text())

        if elv >= 1:
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[7]/div/div/div[9]/section/div/label[2]/p',
            ).click()
            print("엘레베이터 있음(갯수 : " + str(elv) + ")")
        else:
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[7]/div/div/div[9]/section/div/label[1]/p',
            ).click()
            print("엘레베이터 없음")

        # 주차
        # 주차 가능 댓수 가져오기
        try:
            parkings = 0
            parking1 = soup.find("indrautoutcnt").get_text()
            parking2 = soup.find("indrmechutcnt").get_text()
            parking3 = soup.find("oudrautoutcnt").get_text()
            parking4 = soup.find("oudrmechutcnt").get_text()
            parkings = int(parking1) + int(parking2) + \
                int(parking3) + int(parking4)

            if not parkings == 0:
                # 가능 선택
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[7]/div/div/div[10]/section/div/label[2]/p',
                ).click()
                driver.find_element(by=By.NAME, value="parkingNum").clear()
                driver.find_element(
                    by=By.NAME, value="parkingNum").send_keys(parkings)

            print("주차대수 입력 \033[32m성공\033[37m(" + str(parkings) + ")")
        except:
            print("주차대수 입력 \033[31m실패\033[37m")

        # 공용관리비
        try:
            driver.find_element(
                by=By.XPATH, value='//*[text() = "청소비"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "승강기유지비"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "인터넷"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "유선TV"]').click()
            driver.find_element(
                by=By.XPATH, value='(//p[text() = "기타"])[2]').click()
            print("공용관리비 체크 \033[32m성공\033[37m")
        except:
            print("공용관리비 체크 \033[31m실패\033[37m")

        # 개별사용료
        try:
            driver.find_element(
                by=By.XPATH, value='//*[text() = "난방비"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "전기료"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "가스사용료"]').click()
            print("개별사용료 체크 \033[32m성공\033[37m")
        except:
            print("개별사용료 체크 \033[31m실패\033[37m")

        # 추가 옵션
        try:
            driver.find_element(
                by=By.XPATH, value='//*[text() = "에어컨"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "세탁기"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "옷장"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "TV"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "신발장"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "냉장고"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "가스레인지"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "전자도어락"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "공동현관 보안"]').click()
            driver.find_element(
                by=By.XPATH, value='//*[text() = "인터폰"]').click()
            print("추가옵션 체크 \033[32m성공\033[37m")
        except:
            print("추가옵션 체크 \033[31m실패\033[37m")

        # 중개 의뢰 방법
        try:
            select_method = Select(
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="content"]/div[10]/div/div/div[1]/section/div[2]/select',
                )
            )
            select_method.select_by_index(1)
            print("중개 의뢰 방법 선택 \033[32m성공\033[37m")
        except:
            print("중개 의뢰 방법 선택 \033[31m실패\033[37m")

        # 마이홈 추가노출 선택
        try:
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="content"]/div[10]/div/div/div[2]/section/div/div/label[1]',
            ).click()
            print("마이홈 추가노출 선택 \033[32m성공\033[37m")
        except:
            print("마이홈 추가노출 선택 \033[31m실패\033[37m")

        print("완료\n\n\n\n\n\n")
