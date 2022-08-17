donglist = [
    "두정동",
    "성성동",
    "성정동",
    "쌍용동",
    "백석동",
    "차암동",
    "신부동",
    "봉명동",
    "쌍용동",
    "청당동",
    "청수동",
    "삼룡동",
    "신방동",
]

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
    "의원": "제2종근린생활시설",
}


def dongconvert(dong):
    if dong == "성정동":
        return "10200"

    if dong == "백석동":
        return "10300"

    if dong == "두정동":
        return "10400"

    if dong == "성성동":
        return "10500"

    if dong == "차암동":
        return "10600"

    if dong == "쌍용동":
        return "10700"

    if dong == "원성동":
        return "10700"

    if dong == "청수동":
        return "10900"

    if dong == "삼룡동":
        return "11000"

    if dong == "청당동":
        return "11100"

    if dong == "봉명동":
        return "11300"

    if dong == "신방동":
        return "11600"

    if dong == "신부동":
        return "11800"


def sigunguCdconvert(dong):

    if dong == "성정동":
        return "44133"

    if dong == "백석동":
        return "44133"

    if dong == "두정동":
        return "44133"

    if dong == "성성동":
        return "44133"

    if dong == "차암동":
        return "44133"

    if dong == "쌍용동":
        return "44133"

    if dong == "원성동":
        return "44131"

    if dong == "청수동":
        return "44131"

    if dong == "삼룡동":
        return "44131"

    if dong == "청당동":
        return "44131"

    if dong == "봉명동":
        return "44131"

    if dong == "신방동":
        return "44131"

    if dong == "신부동":
        return "44131"
