from bs4 import BeautifulSoup
import pandas as pd
from bs4.element import Comment
import re
import nltk
import numpy as np
class HtmlAnalyzer:

    def __init__(self, email, keywords={}):
        self.soup = BeautifulSoup(email.email_body, 'html.parser')
        self.subject = email.email_subject
        self.keywords = keywords
        self.tags = {}
        self.description = []
        self.body_text = ''
        self.__generate_body_text()
        self.__find_keywords_in_subject()
        self.__find_keywords_in_body()
        # self.info = {}
        # self.__find_info()

    def __add_tag(self, key, tag):
        if key in self.tags:
            if tag not in self.tags[key]:
                self.tags[key].append(tag)              
        else:
            self.tags[key] = []
            self.tags[key].append(tag)


    def __find_keywords_in_subject(self):
        lower_subject = self.subject.lower()
        for key in self.keywords.keys():
            for keyword in self.keywords[key]:
                if keyword.lower() in lower_subject:
                    self.__add_tag(key,keyword)
   
    def __generate_body_text(self):  
        

        raw_text = self.__get_visible_text()
        clean_split_sents = []
        for sent in nltk.sent_tokenize(raw_text):
            words = nltk.word_tokenize(sent)
            cleaned_words = [word for word in words if word.isalpha()]
            clean_split_sents.append(' '.join(cleaned_words))

        self.body_text = clean_split_sents



    def __find_keywords_in_body(self):
        description_text = []
        for line in self.body_text:
            for key in self.keywords.keys():
                for keyword in self.keywords[key]:
                    if keyword.lower() in line.lower():
                        self.__add_tag(key,keyword)
                        sent = line + '. '
                        if sent not in description_text and ' re ' not in sent.lower():
                            description_text.append(line + '. ')
        self.description = ' '.join(description_text)
        



    # def __find_info(self):
    #     tables = self.find_html_tags("table")
    #     lists = self.find_html_tags("ul")
    #     self.list_data = {}
    #     self.table_data = {}
    #     if tables:
    #         self.tables = tables
    #         self.__make_table_dict()
    #     if lists:
    #         self.lists = lists
    #         self.__process_list()

    #     self.__compile_info()

    # def __compile_info(self):
    #     self.info = {}
    #     self.info["text"] = self.raw_text
    #     if self.table_data:
    #         self.info["table_data"] = self.table_data
    #     if self.list_data:
    #         self.info["list_data"] = self.list_data
        

    
    # def __make_table_dict(self):
    #     tables_data = []
    #     for table in self.tables:
    #         has_lists = table.find_all('ul')
    #         if has_lists:
    #             pass
    #         rows = table.find_all("tr")
    #         table_data = []
    #         for row in rows:
    #             row_data = []
    #             entries = row.find_all("td")
    #             for entry in entries:
    #                 if entry.text:
    #                     row_data.append(self.__clean_text(entry.text))
    #             if row_data:
    #                 table_data.append(row_data)
    #         table_data = self.__process_table_data(table_data)
    #         self.table_data = table_data
            
    
    # def __process_table_data(self,table):
    #     table = self.__clean_table(table)
    #     real_table = []
    #     data = {}
    #     for row in table:
    #         if len(row) > 1:
    #             if all(': ' in entry for entry in row):
    #                 for entry in row:
    #                     split_entry = entry.split(': ')
    #                     data[split_entry[0]] = split_entry[1]
    #             if any(': ' in entry for entry in row):
    #                 data[row[0]] = row[1:]
    #             else:
    #                 real_table.append(row)
    #     if real_table:
    #         table_t = np.array(real_table).T.tolist()
    #         for row in table_t:
    #             data[row[0]] = row[1:]
    #     return data

    
    # def __clean_table(self, table):
    #     table = [elem for elem in table if u'\xa0' not in elem]
    #     return table             

    # def __process_list(self):
    #     for l in self.lists:
    #         prev = l.find_previous_sibling()
    #         list_items = l.find_all('li')
    #         list_item_text = []
    #         for item in list_items:
    #             list_item_text.append(item.text)
    #         if prev.text:
    #             if prev.text in self.list_data:
    #                 self.list_data[prev.text].append(list_item_text)
    #             else:
    #                 self.list_data[prev.text] = []
    #                 self.list_data[prev.text].append(list_item_text)

    # def __clean_text(self, text):
    #     special_chars = ['\n', '\t']
    #     unicode_chars = [u'\xa0', u'\u200b']
    #     cleaned_array = [ch for ch in text or ' ' if ch not in special_chars and ch not in unicode_chars]
    #     return ''.join(cleaned_array)
        
        

    def __tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def __get_visible_text(self):
        texts = self.soup.findAll(text=True)
        visible_texts = filter(self.__tag_visible,texts)
        all_text = u" ".join(t.strip() for t in visible_texts)
        return all_text
    
    # def get_tag_children(self, tag):
    #     tags = self.find_html_tags(tag)
    #     tag_dict = {}
    #     for tag in tags:
    #         children_text = []
    #         for child in tag.findChildren():
    #             children_text.append(child.text)
    #         tag_dict[tag.text] = children_text
    #     return tag_dict


    # def find_html_tags(self, tag):
    #     return self.soup.find_all(tag)

    # def get_info(self):
    #     return self.info
        