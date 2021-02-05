import pandas as pd
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPooling1D, concatenate

train_file = "/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/models/intent/total_train_data.csv"
data = pd.read_csv(train_file)
queries = data['query'].tolist()
intents = data['intent'].tolist()

from utils.Preprocess import Preprocess

p = Preprocess(word2index_dic = '/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/train_tools/dict/chatbot_dict.bin',
               userdic = '/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/utils/user_dic.tsv')

sequences = []
for sentence in queries:
    pos = p.pos(sentence)
    keywords = p.get_keywords(pos, without_tag = True)
    seq = p.get_wordidx_sequence(keywords)
    sequences.append(seq)

from config.Globalparams import MAX_SEQ_LEN
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen = MAX_SEQ_LEN, padding = 'post')

ds = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
ds = ds.shuffle(len(queries))

train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

dropout_prob = 0.5
EMB_SIZE = 125
EPOCH = 5
VOCAB_SIZE = len(p.word_index) + 1

input_layer = Input(shape = (MAX_SEQ_LEN, ))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length = MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate = dropout_prob)(embedding_layer)

conv1 = Conv1D(filters = 128, kernel_size= 3, padding = 'valid', activation= tf.nn.relu)(dropout_emb)
pool1 = GlobalMaxPooling1D()(conv1)

conv2 = Conv1D(filters = 128, kernel_size= 4, padding = 'valid', activation= tf.nn.relu)(dropout_emb)
pool2 = GlobalMaxPooling1D()(conv2)

conv3 = Conv1D(filters = 128, kernel_size= 5, padding = 'valid', activation= tf.nn.relu)(dropout_emb)
pool3 = GlobalMaxPooling1D()(conv3)

concat = concatenate([pool1, pool2, pool3])

hidden = Dense(128, activation = tf.nn.relu)(concat)
dropout_hidden = Dropout(rate = dropout_prob)(hidden)
logits = Dense(5, name = 'logits')(dropout_hidden)
predictions = Dense(5, activation = tf.nn.softmax)(logits)

model = Model(inputs = input_layer, outputs = predictions)
model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
model.fit(train_ds, validation_data = val_ds, epochs = EPOCH, verbose = 1)

loss, accuracy = model.evaluate(test_ds, verbose = 1)
print('Accuracy : %f' % (accuracy * 100))
print('loss : %f' % (loss * 100))

model.save('intent_model.h5')