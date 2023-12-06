from nltk.translate.bleu_score import sentence_bleu

# 1. "한국인 나트륨 일일 평균 섭취량을 알려줘.
reference = [["this", "is", "the", "sample"]]

for i in range(0,10):
    candidate = ['this', "is", "the", "sample"]
    score1 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)) # 1.0