import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

LIBS_PATH = PROJECT_ROOT / "libs"
if LIBS_PATH.exists():
    sys.path.insert(0, str(LIBS_PATH))

from src.crawler import fetch_page, extract_product_candidates, load_urls_from_csv

def main():
    url = None

    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"🔍 Анализ URL из аргумента: {url}")

    if not url:
        csv_path = PROJECT_ROOT / "data" / "databases" / "URL_list.csv"
        if csv_path.exists():
            urls = load_urls_from_csv(csv_path)
            if urls:
                url = urls[0]
                print(f"🔍 Анализ первого URL из CSV: {url}")
    
    if not url:
        print("❌ URL не найден. Укажите URL аргументом или добавьте URL_list.csv в data/databases/")
        print("Пример: python scripts/main.py 'https://www.ikea.com/...'")
        return
    
    print(f"\n🌐 Загрузка страницы...")
    html = fetch_page(url)
    
    if not html:
        print("❌ Не удалось загрузить страницу")
        return
    
    candidates = extract_product_candidates(html)
    
    print("\n" + "="*50)
    print("📦 НАЙДЕННЫЕ ТОВАРЫ:")
    print("="*50)
    
    if candidates:
        for i, name in enumerate(candidates[:10], 1):
            print(f"  {i}. {name}")
    else:
        print("  ❌ Товары не найдены")
    
    print("="*50)

if __name__ == "__main__":
    main()