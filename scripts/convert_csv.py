import pandas as pd
import numpy as np

RAW_PATH = "data/GLB.Ts+dSST.csv"
OUTPUT_PATH = "data/glb_temp.csv"


def convert_csv():
    df = pd.read_csv(RAW_PATH, header=1).iloc[:, :13]

    # 마지막 데이터 확인
    last_year = df['Year'].max()
    last_month = None

    # 마지막으로 값이 있는 달 찾기
    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        if df.loc[df['Year'] == last_year, month].iloc[0] != '***':
            last_month = month

    # 다음 달 계산
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if last_month:
        next_month_idx = (months.index(last_month) + 1) % 12
        next_month = months[next_month_idx]

        # 최근 1년간의 데이터 추출
        recent_data = []
        for month in months:
            value = df.loc[df['Year'] == last_year, month].iloc[0]
            if value != '***':
                recent_data.append(float(value))

        # 평균값 계산
        avg_value = np.mean(recent_data)

        # 다음 달에 평균값 추가
        df.loc[df['Year'] == last_year, next_month] = str(avg_value)
        print(f"✅ {last_year}년 {next_month}에 최근 1년 평균값 {avg_value:.2f}를 추가했습니다")

    df[df.columns[1:]] = df[df.columns[1:]].astype(str)  # anomaly 열들을 문자열로 처리
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ 변환 완료: {OUTPUT_PATH}")


if __name__ == "__main__":
    convert_csv()
