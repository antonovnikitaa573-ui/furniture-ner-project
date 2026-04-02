import json
from pathlib import Path
from typing import List, Dict, Tuple
import random

from crawler import extract_text_from_html
from transformers import (
    AutoTokenizer, 
    AutoModelForTokenClassification, 
    TrainingArguments, 
    Trainer,
    DataCollatorForTokenClassification
)
from datasets import Dataset
import torch

TRAINING_URLS = [
    "https://www.ikea.com/us/en/p/ektorp-sofa-90212345/",
    "https://www.ikea.com/us/en/p/malm-bed-frame-12345678/",
    "https://www.westelm.com/products/coastlinen-sofa-h1987/",
    "https://www.wayfair.com/furniture/pdp/serta-mattress-sert001.html",
]

def create_training_data(urls: List[str], output_path: Path) -> List[Dict]:

    from src.crawler import fetch_page, extract_product_candidates
    
    training_examples = []
    
    for url in urls[:20]:  
        html = fetch_page(url)
        if not html:
            continue
            
        candidates = extract_product_candidates(html)

        for candidate in candidates[:3]:  
            training_examples.append({
                "url": url,
                "product_name": candidate,
                "context": extract_text_from_html(html)[:500]
            })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_examples, f, indent=2, ensure_ascii=False)
    
    return training_examples

def prepare_dataset_for_ner(training_examples: List[Dict], model_name: str = "distilbert-base-uncased"):

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    label2id = {"O": 0, "B-PRODUCT": 1, "I-PRODUCT": 2}
    id2label = {v: k for k, v in label2id.items()}

    def label_text(text: str, product_name: str):

        words = text.split()
        labels = ["O"] * len(words)
        
        product_words = product_name.lower().split()
        for i in range(len(words) - len(product_words) + 1):
            if [w.lower() for w in words[i:i+len(product_words)]] == product_words:
                labels[i] = "B-PRODUCT"
                for j in range(1, len(product_words)):
                    labels[i+j] = "I-PRODUCT"
                break
        
        return {"words": words, "labels": labels}

    all_encodings = []
    for ex in training_examples:
        labeled = label_text(ex["context"], ex["product_name"])
        encoding = tokenizer(
            labeled["words"],
            is_split_into_words=True,
            truncation=True,
            max_length=128,
            padding=False
        )

        labels = []
        word_ids = encoding.word_ids()
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                labels.append(-100)
            elif word_idx != previous_word_idx:
                labels.append(label2id[labeled["labels"][word_idx]])
            else:
                labels.append(label2id[labeled["labels"][word_idx]] if labeled["labels"][word_idx] != "O" else -100)
            previous_word_idx = word_idx
        
        encoding["labels"] = labels
        all_encodings.append(encoding)
    
    return Dataset.from_list(all_encodings), tokenizer, id2label, label2id

def train_model(training_data_path: Path, model_save_path: Path):

    with open(training_data_path, 'r', encoding='utf-8') as f:
        training_examples = json.load(f)
    
    dataset, tokenizer, id2label, label2id = prepare_dataset_for_ner(training_examples)
    
    model = AutoModelForTokenClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id
    )
    
    training_args = TrainingArguments(
        output_dir=str(model_save_path),
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        num_train_epochs=3,
        save_strategy="epoch",
        push_to_hub=False,
    )
    
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    
    trainer.train()
    trainer.save_model(str(model_save_path))
    tokenizer.save_pretrained(str(model_save_path))
    
    print(f"✅ Модель сохранена в {model_save_path}")
    return model, tokenizer