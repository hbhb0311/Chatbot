from utils.Preprocess import Preprocess

sent = "내일 오전 10시에 탕수육을 주문하고 싶어"
p = Preprocess(userdic = '/Users/hyebin/PycharmProjects/pycharmgit/Chatbot/utils/user_dic.tsv')
pos = p.pos(sent)
print(pos)

ret = p.get_kewords(pos, without_tag = False)
print(ret)

ret = p.get_kewords(pos, without_tag = True)
print(ret)