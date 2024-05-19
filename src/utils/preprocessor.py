from typing import Union
import re

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
        except AssertionError as err:
            print(err)


    def process(self, text):
        for method in self.methods:
            try:
                text = self.processing_methods[method](text)
            except KeyError:
                print('No such processing method')
                raise
        return text
    
    @staticmethod
    def normalize_spaces(text):
        assert isinstance(text, str)
        return ' '.join(text.split())
    
    @staticmethod
    def lowcase_process(text):
        assert isinstance(text, str)
        return text.lower()
    
    @staticmethod
    def special_chars(text):
        assert isinstance(text, str)
        return re.sub('[^A-Za-z0-9А-Яа-я ]+', '', text)

    
    processing_methods = {
        'normalize_spaces':normalize_spaces,
        'lowcase':lowcase_process,
        'special_chars':special_chars
    }
    