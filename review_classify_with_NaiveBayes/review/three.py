from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from pprint import pprint

Kkma= Kkma()
kom = Komoran()
hann = Hannanum()

sentence ='아버지가 방에 들어 가신다.'
twt = Twitter()
tagging = twt.pos(sentence)
pprint(tagging)

Kkma_tagger = Kkma.pos(sentence)
pprint(Kkma_tagger)

kom_tagger = kom.pos(sentence)
pprint(kom_tagger)