import spacy
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)

class NLPProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.spacy_nlp = spacy.load("ru_core_news_sm")

    def process_text(self, text):
        # Обработка с Natasha
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)
        
        # Извлечение юридических сущностей
        legal_entities = []
        for span in doc.spans:
            if span.type in ('ORG', 'LAW'):
                span.normalize(self.morph_vocab)
                legal_entities.append(span.normal)
        
        # Обработка с spaCy для дополнительного анализа
        spacy_doc = self.spacy_nlp(text)
        for ent in spacy_doc.ents:
            if ent.label_ in ('LAW', 'ORG', 'LOC') and ent.text not in legal_entities:
                legal_entities.append(ent.text)
        
        return list(set(legal_entities))
