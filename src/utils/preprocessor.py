from typing import Union

# class WordPreprocessor:
#     """
#     Class of word preprocessing instantce that change given world depending on the given methods
#     """
#     def __init__(self, method: Union[str, list]):
#         try:
#             assert type(method) in [type(None), str, list], "Wrong method attribute"
#             if method is None:
#                 self.methods = []
#             elif isinstance(method, str):
#                 self.methods = [method]
#             else:
#                 self.methods = method
#         except AssertionError as err:
#             print(err)

#     def process(self, word):
#         for method in self.methods:
#             try:
#                 word = self.processing_methods[method](word)
#             except KeyError:
#                 print('No such processing method')
#                 raise
#         return word

#     @staticmethod
#     def lowcase_process(word):
#         assert isinstance(word, str)
#         return word.lower()
    
#     processing_methods = {
#         'lowcase':lowcase_process,
#     }

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
    
    processing_methods = {
        'normalize_spaces':normalize_spaces,
        'lowcase':lowcase_process,
    }
    