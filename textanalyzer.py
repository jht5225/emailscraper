import nltk, re, spacy
from operator import itemgetter
from textblob import TextBlob

class TextAnalyzer:
    def __init__(self, text):
        self.text = text
        self.__process_text()
        self.nlp = spacy.load("en_core_web_sm")
        self.__preprocess()
    

    def __process_text(self):
        self.__make_sentences()
        self.__tag_and_chunk_sentences()


    def __make_sentences(self):
        self.sentences = []
        for line in nltk.sent_tokenize(self.text):
            self.sentences.append(self.__process_line(line))
    
    def __tag_and_chunk_sentences(self):
        self.sentence_tags = []
       
        for sentence in self.sentences:
            blob = TextBlob(sentence)
            sentence_tags = blob.tags
            self.sentence_tags.append(sentence_tags)
        print(self.sentence_tags)


    def __process_line(self,line):
        special_chars = ['\n', '\t', u'\xa0', u'\u200b']
        list_without_special_chars = [c for c in line if c not in special_chars]
        list_to_line = ''.join(list_without_special_chars)
        stripped_line = list_to_line.strip()
        lower_case_line = stripped_line.lower()
        return lower_case_line

    
    def get_summary_sentences(self):
        self.__score_sents()
        if len(self.scores) > 2:
            tops = self.__get_dict_max(self.scores)
        else:
            tops = self.scores
        sents = tops.keys()

        return ' '.join(sents)

    def get_summary_words(self):
        if len(self.word_freq) > 2:
            tops = self.__get_dict_max(self.word_freq)
        else:
            tops = self.word_freq
        return tops

    def search_for(self, search):
        results = []
        for q in search:
            if q.lower() in self.text.lower():
                results.append(q)
        return results

    def __get_dict_max(self, scores, N=3):
        maxes = dict(sorted(scores.items(), key=itemgetter(1), reverse=True )[:N])
        return maxes

    def __preprocess(self):
        self.__textsplit()
        self.__format_text()
        self.__count_word_frequencies()
        self.__weight_frequencies()

    def __format_text(self): 
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', self.text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        self.text = formatted_article_text
   
    def __textsplit(self):
        self.sentences = []
        sentences = nltk.sent_tokenize(self.text)
        for sent in sentences:
            split_lines = sent.split('\n')
            for line in split_lines:
                self.sentences.append(line)

    def __count_word_frequencies(self):
        stopwords = nltk.corpus.stopwords.words('english')
        self.word_freq = {}
        for word in nltk.word_tokenize(self.text):
            if word not in stopwords:
                if word not in self.word_freq.keys():
                    self.word_freq[word] = 1
                else:
                    self.word_freq[word] += 1

    def __weight_frequencies(self):
        max_freq = max(self.word_freq.values())
        
        for word in self.word_freq.keys():
            self.word_freq[word] = (self.word_freq[word]/max_freq)
    
    def __score_sents(self):
        scores = {}
        for sent in self.sentences:
            for word in nltk.word_tokenize(sent.lower()):
                if word in self.word_freq.keys():
                    if sent not in scores.keys():
                        scores[sent] = self.word_freq[word]
                    else:
                        scores[sent] += self.word_freq[word]
        for sent in scores.keys():
            if scores[sent] == 1.0:
                scores[sent] = 0 

        self.scores = scores

