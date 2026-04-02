import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

LIBS_PATH = PROJECT_ROOT / "libs"
if LIBS_PATH.exists():
    sys.path.insert(0, str(LIBS_PATH))

from src.crawler import (
    fetch_page, 
    extract_product_candidates, 
    load_urls_from_csv, 
    save_database,
    save_html         
)

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, desc=""):
        print(desc)
        return iterable

def main():

    data_dir = PROJECT_ROOT / "data"
    csv_path = data_dir / "databases" / "URL_list.csv"
    output_path = data_dir / "databases" / "products_database.json"
    html_dir = data_dir / "raw_html"

    if not csv_path.exists():
        print(f"❌ Файл не найден: {csv_path}")
        print("Создайте файл data/databases/URL_list.csv с колонкой 'url'")
        return

    print(f"📂 Загрузка URL из: {csv_path}")
    urls = load_urls_from_csv(csv_path)
    print(f"✅ Найдено URL: {len(urls)}")
    
    database = []

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] {url[:80]}...")
        
        html = fetch_page(url)
        
        if html:

            html_path = save_html(url, html, html_dir)

            products = extract_product_candidates(html)
            
            database.append({
                "url": url,
                "products": products,
                "product_count": len(products),
                "html_file": str(html_path),
                "status": "success"
            })
            print(f"  ✅ Найдено товаров: {len(products)}")
        else:
            database.append({
                "url": url,
                "products": [],
                "product_count": 0,
                "html_file": None,
                "status": "failed"
            })
            print(f"  ❌ Не загружено")

        time.sleep(0.5)

    save_database(database, output_path)
    
    successful = sum(1 for item in database if item["status"] == "success")
    total_products = sum(item["product_count"] for item in database)
    
    print("\n" + "="*50)
    print("📊 СТАТИСТИКА:")
    print("="*50)
    print(f"  ✅ Успешно загружено: {successful}/{len(urls)}")
    print(f"  📦 Всего найдено товаров: {total_products}")
    print(f"  📁 HTML сохранены в: {html_dir}")
    print(f"  💾 База сохранена в: {output_path}")
    print("="*50)

if __name__ == "__main__":
    main()