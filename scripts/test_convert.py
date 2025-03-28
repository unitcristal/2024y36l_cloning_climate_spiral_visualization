import pandas as pd
import sys

FILE_PATH = "data/glb_temp.csv"
REQUIRED_COLUMNS = ["Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

try:
    df = pd.read_csv(FILE_PATH)
except Exception as e:
    print(f"❌ 파일을 열 수 없습니다: {FILE_PATH}\n{e}")
    sys.exit(1)

missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing_cols:
    print(f"❌ 누락된 열이 있습니다: {missing_cols}")
    sys.exit(1)


def is_valid(val):
    try:
        float(val)
        return True
    except:
        return val == "***"


invalids = []
for col in REQUIRED_COLUMNS[1:]:
    invalid_values = df[~df[col].apply(is_valid)][col].tolist()
    if invalid_values:
        invalids.append((col, invalid_values[:3]))

if invalids:
    print("❌ 유효하지 않은 anomaly 값이 있습니다:")
    for col, vals in invalids:
        print(f"  - {col}: 예시 → {vals}")
    sys.exit(1)

print("✅ glb_temp.csv 테스트 통과!")
