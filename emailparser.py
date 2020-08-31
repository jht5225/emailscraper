import re, spacy
import pandas as pd
from bs4 import BeautifulSoup
from emailobj import Email
from textanalyzer import TextAnalyzer
from htmlanalyzer import HtmlAnalyzer

class EmailParser:
    
    def __init__(self, email=None, context=None):
        self.text_info = []
        self.html_info = []
        if context:
            self.context = context
        else:
            self.context = None
        if type(email) is Email:
            self.email = email
            self.__parse_email()
    
    def __parse_email(self):
        self.__parse_header()
        self.__parse_body()

    def __parse_header(self):
        self.__search_context_in_text(self.email.subject)
    
    def __parse_body(self):
        self.body_data = {}
        for text in self.email.get_text_content():
            if text['type'] == 'text':
                self.__parse_text(text['content'])
            if text['type'] == 'html':
                self.__parse_html(text['content'])

    def __parse_text(self, content):
        text_content = {}
        processed_content = self.__parse_intro_exit(content)
        text_analyzer = TextAnalyzer(processed_content)
        text_content['summary'] = text_analyzer.get_summary_sentences()
        if self.context:
            for key in self.context.keys():
                search = text_analyzer.search_for(self.context[key])
                text_content[key] = search
        
        self.text_info.append(text_content)
    
    def __parse_intro_exit(self, content):
        split_content = content.split('\n\n')
        if len(split_content) > 2:
            if ',' in split_content[0]:
                split_content.pop(0)
            split_content.pop()
            split_content.pop()
        return ' '.join(split_content)

    def __parse_html(self,content):
        html = HtmlAnalyzer(content)
        self.html_info.append(html.get_info())
    
    def __search_context_in_text(self, text):
        if self.context:
            results  = {}
            for key in self.context.keys():
                search = [match for match in self.context[key] if match in text]
                results[key] = search
            return results
        else:
            return None

    def __search_context_in_df(self, df):
        if self.context:
            print(df.columns)

    def __find_text_info(self, sent):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(sent)
        for ent in doc:
            print(ent.text, ent.start_char, ent.end_char, ent.label_) 


    def get_text_content(self):
        return self.text_info
    
    def get_html_content(self):
        return self.html_info
