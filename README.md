🪑 Мебельный NER Экстрактор
https://img.shields.io/badge/python-3.11+-blue.svg
https://img.shields.io/badge/license-MIT-green.svg

Извлечение названий мебельных товаров с веб-сайтов с помощью NER модели.

Этот проект реализует полный пайплайн для обучения модели NER (Named Entity Recognition), которая определяет названия мебельных товаров на веб-страницах. Включает сбор данных, обучение модели и веб-интерфейс для демонстрации.

🎯 Возможности
Полный пайплайн обучения NER – сбор данных, разметка, обучение и оценка

Два метода извлечения – CSS-селекторы (структурный) + NER модель (семантический)

Пакетная обработка CSV – извлечение товаров из нескольких URL одновременно

Веб-интерфейс – удобный UI на Gradio для тестирования

Сравнение моделей – сравнение предобученной и вашей обученной модели

Локальное хранение модели – обучил один раз, используй офлайн

📁 Структура проекта
text
furniture-ner-project/
│
├── scripts/                        # Запускаемые скрипты
│   ├── main.py                     # Извлечение из одного URL (консоль)
│   ├── database_builder.py         # Пакетная обработка из CSV
│   ├── web_app.py                  # Веб-интерфейс (Gradio)
│   ├── prepare_training_data.py    # Сбор и разметка данных
│   ├── train_model.py              # Обучение NER модели
│   └── compare_models.py           # Сравнение моделей
│
├── src/                            # Переиспользуемые модули
│   ├── crawler.py                  # Утилиты для веб-парсинга
│   ├── model_predict.py            # Обёртка для инференса модели
│   └── trainer.py                  # Утилиты для обучения
│
├── models/                         # Сохранённые модели
│   └── furniture_ner/              # Ваша обученная модель (веса не включены)
│
├── data/                           # Данные
│   ├── databases/
│   │   ├── URL_list.csv            # URL для пакетной обработки
│   │   └── products_database.json  # Результаты парсинга
│   └── training/
│       └── training_data.json      # Размеченные примеры для обучения
│
├── requirements.txt                # Зависимости
├── setup.py                        # Установка проекта как пакета
├── run.bat / run.sh                # Скрипты быстрого запуска
└── README.md                       # Документация
🚀 Быстрый старт
Требования
Python 3.11 или выше

pip (менеджер пакетов)

Установка
bash
# 1. Клонируйте репозиторий
git clone https://github.com/antonovnikitaa573-ui/furniture-ner-project.git
cd furniture-ner-project

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте его
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Установите зависимости
pip install -r requirements.txt
Запуск веб-интерфейса
bash
python scripts/web_app.py
Затем откройте http://127.0.0.1:7860 в браузере.

📖 Руководство по использованию
1. Извлечение из одного URL (консоль)
bash
python scripts/main.py "https://www.ikea.com/us/en/p/ektorp-sofa-90212345/"
2. Пакетная обработка из CSV
Подготовьте файл data/databases/URL_list.csv с колонкой url:

csv
url
https://www.ikea.com/us/en/p/ektorp-sofa-90212345/
https://www.westelm.com/furniture/sofas/
Затем запустите:

bash
python scripts/database_builder.py
Результаты сохранятся в data/databases/products_database.json.

3. Обучение своей модели
Шаг 1: Сбор данных для обучения

bash
python scripts/prepare_training_data.py
Это создаст файл data/training/training_data.json с кандидатами в названия товаров.

Шаг 2: Ручная разметка

Отредактируйте training_data.json – убедитесь, что поля product_name заполнены правильно.

Шаг 3: Обучение модели

bash
python scripts/train_model.py
Обученная модель сохранится в models/furniture_ner/.

Шаг 4: Использование вашей модели

В файле scripts/web_app.py измените:

python
USE_TRAINED_MODEL = True   # Использовать вашу модель
USE_TRAINED_MODEL = False  # Использовать готовую модель
4. Сравнение моделей
bash
python scripts/compare_models.py
Показывает результаты предобученной и вашей обученной модели рядом.

🧠 Как это работает
Архитектура
text
User URL → Загрузка HTML → Извлечение текста → NER модель → Названия товаров
                                      ↑
                           CSS-селекторы (запасной метод)
NER модель
Базовая архитектура: distilbert-base-uncased

Метки: B-PRODUCT (начало), I-PRODUCT (внутри), O (вне)

Данные для обучения: ~100 страниц с ручной разметкой

Запасной вариант: dslim/bert-base-NER (если нет обученной модели)

Методы извлечения
Метод	Скорость	Точность	Применение
CSS-селекторы	⚡ Быстро	🟡 Средняя	Структурированные страницы товаров
NER модель	🐢 Медленнее	🟢 Высокая	Неструктурированный контент
Пример вывода
text
🛋️ РЕЗУЛЬТАТЫ
========================================
URL: https://www.ikea.com/us/en/p/ektorp-sofa-90212345/

📌 CSS-селекторы:
  • EKTORP Sofa
  • Информация о товаре

🧠 NER модель:
  • EKTORP
  • Sofa
  • Чехол
  • Каркас

✅ Всего найдено товаров: 4
========================================
🛠️ Настройка
Переключение между моделями
Отредактируйте scripts/web_app.py:

python
USE_TRAINED_MODEL = True   # Ваша обученная модель
USE_TRAINED_MODEL = False  # Готовая модель
Пользовательские CSS-селекторы
Измените функцию extract_product_candidates() в src/crawler.py:

python
selectors = [
    'h1',
    '.product-title',
    '.ваш-пользовательский-класс',  # Добавьте свой
]
📦 Зависимости
torch – фреймворк для глубокого обучения

transformers – модели от Hugging Face

gradio – веб-интерфейс

beautifulsoup4 – парсинг HTML

requests – HTTP-запросы

pandas – работа с CSV

tqdm – прогресс-бары

Полный список см. в requirements.txt.

🤝 Вклад в проект
Форкните репозиторий

Создайте ветку для функции (git checkout -b feature/amazing)

Зафиксируйте изменения (git commit -m 'Add amazing feature')

Отправьте в ветку (git push origin feature/amazing)

Откройте Pull Request

📧 Контакты
По вопросам и замечаниям, пожалуйста, создайте issue на GitHub.

⭐ Поддержите проект
Если этот проект помог вам, поставьте звезду на GitHub!

