from nltk.translate.bleu_score import sentence_bleu
import csv
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

"""
1-1. Bleu score: 
reference: https://jrc-park.tistory.com/273
"""

f = list(csv.reader(open("question-keyword-answer.csv",'r')))

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
reference = ["한국인의 일일 나트륨 평균 섭취량은 약 4500mg 입니다.".split()]

score1_arr = []
for row in range(1,11):
    candidate = f[row][2].replace(",","").split()  # answer
    score1 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)) # 1.0
    score1_arr.append(score1)

# print(score1_arr)

# 2. "전청조의 사기 액수를 알려줘."
reference = ["천청조의 사기 액수는 36억 9000여만원입니다.".split(),"전청조는 사기를 통해 약 37억원의 피해액을 발생시켰습니다.".split(), "전청조에 의해 발생한 피해액은 36억9000여만원 입니다.".split()]
score2_arr = []
for row in range(11,21):
    candidate = f[row][2].replace(",","").split()  # answer
    score2 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0))  # 1.0
    score2_arr.append(score2)

# print(score2_arr)

"""
1-2. 막대그래프로 표현
"""
x = [1,2,3,4,5,6,7,8,9,10]

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
plt.subplot(1,2,1)
plt.bar(x, score1_arr)
plt.ylim([0,1])

# 2. "전청조의 사기 액수를 알려줘."
plt.subplot(1,2,2)
plt.bar(x, score2_arr)
plt.ylim([0,1])

plt.show()