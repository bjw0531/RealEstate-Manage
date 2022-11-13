import decimal
import re
from tkinter import *

import pandas as pd
import PublicDataReader as pdr

serviceKey = "boUDsxTChVh4mecHhfF0r1%2B3w%2FIOzO4tnvgdHmhLWsUsaX2bx%2FKspfmPnJrP1%2B6z2cBqTewiS30Lf3ohEghk9g%3D%3D"
bd = pdr.Building(serviceKey, debug=False)


class newsession:
    @staticmethod
    def 표제부(시군구코드, 법정동코드, 번, 지):
        """
        표제부 세션을 만듭니다.\n
        세션.표제부세션 으로 접근할 수 있습니다.
        """
        df = bd.read_data(category="표제부", sigunguCd=시군구코드,
                          bjdongCd=법정동코드, bun=번, ji=지)
        newsession.표제부세션 = df.head(10000)

    @staticmethod
    def 전유공용면적(시군구코드, 법정동코드, 번, 지):
        """
        전유공용면적 세션을 만듭니다.\n
        세션.전유공용면적세션 으로 접근할 수 있습니다.
        """
        df = bd.read_data(
            category="전유공용면적", sigunguCd=시군구코드, bjdongCd=법정동코드, bun=번, ji=지
        )
        newsession.전유공용면적세션 = df.head(10000)

    @staticmethod
    def 층별개요(시군구코드, 법정동코드, 번, 지):
        """
        층별개요 세션을 만듭니다.\n
        세션.층별개요세션 으로 접근할 수 있습니다.
        """
        df = bd.read_data(category="층별개요", sigunguCd=시군구코드,
                          bjdongCd=법정동코드, bun=번, ji=지)
        newsession.층별개요세션 = df.head(10000)


def 사용승인일(표제부세션):
    """
    사용승인일을 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 표제부세션
    if len(df.index) == 1:
        return df.iloc[0]["사용승인일"]
    else:
        return False


def 호실면적(전유공용면적세션, 호실):
    """
    호실면적을 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 전유공용면적세션
    df["호명칭"] = df["호명칭"].astype(str)
    df = df.loc[
        ((df["호명칭"] == str(호실)) | (df["호명칭"] == str(호실) + "호"))
        & (df["층번호명"] != "각층")
        & (df["전유공용구분코드명"] == "전유")
    ]
    if len(df.index) == 1:
        result = df.iloc[0]["면적"]
        return result
    else:
        return len(df.index)


def 공급면적(전유공용면적세션, 호실):
    """
    공급면적을 출력합니다.\n
    실패시 False를 출력합니다.
    """
    try:
        df = 전유공용면적세션
        df["호명칭"] = df["호명칭"].astype(str)
        df["면적"] = df["면적"].astype(float)
        df = df.loc[df["호명칭"] == str(호실)]

        length = len(df.index)

        arealist = list(map(str, df["면적"].values[range(length)].tolist()))

        result = decimal.Decimal("0.0")

        for i in arealist:
            result += decimal.Decimal(i)

        if result != None:
            return float(result)
        else:
            raise
    except:
        return result


def 호실용도(전유공용면적세션, 호실):
    """
    호실용도를 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 전유공용면적세션
    df["호명칭"] = df["호명칭"].astype(str)
    df = df.loc[
        ((df["호명칭"] == str(호실)) | (df["호명칭"] == str(호실) + "호"))
        & (df["층번호명"] != "각층")
        & (df["전유공용구분코드명"] == "전유")
    ]
    if len(df.index) == 1:
        result = df.iloc[0]["주용도코드명"]
        return result
    else:
        return False


def 층용도(층별개요세션, 층):
    """
    층용도를 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 층별개요세션
    df = df.loc[(df["층번호명"] == str(층) + "층")]
    if len(df.index) == 1:
        result = df.iloc[0]["기타용도"]
        result = re.sub("\(.*?\)", "", result)
        result = re.sub("\(", "", result)
        result = re.sub("\)", "", result)
        result = re.sub(" ", "", result)
        return result
    else:
        return False


def 승강기수(표제부세션):
    """
    총 승강기 수를 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 표제부세션
    if len(df.index) == 1:
        result = int(df.iloc[0]["비상용승강기수"]) + int(df.iloc[0]["승용승강기수"])
        return result
    else:
        return False


def 주차대수(표제부세션):
    """
    옥내,옥외,자주식,기계식 주차대수를 모두 더해 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 표제부세션
    if len(df.index) == 1:
        result = (
            int(df.iloc[0]["옥외자주식대수"])
            + int(df.iloc[0]["옥외기계식대수"])
            + int(df.iloc[0]["옥내자주식대수"])
            + int(df.iloc[0]["옥내기계식대수"])
        )
        return result
    else:
        return False

def 세대수(표제부세션):
    """
    가구수, 세대수, 호수를 차례대로 구하여 0이 아닌 것을 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 표제부세션
    if len(df.index) == 1:
        lst = ["가구수", "세대수", "호수"]
        for i in lst:
            result = int(df.iloc[0][i])
            if result:
                return result
        return False


def 총층수(표제부세션):
    """
    총 층수를 출력합니다.\n
    실패시 False를 출력합니다.
    """
    df = 표제부세션
    if len(df.index) == 1:
        result = df.iloc[0]["지상층수"]
        return str(result)
    else:
        return False


if __name__ == "__main__":

    session = newsession()
    session.표제부("44133", "10400", "1420", "0000")
    session.전유공용면적("44133", "10400", "1420", "0000")

    a = session.표제부세션
    b = session.전유공용면적세션

    print(세대수(a))
