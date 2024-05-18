from collections import defaultdict
import pickle    
import hashlib
import os

import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils import bm_search, read_whole_content



class InvertedIndex:
    def __init__(self, documents: list[str], load_path=None):
        self.index = defaultdict(set)
        self.documents = documents

        if load_path is None:
            self.build_index()
        else:
            self.load_index(load_path)

    def load_index(self, path, method='pickle'):
        '''
        Load stored inverted index
        '''
        print("Loading index from storage")
        AVAILABLE_METHODS = ['pickle']
        assert method in AVAILABLE_METHODS, 'Unknown load method'

        if method == 'pickle':
            with open(path, 'rb') as f:
                self.index = pickle.load(f)

    
    def save_index(self, save_path, method='pickle'):
        AVAILABLE_METHODS = ['pickle']
        assert method in AVAILABLE_METHODS, 'Unknown load method'

        if method == 'pickle':
            with open(save_path, 'wb') as f:
                pickle.dump(self.index, f)


    def build_index(self):
        print("Building index from scratch")
        for index, document in enumerate(self.documents):
            splitted_words = document.split()
            for word in splitted_words:
                self.index[word].add(index)
        
        
    def _get_documents_containing_words_of_expression(self, expression: str) -> list:
        words_to_search = expression.split()
        documents_indexes = []

        for word in words_to_search:
            documents_indexes.append(self.index[word])

        containing_documents = documents_indexes[0]
        for curr_indexes in documents_indexes[1:]:
            containing_documents.intersection(curr_indexes)

        return list(containing_documents)
    
    
    def search(self, expression: str) -> list[int, str]:
        """
        Return indices and documents where expression occurs
        """
        indexes_to_search = self._get_documents_containing_words_of_expression(expression)
        right_documents = list()
        docs_to_search = [self.documents[doc] for doc in indexes_to_search]
        for index, document in enumerate(docs_to_search):
            if bm_search(document, expression):
                right_documents.append((indexes_to_search[index], document))

        return right_documents
    

def _get_index_path(database_path: str) -> str:
        """
        All indexes is stored in ./data/index directory, name of the file generates from db_path through md5 hash
        """
        db_path_hash = f'{hashlib.md5(database_path.encode()).hexdigest()}.pickle'
        db_parent_path = os.path.dirname(os.path.dirname(database_path))
        return os.path.join(db_parent_path, 'index', db_path_hash)

def index_initializer(database_path):
    save_index = True
    hashed_index_path = _get_index_path(database_path)
    load_path = None
    if os.path.exists(hashed_index_path):
        save_index = False
        load_path = hashed_index_path

    documents = read_whole_content(database_path)
    initialized_index = InvertedIndex(documents, load_path)

    if save_index:
        initialized_index.save_index(hashed_index_path)

    return initialized_index





        


    

