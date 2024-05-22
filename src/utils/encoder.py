import numpy as np
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from tqdm import tqdm

class AbstractEncoder(ABC):

    @staticmethod
    @abstractmethod
    def encode(arr: np.array) -> np.array:
        ...

    @staticmethod
    @abstractmethod
    def decode(arr: np.array) -> np.array:
        ...



class EliasGammaEncoder(AbstractEncoder):
    @staticmethod
    def encode(a: np.array):
        a = a.view(f'u{a.itemsize}')
        l = np.log2(a).astype('u1')
        L = ((l<<1)+1).cumsum()
        out = np.zeros(L[-1],'u1')
        for i in range(l.max()+1):
            out[L-i-1] += (a>>i)&1
        return np.packbits(out)

    @staticmethod
    def decode(b: np.array):
        n = b.size
        b = np.unpackbits(b,count=n).view(bool)
        s = b.nonzero()[0]
        s = (s<<1).repeat(np.diff(s,prepend=-1))
        s -= np.arange(-1,len(s)-1)
        s = s.tolist() # list has faster __getitem__
        ns = len(s)
        def gen():
            idx = 0
            yield idx
            while idx < ns:
                idx = s[idx]
                yield idx
        offs = np.fromiter(gen(),int)
        sz = np.diff(offs)>>1
        mx = sz.max()+1
        out = np.zeros(offs.size-1,int)
        for i in range(mx):
            out[b[offs[1:]-i-1] & (sz>=i)] += 1<<i
        return out
    

class EncodedInvertedIndex(MutableMapping):
    """
    Stores values of 
    """
    possible_encoders = {
        'eliasgamma':EliasGammaEncoder
    }
    def __init__(self, inverted_index: dict[str, set], encoding_method='eliasgamma'):
        self.__dict = inverted_index
        self.encoder: AbstractEncoder = self.possible_encoders[encoding_method]()

        for key in tqdm(self.__dict):
            self.__dict[key] = self.__encode_value(self.__dict[key])


    def load_encoded_dict(self, encoded_dict):
        self.__dict = encoded_dict

    def get_encoded_dict(self):
        return self.__dict


    def __encode_value(self, arr: set) -> np.array:
        np_arr = np.array(list(arr))
        encoded_arr = self.encoder.encode(np_arr)
        return encoded_arr
    
    def __decode_value(self, encoded_arr: np.array) -> set:
        if len(encoded_arr) == 0:
            return encoded_arr
        decoded_arr = self.encoder.decode(encoded_arr)
        return set(list(decoded_arr))

    def __getitem__(self, key):
        decoded_value = self.__decode_value(self.__dict[key])
        return decoded_value
    
    def __setitem__(self, key, value):
        encoded_value = self.__encode_value(value)
        self.__dict[key] = encoded_value

    def __delitem__(self, key):
        del self.__dict[key]

    def __iter__(self):
        return iter(self.__dict)
    
    def __len__(self):
        return len(self.__dict)
    
    def __str__(self):
        """returns simple str of a dict, values will be encoded"""
        return str(self.__dict)
    
    def __repr__(self):
        return '{}, D({})'.format(super(EncodedInvertedIndex, self).__repr__(), 
                                  self.__dict)

