import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
from transformers import (
    AutoTokenizer, 
    AutoModelForTokenClassification, 
    TrainingArguments, 
    Trainer,
    DataCollatorForTokenClassification
)
from datasets import Dataset
import torch

def train():

    data_path = PROJECT_ROOT / "data" / "training" / "training_data.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        training_data = json.load(f)
    
    if len(training_data) < 5:
        print("❌ Мало данных для обучения (нужно минимум 5-10 примеров)")
        return
    
    print(f"📊 Загружено {len(training_data)} примеров")

    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    label2id = {"O": 0, "B-PRODUCT": 1, "I-PRODUCT": 2}
    id2label = {v: k for k, v in label2id.items()}

    
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id
    )

    model_save_path = PROJECT_ROOT / "models" / "furniture_ner"
    model_save_path.mkdir(parents=True, exist_ok=True)
    
    model.save_pretrained(str(model_save_path))
    tokenizer.save_pretrained(str(model_save_path))
    
    print(f"✅ Модель сохранена в {model_save_path}")

if __name__ == "__main__":
    train()