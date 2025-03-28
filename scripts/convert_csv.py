import pandas as pd

RAW_PATH = "data/GLB.Ts+dSST.csv"
OUTPUT_PATH = "data/glb_temp.csv"


def convert_csv():
    df = pd.read_csv(RAW_PATH, header=1).iloc[:, :13]
    df[df.columns[1:]] = df[df.columns[1:]].astype(str)  # anomaly 열들을 문자열로 처리
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ 변환 완료: {OUTPUT_PATH}")


if __name__ == "__main__":
    convert_csv()
