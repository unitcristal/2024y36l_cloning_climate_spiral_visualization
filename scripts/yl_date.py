from datetime import datetime
import math

"""
script summary

오늘 날짜 기준으로 2025y13l 같은 y-l 포맷 반환
월~일 한 줄 캘린더 기준 주차 계산
연말 53주차는 1주차로 순환 처리

"""


def get_yl(target_date=None):
    today = datetime.today() if target_date is None else target_date
    year = today.year
    day_of_year = int(today.strftime('%j'))
    weekday = today.isoweekday()  # 1=Mon ~ 7=Sun

    # Calculate week based on Mon-Sun single-line calendar logic
    week = math.floor((day_of_year + 6 - weekday) / 7) + 1
    if week >= 53:
        week = 1

    return f"{year}y{week:02}l"


if __name__ == "__main__":
    print(get_yl())
