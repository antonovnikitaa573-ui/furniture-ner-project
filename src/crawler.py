import sys
from pathlib import Path

# Добавляем локальные библиотеки, если они есть
LIBS_PATH = Path(__file__).parent.parent / "libs"
if LIBS_PATH.exists():
    sys.path.insert(0, str(LIBS_PATH))

import requests
from bs4 import BeautifulSoup
import re
import time
import json
import csv
from typing import Dict, List, Optional, Tuple
import pandas as pd

def load_urls_from_csv(csv_path: Path) -> List[str]:

    urls = []
    
    try:
        df = pd.read_csv(csv_path)

        possible_columns = ['url', 'URL', 'link', 'Link', 'product_url', 'product_link']
        url_column = None
        
        for col in possible_columns:
            if col in df.columns:
                url_column = col
                break
        
        if url_column is None:
            # Берём первую колонку
            url_column = df.columns[0]
        
        urls = df[url_column].dropna().tolist()
        
    except Exception as e:
        print(f"Pandas не сработал, пробуем стандартный csv: {e}")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if row and row[0].startswith('http'):
                    urls.append(row[0])
    
    urls = [url.strip() for url in urls if url and str(url).startswith('http')]
    return urls

def fetch_page(url: str, use_selenium: bool = False) -> Optional[str]:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        if use_selenium:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            driver.get(url)
            time.sleep(2)
            html = driver.page_source
            driver.quit()
            return html
        else:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return None

def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text[:3000]  # Ограничиваем для NER

def extract_product_candidates(html: str) -> List[str]:

    soup = BeautifulSoup(html, 'html.parser')
    candidates = []

    selectors = [
        'h1', 
        '.product-title', 
        '.product-name', 
        '.product__title', 
        '[data-testid="product-title"]',
        '.product-card__title', 
        '.item-title',
        '.product-details-title',
        '.product-name__item',
        'h2.product-title',
        '.product-info__name'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        for el in elements:
            text = el.get_text(strip=True)
            if text and 3 < len(text) < 200 and not re.match(r'^\d+[\d\.,]*$', text):
                text = re.sub(r'\s+', ' ', text).strip()
                candidates.append(text)
    
    if not candidates and soup.title:
        title = soup.title.get_text(strip=True)
        title = re.sub(r'\|.*$', '', title)
        title = re.sub(r'–.*$', '', title)
        candidates.append(title.strip())
    
    return list(dict.fromkeys(candidates))

def save_html(url: str, html: str, data_dir: Path) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    # Создаём безопасное имя файла
    filename = re.sub(r'[^\w\-_]', '_', url)[:80] + '.html'
    filepath = data_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath

def save_database(database: List[Dict], output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    print(f"💾 База сохранена: {output_path}")

def load_database(input_path: Path) -> List[Dict]:
    if input_path.exists():
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []