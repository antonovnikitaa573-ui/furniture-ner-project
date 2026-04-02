# 🪑 Furniture NER Extractor

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**NER model for extracting furniture product names from e-commerce websites.**

This project implements a complete pipeline for training a Named Entity Recognition (NER) model that identifies furniture product names in web pages. It includes data collection, model training, and a web interface for demonstration.

---

## 🎯 Features

- **Complete NER training pipeline** – collect data, annotate, train, and evaluate
- **Two extraction methods** – CSS selectors (structural) + NER model (semantic)
- **CSV batch processing** – extract products from multiple URLs at once
- **Web interface** – Gradio-based UI for easy testing
- **Model comparison** – compare pretrained vs your trained model
- **Local model storage** – train once, use offline

---

## 📁 Project Structure

furniture-ner-project/
├── scripts/
│ ├── main.py # Single URL extraction (console)
│ ├── database_builder.py # Batch processing from CSV
│ ├── web_app.py # Web interface (Gradio)
│ ├── prepare_training_data.py # Collect and annotate data
│ ├── train_model.py # Train NER model
│ └── compare_models.py # Compare model performance
├── src/
│ ├── crawler.py # Web scraping utilities
│ ├── model_predict.py # Model inference wrapper
│ └── trainer.py # Training utilities
├── models/
│ └── furniture_ner/ # Your trained model (weights excluded)
├── data/
│ ├── databases/
│ │ └── URL_list.csv # Input URLs for batch processing
│ └── training/
│ └── training_data.json # Annotated training examples
├── requirements.txt
├── setup.py
├── run.bat / run.sh # Quick launch scripts
└── README.md

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/antonovnikitaa573-ui/furniture-ner-project.git
cd furniture-ner-project

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

Run the Web Interface
bash
python scripts/web_app.py
Then open http://127.0.0.1:7860 in your browser.

📖 Usage Guide
1. Single URL Extraction (Console)
bash
python scripts/main.py "https://www.ikea.com/us/en/p/ektorp-sofa-90212345/"
2. Batch Processing from CSV
Prepare data/databases/URL_list.csv with a column named url:

csv
url
https://www.ikea.com/us/en/p/ektorp-sofa-90212345/
https://www.westelm.com/furniture/sofas/
Then run:

bash
python scripts/database_builder.py
Results are saved to data/databases/products_database.json.

3. Train Your Own Model
Step 1: Collect training data

bash
python scripts/prepare_training_data.py
This creates data/training/training_data.json with candidate product names.

Step 2: Annotate manually

Edit training_data.json – verify that product_name fields are correct.

Step 3: Train the model

bash
python scripts/train_model.py
The trained model is saved to models/furniture_ner/.

Step 4: Use your trained model

In scripts/web_app.py, change:

python
USE_TRAINED_MODEL = True   # Use your trained model
USE_TRAINED_MODEL = False  # Use pretrained fallback
4. Compare Models
bash
python scripts/compare_models.py
Shows side-by-side results from pretrained vs your trained model.

🧠 How It Works
Architecture
text
User URL → Fetch HTML → Extract Text → NER Model → Product Names
                                      ↑
                           CSS Selectors (fallback)
NER Model
Base architecture: distilbert-base-uncased

Labels: B-PRODUCT (beginning), I-PRODUCT (inside), O (outside)

Training data: ~100 manually annotated furniture product pages

Fallback: dslim/bert-base-NER if no trained model exists

Extraction Methods
Method	Speed	Accuracy	Use Case
CSS Selectors	⚡ Fast	🟡 Medium	Structured product pages
NER Model	🐢 Slower	🟢 High	Unstructured content
📊 Example Output
text
🛋️ RESULTS
========================================
URL: https://www.ikea.com/us/en/p/ektorp-sofa-90212345/

📌 CSS Selectors:
  • EKTORP Sofa
  • Product details

🧠 NER Model:
  • EKTORP
  • Sofa
  • Cover
  • Frame

✅ Total products found: 4
========================================
🛠️ Configuration
Switching Models
Edit scripts/web_app.py:

python
USE_TRAINED_MODEL = True   # Trained model
USE_TRAINED_MODEL = False  # Pretrained fallback
Custom CSS Selectors
Modify src/crawler.py – extract_product_candidates() function:

python
selectors = [
    'h1',
    '.product-title',
    '.your-custom-class',  
]
📦 Dependencies
torch – Deep learning framework

transformers – Hugging Face models

gradio – Web interface

beautifulsoup4 – HTML parsing

requests – HTTP requests

pandas – CSV handling

tqdm – Progress bars

See requirements.txt for full list.

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing)

Open a Pull Request

📝 License
This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgments
Hugging Face for transformers library

dslim/bert-base-NER for pretrained model

Gradio for web interface

📧 Contact
For questions or feedback, please open an issue on GitHub.

⭐ Show Your Support
If this project helped you, please give it a star on GitHub!

Copyright (c) 2026 Nikitos3x

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
