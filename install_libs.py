import subprocess
import sys
from pathlib import Path

LIBS_DIR = Path(__file__).parent / "libs"
LIBS_DIR.mkdir(exist_ok=True)

DEPENDENCIES = [
    "torch>=2.9.0",           
    "transformers>=4.50.0",
    "gradio>=5.0.0",
    "requests>=2.32.0",
    "beautifulsoup4>=4.13.0",
    "selenium>=4.30.0",
    "webdriver-manager>=4.0.2",
    "tqdm>=4.67.0",
    "pandas>=2.2.0",
    "numpy>=2.0.0",
]

def install_libs():
    print(f"📦 Установка в {LIBS_DIR}")
    for dep in DEPENDENCIES:
        print(f"  Установка {dep}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--target", str(LIBS_DIR),
                "--upgrade",
                dep
            ])
        except Exception as e:
            print(f"    Ошибка: {e}")

if __name__ == "__main__":
    install_libs()
    print("\n✅ Готово!")