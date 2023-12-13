import csv
import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

"""
1-1. Bleu score: 
reference: https://jrc-park.tistory.com/273
"""

f = list(csv.reader(open("question-keyword-answer.csv",'r')))

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
reference = ["한국인의 일일 나트륨 평균 섭취량은 약 4500mg 입니다.".split()]

score1_bleu_arr = []
for row in range(1,11):
    candidate = f[row][2].replace(",","").split()  # answer
    score1 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)) # 1.0
    score1_bleu_arr.append(score1)


# 2. "전청조의 사기 액수를 알려줘."
reference = ["천청조의 사기 액수는 36억 9000여만원입니다.".split(),"전청조는 사기를 통해 약 37억원의 피해액을 발생시켰습니다.".split(), "전청조에 의해 발생한 피해액은 36억9000여만원 입니다.".split()]
score2_bleu_arr = []
for row in range(11,21):
    candidate = f[row][2].replace(",","").split()  # answer
    score2 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0))  # 1.0
    score2_bleu_arr.append(score2)


"""
1-2. 막대그래프로 표현
"""
# 한글 지원
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

x = [1,2,3,4,5,6,7,8,9,10]

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
plt.subplot(1,2,1)
plt.title("한국인 나트륨 일일 평균 섭취량")
plt.bar(x, score1_bleu_arr)
plt.yticks(np.arange(0,1.1,0.1))

# 2. "전청조의 사기 액수를 알려줘."
plt.subplot(1,2,2)
plt.title("전청조의 사기 액수")
plt.bar(x, score2_bleu_arr)
plt.yticks(np.arange(0,1.1,0.1))

plt.suptitle("Bleu Score")
plt.show()

# print(score1_bleu_arr)
score1_bleu_avg = 0
for i in score1_bleu_arr:
    score1_bleu_avg += i
score1_bleu_avg = score1_bleu_avg / len(score1_bleu_arr)

# print(score1_bleu_arr)
# print(avg)

# print(score2_bleu_arr)
score2_bleu_avg = 0
for i in score2_bleu_arr:
    score2_bleu_avg += i
score2_bleu_avg = score2_bleu_avg / len(score2_bleu_arr)
# print(avg)

"""
2-1. TF-IDF + Cosine Similarity
reference:
1) TF-IDF: https://wikidocs.net/31698
2) Cosine similarity: https://yanoo.tistory.com/21
    - range: -1 ~ 1, high value, high similarity
"""

from sklearn.feature_extraction.text import TfidfVectorizer

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
reference = "한국인의 일일 나트륨 평균 섭취량은 약 4500mg 입니다."

score1_cs_arr = np.zeros(shape=(10,), dtype=np.float64)
for row in range(1,11):
    candidate = f[row][2]
    sent = (reference, candidate)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sent)
    score1 = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score1_cs_arr[row-1] = (score1[0][0] + 1) / 2
    # idf = tfidf_vectorizer.idf_

reference = "천청조의 사기 액수는 36억 9000여만원입니다." + " 전청조는 사기를 통해 약 37억원의 피해액을 발생시켰습니다." + " 전청조에 의해 발생한 피해액은 36억9000여만원 입니다."
score2_cs_arr = np.zeros(shape=(10,), dtype=np.float64)
for row in range(11,21):
    candidate = f[row][2]
    sent = (reference, candidate)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sent)
    score2 = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score2_cs_arr[row-11] = (score2[0][0] + 1) / 2
    # idf = tfidf_vectorizer.idf_

"""
2-2. 막대그래프로 표현
"""
x = [1,2,3,4,5,6,7,8,9,10]

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
plt.subplot(1,2,1)
plt.title("한국인 나트륨 일일 평균 섭취량")
plt.bar(x, score1_cs_arr)
plt.yticks(np.arange(0,1.1,0.1))

# 2. "전청조의 사기 액수를 알려줘."
plt.subplot(1,2,2)
plt.title("전청조의 사기 액수")
plt.bar(x, score2_cs_arr)
plt.yticks(np.arange(0,1.1,0.1))

score1_cs_avg = 0
for i in score1_cs_arr:
    score1_cs_avg += i
score1_cs_avg = score1_cs_avg / len(score1_cs_arr)
# print(score1_cs_arr)
# print(avg)

score2_cs_avg = 0
for i in score2_cs_arr:
    score2_cs_avg += i
score2_cs_avg = score2_cs_avg / len(score2_cs_arr)
# print(avg)

plt.suptitle("TF-IDF + Cosine Similarity")
plt.show()

print(f"Score1(BLEU Score)")
print(f"Min: {round(min(score1_bleu_arr),2)}, Max: {round(max(score1_bleu_arr),2)}, Avg: {round(score1_bleu_avg,2)}")
print(f"Score2(BLEU Score)")
print(f"Min: {round(min(score2_bleu_arr),2)}, Max: {round(max(score2_bleu_arr),2)}, Avg: {round(score2_bleu_avg,2)}")

print(f"Score1(CS)")
print(f"Min: {round(min(score1_cs_arr),2)}, Max: {round(max(score1_cs_arr),2)}, Avg: {round(score1_cs_avg,2)}")
print(f"Score2(CS)")
print(f"Min: {round(min(score2_cs_arr),2)}, Max: {round(max(score2_cs_arr),2)}, Avg: {round(score2_cs_avg,2)}")
