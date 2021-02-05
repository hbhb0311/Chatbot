import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

class IntentModel:
    def __init__(self, model_name, preprocess):
        self.labels = {0 : '인사', 1: '욕설', 2: '주문', 3: '예약', 4: '기타'}
        self.model = load_model(model_name)
        self.p = preprocess

    def predict_class(self, query):
        pos = self.p.pos(query)
        keywords = self.p.get_keywords(pos, without_tag = True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        from config.Globalparams import MAX_SEQ_LEN
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen = MAX_SEQ_LEN, padding = 'post')
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis = 1)

        return predict_class.numpy()[0]
