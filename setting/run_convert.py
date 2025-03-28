import subprocess
import os

PYTHON_SCRIPT = "scripts/convert_csv.py"
CSV_SOURCE = "data/GLB.Ts+dSST.csv"
DOCKER_IMAGE = "ccsv"


def run_convert_in_ccsv():
    if not os.path.exists(CSV_SOURCE):
        print(f"❌ 원본 파일이 존재하지 않습니다: {CSV_SOURCE}")
        return

    if not os.path.exists(PYTHON_SCRIPT):
        print(f"❌ 변환 스크립트가 존재하지 않습니다: {PYTHON_SCRIPT}")
        return

    print(f"🚀 컨테이너에서 {PYTHON_SCRIPT} 실행 중...")
    subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/workspace",
        DOCKER_IMAGE,
        "python", PYTHON_SCRIPT
    ], check=True)

    print("✅ 변환 완료: data/glb_temp.csv 생성됨")


if __name__ == "__main__":
    run_convert_in_ccsv()
