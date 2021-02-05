from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel

p = Preprocess(word2index_dic = '/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/train_tools/dict/chatbot_dict.bin',
               userdic = '/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/utils/user_dic.tsv')

intent = IntentModel(model_name = '/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/models/intent/intent_model.h5',
                     preprocess = p)

# 아무 질문이나 query에 넣어서 테스트 진행 #
query = '저녁 7시에 삼겹살 먹으러 가려고 하는데 예약되나요?'
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print('의도 예측 클래스 : ', predict)
print('의도 예측 레이블 : ', predict_label)
