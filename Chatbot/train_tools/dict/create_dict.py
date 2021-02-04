from utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle


def read_corpus_data(filename):
    with open(filename, 'r', encoding='utf8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]

    return data


corpus_data = read_corpus_data('/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/train_tools/dict/corpus.txt')

p = Preprocess()
dict = []

for c in corpus_data:
    pos = p.pos(c[1])
    for k in pos:
        dict.append(k[0])

tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index
# print(word_index)

f = open('chatbot_dict.bin', 'wb')

try:
    pickle.dump(word_index, f)

except Exception as e:
    print(e)

finally:
    f.close()