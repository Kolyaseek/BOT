from natasha import MorphVocab, Doc
from pymorphy2 import MorphAnalyzer

# Инициализация анализаторов
morph = MorphAnalyzer()
morph_vocab = MorphVocab()

def extract_keywords(text: str) -> list:
    doc = Doc(text.lower())
    doc.segment()
    
    keywords = []
    for token in doc.tokens:
        # Нормализация слова
        parsed = morph.parse(token.text)[0]
        lemma = parsed.normal_form
        
        # Отбираем существительные и имена собственные
        if parsed.tag.POS in {'NOUN', 'PROPN'} and len(lemma) > 3:
            keywords.append(lemma)
    
    # Добавляем числа (номера статей)
    keywords += [word for word in text.split() if word.isdigit()]
    
    return list(set(keywords))  # Удаляем дубликаты
