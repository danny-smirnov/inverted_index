import pickle

def read_index(index_path):
    with open(index_path, 'rb') as f:
        index = pickle.load(f)
    return index

def get_num_of_words(index):
    return len(index)

def get_avg_elias_code(index):
    lengths = [len(x[0]) for x in index.values()]
    return sum(lengths) / len(lengths)




if __name__ == '__main__':
    delta_index_path = '/Users/daniilsmirnov/blekanov_3/data/index/af947f4d241233e795ada699eec759a8.pickle'
    gamma_index_path = '/Users/daniilsmirnov/blekanov_3/data/index/b82a8d8322bce1697cea7c8a4a3305cc.pickle'
    gamma_index = read_index(gamma_index_path)
    delta_index = read_index(delta_index_path)
    print(get_avg_elias_code(delta_index))
    print(get_avg_elias_code(gamma_index))
