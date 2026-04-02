import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import gradio as gr
from src.model_predict import FurnitureNER
from src.crawler import fetch_page, extract_product_candidates

USE_TRAINED_MODEL = True   # <--- True-обученная мной False-готовая


print(f"🔄 Загрузка модели... (USE_TRAINED_MODEL={USE_TRAINED_MODEL})")
ner_model = FurnitureNER(use_trained_model=USE_TRAINED_MODEL)
print(f"📌 Используется: {ner_model.get_model_info()}")

def extract_from_url(url):
    if not url:
        return "❌ Пожалуйста, введите URL"
    
    if not url.startswith('http'):
        return "❌ URL должен начинаться с http:// или https://"
    
    html = fetch_page(url)
    if not html:
        return f"❌ Не удалось загрузить страницу: {url}"

    css_products = extract_product_candidates(html)

    text = extract_text_from_html(html) 
    ner_products = ner_model.extract_products(text)
    
    result = "# 🛋️ РЕЗУЛЬТАТЫ АНАЛИЗА\n\n"
    result += f"**URL:** `{url}`\n"
    result += f"**Используемая модель:** {ner_model.get_model_info()}\n\n"
    
    result += "## 📌 CSS-селекторы\n\n"
    if css_products:
        for p in css_products[:10]:
            result += f"• {p}\n"
    else:
        result += "*Товары не найдены*\n"
    
    result += f"\n## 🧠 NER модель\n\n"
    if ner_products:
        for p in ner_products[:10]:
            result += f"• {p}\n"
    else:
        result += "*Товары не найдены*\n"
    
    return result

from src.crawler import extract_text_from_html

with gr.Blocks(title="Мебельный экстрактор товаров") as demo:
    gr.Markdown("# 🪑 Мебельный экстрактор товаров")
    gr.Markdown("Введите URL страницы интернет-магазина мебели.")
    
    with gr.Row():
        with gr.Column(scale=4):
            url_input = gr.Textbox(
                label="🔗 URL страницы",
                placeholder="https://www.ikea.com/us/en/p/ektorp-sofa-90212345/",
                lines=2
            )
        with gr.Column(scale=1):
            submit_btn = gr.Button("🔍 Найти товары", variant="primary")
    
    output = gr.Markdown(label="📦 Результаты")
    submit_btn.click(fn=extract_from_url, inputs=url_input, outputs=output)

if __name__ == "__main__":
    demo.launch()