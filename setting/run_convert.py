import subprocess
import os

PYTHON_SCRIPT = "scripts/convert_csv.py"
CSV_SOURCE = "data/GLB.Ts+dSST.csv"
DOCKER_IMAGE = "climate_spiral"


def run_convert_in_ccsv():
    """
    Docker 컨테이너에서 CSV 변환 스크립트 실행
    """
    current_dir = os.getcwd()
    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{current_dir}:/workspace",
        DOCKER_IMAGE,
        "python",
        PYTHON_SCRIPT,
    ]

    try:
        subprocess.run(cmd, check=True)
        print("✅ CSV 변환 완료")
    except subprocess.CalledProcessError as e:
        print(f"❌ CSV 변환 실패: {e}")
        raise


if __name__ == "__main__":
    run_convert_in_ccsv()
