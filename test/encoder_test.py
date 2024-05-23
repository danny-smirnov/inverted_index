import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.utils import EliasGammaEncoder, EliasDeltaEncoder
import unittest
import numpy as np


class TestEncoder(unittest.TestCase):
    
    def setUp(self):
        self.encoder = EliasDeltaEncoder()

    def test_random_arrays(self):
        n = np.random.randint(1, 1000, 1)
        arr = np.random.choice(range(2*n[0]), n, replace=False)
        arr.sort()


        encoded = self.encoder.encode(arr)
        decoded = self.encoder.decode(*encoded)


        self.assertSequenceEqual(arr.tolist(), decoded.tolist())



if __name__ == '__main__':
    unittest.main()