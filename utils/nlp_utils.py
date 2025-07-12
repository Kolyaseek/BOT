from natasha import Segmenter, MorphVocab, Doc
from pymorphy2 import MorphAnalyzer

# Инициализация компонентов Natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
morph = MorphAnalyzer()

def extract_keywords(text: str) -> list:
    """Извлекает ключевые слова из текста"""
    try:
        doc = Doc(text)
        doc.segment(segmenter)  # Добавляем segmenter
        
        keywords = []
        for token in doc.tokens:
            parsed = morph.parse(token.text)[0]
            if parsed.tag.POS in {'NOUN', 'PROPN'} and len(parsed.normal_form) > 3:
                keywords.append(parsed.normal_form)
        
        # Добавляем числа (номера статей)
        keywords += [word for word in text.split() if word.isdigit()]
        
        return list(set(keywords))
    
    except Exception as e:
        print(f"⚠️ NLP Error: {e}")
        return text.split()[:5]  # Возвращаем первые 5 слов как fallback
