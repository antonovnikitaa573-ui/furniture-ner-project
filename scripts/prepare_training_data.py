import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.crawler import fetch_page, extract_product_candidates, save_html
import json

TRAINING_URLS = [
    "https://www.ikea.com/us/en/p/ektorp-sofa-90212345/",
    "https://www.ikea.com/us/en/p/malm-bed-frame-12345678/",
    "https://www.westelm.com/products/coastlinen-sofa-h1987/",
    "https://www.factorybuys.com.au/products/euro-top-mattress-king",
    "https://www.royaloakfurniture.co.uk/products/pop-bench",
    "https://www.warmnordic.com/global/products/news",
    "https://www.wardrobe-bunk-bed-sofa.uk/products/wardrobe-ava-4-3",
    "https://www.fads.co.uk/products/living/sofas/sofa-beds/",
    "https://www.fiveelementsfurniture.com/collections/sola-office-collection/products/sola-lift-desk",
    "https://www.mybudgetfurniture.com/products/3pc-sectional",
    "https://www.fads.co.uk/products/living/sofas/sofa-beds/",
    "https://www.mybudgetfurniture.com/products/3pc-sectional",
    "https://floydhome.com/products/the-floyd-hat",
    "https://viesso.com/products/haru-bed",
    "https://www.comfortfurniture.com.sg/sale/products/office",
    "https://runyonsfinefurniture.com/products/alf-bar-stool",
    "https://distinctive-interiors.com/products/",
    "https://www.yellowleafhammocks.com/products/hammock-gift-card",
    "https://www.loungesplus.com.au/products/baird-fabric-lounge-package"
]

def main():
    data_dir = PROJECT_ROOT / "data" / "training"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    training_data = []
    
    for url in TRAINING_URLS:
        print(f"Обработка: {url}")
        html = fetch_page(url)
        if html:

            html_path = save_html(url, html, data_dir)

            candidates = extract_product_candidates(html)
            
            if candidates:
                training_data.append({
                    "url": url,
                    "html_file": str(html_path),
                    "product_name": candidates[0],  
                    "context": html[:2000]
                })
                print(f"  ✅ Добавлен: {candidates[0]}")
    
    # Сохраняем
    output_path = data_dir / "training_data.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Сохранено {len(training_data)} примеров в {output_path}")

if __name__ == "__main__":
    main()