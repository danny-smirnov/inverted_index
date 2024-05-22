import numpy as np
from abc import ABC, abstractmethod
from collections.abc import MutableMapping

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
        return np.packbits(out),out.size

    @staticmethod
    def decode(b: np.array, n: int):
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
    possible_encoders = {
        'eliasgamma':EliasGammaEncoder
    }
    def __init__(self, inverted_index: dict[str, set], encoding_method='eliasgamma'):
        self.__dict__ = inverted_index
        self.encoder: AbstractEncoder = self.possible_encoders[encoding_method]()

        for key in self.__dict__:
            self.__dict__[key] = self.__encode_value(self.__dict__[key])


    def __encode_value(self, arr: set) -> tuple[list, int]:
        np_arr = np.array(list(arr))
        encoded_arr, n = self.encoder.encode(np_arr)
        return (list(encoded_arr), n)
    
    def __decode_value(self, arr: tuple[list, int]) -> set:
        encoded_arr, n = arr
        np_arr = np.array(encoded_arr)
        decoded_arr = self.encoder.decode(np_arr, n)
        return set(list(decoded_arr))

    def __getitem__(self, key):
        decoded_value = self.__decode_value(self.__dict__[key])
        return decoded_value
    
    def __setitem__(self, key, value):
        encoded_value = self.__encode_value(value)
        self.__dict__[key] = encoded_value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)
    
    def __len__(self):
        return len(self.__dict__)
    
    def __str__(self):
        """returns simple str of a dict, values will be encoded"""
        return str(self.__dict__)
    
    def __repr__(self):
        return '{}, D({})'.format(super(EncodedInvertedIndex, self).__repr__(), 
                                  self.__dict__)

