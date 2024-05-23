from collections import defaultdict
import pickle    
import hashlib
import os
import numpy as np
from functools import partial
from typing import Union
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils import bm_search, read_whole_content, DocumentProcessor, EncodedInvertedIndex



class InvertedIndex:
    def __init__(self, documents: list[str], preprocessor, load_path=None, encoding=False):
        self.index = defaultdict(partial(np.ndarray, 0, dtype='int32'))

        self.documents = documents
        self.preprocessor = preprocessor
        self.encoding = encoding

        if load_path is None:
            self.build_index()
            if not encoding is None:
                print('Encoding inverted index')
                self.index = EncodedInvertedIndex(self.index, encoding_method=self.encoding)
        else:
            self.load_index(load_path)

        

    def load_index(self, path):
        '''
        Load stored inverted index
        '''
        print("Loading index from storage")
        
        if not self.encoding is None:
            self.index = EncodedInvertedIndex(self.index, encoding_method=self.encoding)
            with open(path, 'rb') as f:
                loaded_index = pickle.load(f)
            self.index.load_encoded_dict(loaded_index)
        else:
            with open(path, 'rb') as f:
                self.index = pickle.load(f)

    
    def save_index(self, save_path):

        print("Saving index")

        if not self.encoding is None:
            with open(save_path, 'wb') as f:
                pickle.dump(self.index.get_encoded_dict(), f)
        else:
            with open(save_path, 'wb') as f:
                pickle.dump(self.index, f)


    def build_index(self):
        print("Building index from scratch")
        for index, document in enumerate(self.documents):
            document = self.preprocessor.process(document)
            splitted_words = document.split()
            for word in splitted_words:
                self.index[word] = np.append(self.index[word], index+1)
        for word in self.index:
            self.index[word] = np.unique(self.index[word])
        
    def _get_documents_containing_words_of_expression(self, expression: str) -> list:
        words_to_search = expression.split()
        documents_indexes = []

        for word in words_to_search:
            documents_indexes.append(self.index[word])


        containing_documents = documents_indexes[0]
        for curr_indexes in documents_indexes[1:]:
            containing_documents = np.intersect1d(containing_documents, curr_indexes)
        return list(containing_documents-1)
    
    
    def search(self, expression: str) -> list[int, str]:
        """
        Return indices and documents where expression occurs
        """
        indexes_to_search = self._get_documents_containing_words_of_expression(expression)
        right_documents = list()
        docs_to_search = [self.documents[doc] for doc in indexes_to_search]
        for index, document in enumerate(docs_to_search):
            document = self.preprocessor.process(document)
            if bm_search(document, expression):
                right_documents.append((indexes_to_search[index], self.documents[indexes_to_search[index]]))

        return right_documents
    

def _get_index_path(database_path: str, preprocessor: list, encoded: Union[bool, str]=False) -> str:
        """
        All indexes is stored in ./data/index directory, name of the file generates from db_path through md5 hash
        """
        db_path_hash = f'{hashlib.md5((database_path+str(encoded)+'-'.join(preprocessor)).encode()).hexdigest()}.pickle'
        db_parent_path = os.path.dirname(os.path.dirname(database_path))
        return os.path.join(db_parent_path, 'index', db_path_hash)

def index_initializer(database_path, preprocessor, encoding):
    save_index = True
    methods = preprocessor.get_methods()
    hashed_index_path = _get_index_path(database_path, methods, encoding)
    load_path = None
    if os.path.exists(hashed_index_path):
        save_index = False
        load_path = hashed_index_path

    documents = read_whole_content(database_path)
    initialized_index = InvertedIndex(documents, preprocessor, load_path, encoding)

    if save_index:
        initialized_index.save_index(hashed_index_path)

        

    return initialized_index







        


    

