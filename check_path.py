import sys
from pathlib import Path

print("ГДЕ PYTHON ИЩЕТ ФАЙЛЫ:")
print("="*50)
for i, path in enumerate(sys.path):
    print(f"{i}. {path}")

print("\n" + "="*50)
print(f"Ваша папка libs: {Path('libs').absolute()}")
print(f"Она в sys.path? {'libs' in str(sys.path)}")