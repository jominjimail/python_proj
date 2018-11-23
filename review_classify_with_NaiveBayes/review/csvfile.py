import csv

f = open('kor_review.csv','w',encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(["이게 왜 명작 이라는 건지", 0.5])
wr.writerow(["감동이 오지 않음에 나 역시 놀란다 내가 문제인걸까",2])
f.close()