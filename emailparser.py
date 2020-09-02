import re, spacy
import pandas as pd
from bs4 import BeautifulSoup
from emailobj import Email
from textanalyzer import TextAnalyzer
from htmlanalyzer import HtmlAnalyzer

class EmailParser:
    
    def __init__(self, email=None, context=None):
        self.text_info = []
        self.overview = {}
        self.overview['summary'] = []
        self.overview['keywords'] = []
        self.overview['intro'] = []
        self.overview['exit'] = []
        self.overview['data'] = {}
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
        self.overview['subject'] = self.email.subject
        self.overview['from'] = self.email.email_from
    
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
        self.overview['summary'].append(text_analyzer.get_summary_sentences())
        if self.context:
            for key in self.context.keys():
                search = text_analyzer.search_for(self.context[key])
                self.overview['keywords'].append({key : search})
    
    def __parse_intro_exit(self, content):
        split_content = content.split('\n\n')
        if len(split_content) > 2:
            if ',' in split_content[0]:
                self.overview['intro'].append(split_content.pop(0))
            split_content.pop()
            self.overview['exit'].append(split_content.pop())
        return ' '.join(split_content)

    def __parse_html(self,content):
        html = HtmlAnalyzer(content)
        info = html.get_info()
        if 'text' in info:
            self.__parse_text(info['text'])
        if 'table_data' in info:
            self.overview['data'].update(info['table_data'])
        if 'list_data' in info:
            self.overview['data'].update(info['list_data'])

    def __get(self, get):
        if get in self.overview:
            return self.overview[get]        

    def email_info(self):
        return self.overview

    def get_email_data(self):
        return self.__get('data')

    def get_email_summary(self):
        return self.__get('summary')
    
    def get_email_keyword(self):
        return self.__get('keywords')