import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from transformers import pipeline

class FurnitureNER:
    def __init__(self, use_trained_model: bool = True):  #!!!!!

        self.trained_model_path = PROJECT_ROOT / "models" / "furniture_ner"
        
        if use_trained_model and self.trained_model_path.exists():
            print(f"✅ Используем ВАШУ обученную модель из: {self.trained_model_path}")
            self.ner_pipeline = pipeline(
                "token-classification",
                model=str(self.trained_model_path),
                aggregation_strategy="simple"
            )
            self.model_type = "trained"
        else:
            if use_trained_model and not self.trained_model_path.exists():
                print(f"⚠️ Ваша модель не найдена в {self.trained_model_path}")
                print("   Используем готовую модель dslim/bert-base-NER")
            else:
                print("🔄 Используем готовую модель dslim/bert-base-NER")
            
            self.ner_pipeline = pipeline(
                "token-classification",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple"
            )
            self.model_type = "pretrained"
    
    def extract_products(self, text: str) -> list:
        if not text or not self.ner_pipeline:
            return []
        
        results = self.ner_pipeline(text[:3000])
        
        products = set()
        for entity in results:

            if entity['entity_group'] in ['LABEL_1', 'PRODUCT', 'ORG', 'MISC']:
                product = entity['word'].strip('.,;!?\'"')
                if len(product) > 2:
                    products.add(product)
        
        return sorted(list(products))
    
    def get_model_info(self) -> str:
        if self.model_type == "trained":
            return f"Обученная модель (путь: {self.trained_model_path})"
        else:
            return "Готовая модель dslim/bert-base-NER"