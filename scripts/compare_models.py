import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.model_predict import FurnitureNER
from src.crawler import fetch_page, extract_text_from_html

TEST_URL = "https://www.loungesplus.com.au/products/baird-fabric-lounge-package"

print("="*60)
print("СРАВНЕНИЕ МОДЕЛЕЙ")
print("="*60)

print(f"\n🌐 Загрузка: {TEST_URL}")
html = fetch_page(TEST_URL)
if not html:
    print("❌ Не удалось загрузить")
    sys.exit(1)

text = extract_text_from_html(html)

print("\n" + "-"*40)
print("🔄 ГОТОВАЯ МОДЕЛЬ (dslim/bert-base-NER)")
print("-"*40)
pretrained_model = FurnitureNER(use_trained_model=False)
pretrained_results = pretrained_model.extract_products(text)
for p in pretrained_results[:10]:
    print(f"  • {p}")
print(f"\n  Всего найдено: {len(pretrained_results)}")

print("\n" + "-"*40)
print("✅ ВАША ОБУЧЕННАЯ МОДЕЛЬ")
print("-"*40)
trained_model = FurnitureNER(use_trained_model=True)
trained_results = trained_model.extract_products(text)
for p in trained_results[:10]:
    print(f"  • {p}")
print(f"\n  Всего найдено: {len(trained_results)}")

print("\n" + "="*60)
print("ВЫВОД:")
if trained_results:
    print("✅ Ваша модель работает!")
else:
    print("⚠️ Ваша модель ничего не нашла. Возможно, нужно больше данных для обучения.")
print("="*60)