from typing import Union
import re
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
from nltk.stem.snowball import SnowballStemmer


class DocumentProcessor:
    def __init__(self, methods: Union[str, list]):
        try:
            assert type(methods) in [type(None), str, list], "Wrong method attribute"
            if methods is None:
                self.methods = []
            elif isinstance(methods, str):
                self.methods = [methods]
            else:
                self.methods = methods

            self.stemmer = SnowballStemmer("russian") 
            self.stopwords_ru = stopwords.words("russian")
            self.lemmatizer = MorphAnalyzer()

        except AssertionError as err:
            print(err)


    def get_methods(self):
        return self.methods

    def process(self, text):
        for method in self.methods:
            try:
                text = self.processing_methods[method](self, text)
            except KeyError:
                print('No such processing method')
                raise
        return text
    
    def normalize_spaces(self, text):
        assert isinstance(text, str)
        return ' '.join(text.split())
    
    def lowcase_process(self, text):
        assert isinstance(text, str)
        return text.lower()
    
    def special_chars(self, text):
        assert isinstance(text, str)
        return re.sub('[^A-Za-z0-9А-Яа-я ]+', '', text)
    
    def remove_stopwords(self, text):
        preprocessed_tokens = [x for x in text.split() if x not in self.stopwords_ru]
        return ' '.join(preprocessed_tokens)


    def lemmatize_text(self, text):
        preprocessed_tokens = [self.lemmatizer.normal_forms(x)[0] for x in text.split()]  
        return ' '.join(preprocessed_tokens)

    

    
    processing_methods = {
        'normalize_spaces':normalize_spaces,
        'lowcase':lowcase_process,
        'special_chars':special_chars,
        'remove_stopwords':remove_stopwords,
        'lemmatize_text':lemmatize_text
    }
    