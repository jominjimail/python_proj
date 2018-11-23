import sys
from pprint import pprint
from collections import defaultdict
import codecs
import math
import time
from konlpy.tag import Twitter
import winsound

start = time.time()

def tokenize(message):
    t = Twitter()
    #all_words = t.nouns(message)
    all_words= t.pos(message,norm=True, stem=True)
    #pprint(all_words)
    return set(all_words)


class NaiveBayes():
    def __init__(self,k=0.5):
        self.k =k
        self.word_prob_table =[]

    def text_read(self,where):
        f = codecs.open("./" + where + ".txt", 'r', "utf-8")
        line = f.readline()
        line2 = f.readline()
        list1 = []
        while line2:
            line2 = line2.replace("\r\n", '')
            result2 = line2.split("\t")
            # pprint(result2)
            list1.append([result2[1], result2[2]])
            line2 = f.readline()
        return list1

    def count_words(self,out_list):
        counts = defaultdict(lambda: [0, 0])  # [neg , pos] checking
        for review, tag in out_list:
            if self.isNumber(review) is False:
                words = tokenize(review)
                #pprint(words)
                for word in words:
                    if word[1] in ['Punctuation','Conjunction','Josa','Eomi']:
                        #print(word[0])
                        continue
                    counts[word][int(tag)] += 1
        return counts

    def isNumber(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def file_len(self,where):
        f = codecs.open("./" + where + ".txt", 'r', "utf-8")
        for i, l in enumerate(f):
            pass
        f.close()
        return i

    def position_check(self,out_list, list_pos, list_neg):
        for i in out_list:
            if i[1] == '0':
                list_neg.append(i[0])
            else:
                list_pos.append(i[0])

    def word_probability(self,word_count, negnum, posnum, k):
        return [(w,
                 (class0 + k) / (negnum + 2 * k),
                 (class1 + k) / (posnum + 2 * k))
                for w, (class0, class1) in word_count.items()]

    def class0_probability(self,word_prob_table, query_review):
        log_prob_if_class0 = log_prob_if_class1 = 0.0
        query_words = tokenize(query_review)
        query_words2 = set()
        #pprint(query_words)
        #print(type(query_words))
        for d in query_words:
            if d[1] in ['Punctuation','Conjunction','Josa']:
                continue
            else:
                query_words2.add((d[0],d[1]))
        #print(query_words2)

        for word, prob_if_class0, prob_if_class1 in word_prob_table:
            if word in query_words:
                log_prob_if_class0 += math.log(prob_if_class0)
                log_prob_if_class1 += math.log(prob_if_class1)

            else:
                log_prob_if_class0 += math.log(1.0 - prob_if_class0)
                log_prob_if_class1 += math.log(1.0 - prob_if_class1)

        prob_if_class0 = math.exp(log_prob_if_class0)
        prob_if_class1 = math.exp(log_prob_if_class1)

        if (prob_if_class0 > prob_if_class1):
            return 0
        else:
            return 1

    def train(self,trainfile_path):
        out_list = self.text_read(train_name)
        # pprint(out_list)
        list_pos = []
        list_neg = []
        self.position_check(out_list, list_pos, list_neg)
        # pprint(list_neg)
        # pprint(list_pos)
        totalnum = self.file_len(train_name)
        posnum = len(list_pos)
        negnum = len(list_neg)
        word_count = self.count_words(out_list)
        # pprint(word_count)
        self.word_prob_table = self.word_probability(word_count, negnum, posnum, self.k)
        # pprint(word_prob_table)
        print("word_prob_table size : ", len(self.word_prob_table))
        print("train_fin")

    def classify(self, query_review):
        return self.class0_probability(self.word_prob_table, query_review)

    def scoring(self,name2):
        answer_list = self.text_read(name2)
        # pprint(answer_list)
        answernum = self.file_len(name2)
        print("answer_sheet num: ", answernum)
        corret = 0
        counting = 0;
        for ans in answer_list:
            if counting % 1000 == 0:
                print("calculating .... ", counting)
            if ans[1] == '':
                continue
            prediction = self.classify(ans[0])
            if int(ans[1]) == prediction:
                corret += 1
            counting += 1
        print(corret / answernum)

    def result(self,where):
        f = codecs.open("./" + where + ".txt", 'r', "utf-8")

        line = f.readline()
        line2 = f.readline()
        list2 = []
        while line2:
            line2 = line2.replace("\r\n", '')
            result2 = line2.split("\t")
            #pprint(result2)
            list2.append([result2[0], result2[1]])
            line2 = f.readline()
        f.close()

        # pprint(list1)
        f2 = codecs.open("./" + "ratings_result" + ".txt", 'w+', "utf-8")
        string3 = 'id	document	label\n'
        f2.write(string3)

        print('documnet writing...')
        counting2 =0
        for ans in list2:
            if counting2 % 1000 == 0:
                print("calculating .... ", counting2)
            prediction = self.classify(ans[1])
            ans.append(str(prediction))
            #print(ans)
            string2 = ans[0]+'\t'+ans[1]+'\t'+ans[2]+'\n'
            f2.write(string2)
            counting2 += 1
        f2.close()

model = NaiveBayes()
train_name ="ratings_train"
valid_name ="ratings_valid"
test_name = "ratings_test"
model.train(train_name)
model.scoring(valid_name)
model.result(test_name)

print("--- {}s seconds ---",format(time.time() - start))
winsound.Beep(500,1000)
