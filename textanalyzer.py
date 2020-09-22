import nltk, re, spacy
from operator import itemgetter
from textblob import TextBlob

class TextAnalyzer:
    def __init__(self, text, gazetteer=None):
        self.text = text
        self.paragraphs = []
        self.sentences = []
        self.tokens = []
        self.__preprocess()
        self.key_sentences = {}
        if gazetteer:
            self.gazetteer = gazetteer
            self.__match_sents()
    
    def __preprocess(self): 
        self.__format_text()
        self.__split_lines()
    
    def __format_text(self):
        self.clean_text = (''.join(ch for ch in self.text if (ch.isalnum() or ch in [',', '\n', '.', '\'', '\"', ' ', ':']))).lower()


    def __split_lines(self):
        for paragraph in self.clean_text.split('\n'):
            self.paragraphs.append(paragraph)
            for line in paragraph.split('. '):
                if line != '':
                    self.sentences.append(line)
        
    def __match_sents(self):
        for keyword in self.gazetteer.keys():
            for search_val in self.gazetteer[keyword]:
                self.key_sentences[search_val] = [sent for sent in self.sentences if re.search(search_val, sent)]
    
    def get_key_sentences(self):
        keys = []
        if self.key_sentences:
            for keyword in self.key_sentences.keys():
                if self.key_sentences[keyword]:
                    keys.append({keyword: self.key_sentences[keyword]})
        else:
            keys = self.sentences
        
        return keys


