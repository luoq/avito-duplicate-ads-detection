import numpy as np
import os
import pickle

def df_sample_n(data, n, seed=None):
    rng = np.random.RandomState(seed)
    N = data.shape[0]
    return data.iloc[rng.choice(range(N), n)]

def with_cache(cache_file, g):
    if os.path.exists(cache_file):
        return pickle.load(open(cache_file, 'rb'))
    else:
        res = g()
        pickle.dump(res, open(cache_file, 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)
        return res

def list_to_location_map(l):
    return dict(zip(l, range(len(l))))

from collections import OrderedDict

class DataFrameNDArrayWrapper:

    def __init__(self, df):
        self.d = df.values
        self.row_names = df.index.tolist()
        self.column_names = df.columns.tolist()
        self.row_name_to_loc = list_to_location_map(self.row_names)
        self.column_name_to_loc = list_to_location_map(self.column_names)

    def get_row_as_dict(self, row_name):
        i = self.row_name_to_loc[row_name]
        row = self.d[i]
        return OrderedDict(zip(self.column_names, row))


def ngrams(tokens, ngram_range, stop_words=None):
    """Turn tokens into a sequence of n-grams after stop words filtering"""
    # handle stop words
    if stop_words is not None:
        tokens = [w for w in tokens if w not in stop_words]

    # handle token n-grams
    min_n, max_n = ngram_range
    if max_n != 1:
        original_tokens = tokens
        tokens = []
        n_original_tokens = len(original_tokens)
        for n in range(min_n,
                        min(max_n + 1, n_original_tokens + 1)):
            for i in range(n_original_tokens - n + 1):
                tokens.append(" ".join(original_tokens[i: i + n]))

    return tokens