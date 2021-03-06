import sys
sys.path.append('.')
import json
from collections import Counter
from itertools import product, islice
import pickle
from feature import word_ngrams
def set_and_lower_set(tokens):
    return tokens, list(map(str.lower, tokens))

def collect_tokens(x):
    res = []
    for y in x:
        res.extend(y)
    return res

if __name__ == '__main__':
    df = {}
    for type, is_lower, source in product(['word_ngram', 'word_stemmed_ngram'], [False, True],['title', 'description', 'description_sentence']):
        df[(type, is_lower, source)] = Counter()
    df['sentence_number_in_descriptions'] = 0

    def helper(tokens, tokens_lower, type, source, word_ngram_range=None):
        if word_ngram_range is not None:
            df[(type, False, source)].update(set(word_ngrams(tokens, word_ngram_range)))
            df[(type, True, source)].update(set(word_ngrams(tokens_lower, word_ngram_range)))
        else:
            df[(type, False, source)].update(set(tokens))
            df[(type, True, source)].update(set(tokens_lower))


    for line in open('./data/data_files/ItemInfo_preprocessed.jsonl'):
        line = json.loads(line.rstrip())

        tokens, tokens_lower = set_and_lower_set(collect_tokens(line['title']))
        helper(tokens, tokens_lower, type='word_ngram', source='title')

        tokens, tokens_lower = set_and_lower_set(collect_tokens(line['title_stemmed']))
        helper(tokens, tokens_lower, type='word_stemmed_ngram', source='title')

        tokens, tokens_lower = set_and_lower_set(collect_tokens(line['description']))
        helper(tokens, tokens_lower, type='word_ngram', source='description')

        tokens, tokens_lower = set_and_lower_set(collect_tokens(line['description_stemmed']))
        helper(tokens, tokens_lower, type='word_stemmed_ngram', source='description')

        for sentence in line['description']:
            df['sentence_number_in_descriptions'] += 1
            tokens, tokens_lower = set_and_lower_set(sentence)
            helper(tokens, tokens_lower, type='word_ngram', source='description_sentence')

        for sentence in line['description_stemmed']:
            tokens, tokens_lower = set_and_lower_set(sentence)
            helper(tokens, tokens_lower, type='word_stemmed_ngram', source='description_sentence')

    pickle.dump(df, open('./data/data_files/df.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)