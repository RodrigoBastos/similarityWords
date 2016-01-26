# coding=utf-8
import math
from textblob import TextBlob as tb
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def remove_stopwords (sentences):
    phrases = []
    for sentence in sentences:
        #Gera tokens
        tokens = []
        words = word_tokenize(sentence)
        for word in words:
            if word.lower() not in stopwords:
                tokens.append(word)
        phrases.append(' '.join(tokens))
    return phrases

def get_cosine(vec1, vec2):
    size = len(vec1) - 1
    numerator = sum([vec1[x] * vec2[x] for x in range(size)])

    sum1 = sum([vec1[x]**2 for x in range(size)])
    sum2 = sum([vec2[x]**2 for x in range(size)])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator: return 0.0
    else: return float(numerator) / denominator

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    # + 1 para não zerar o denominador
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

#Get StopWords
stopwords = stopwords.words('portuguese')
stopwords.append('pra')

#Lendo arquivo com sentenças
file = open('dataset/sentences.txt')
sentences = file.readlines()
sentences = filter(None, sentences)

#Removendo stopwords
sentences = remove_stopwords(sentences)

#Inicializando Bloblist
bloblist = []
for phrase in sentences:
    bloblist.append(tb(phrase))


table = []
allWords = []
wordsPerDocument = {}

#Gerando TFIDF das palavras
for i, blob in enumerate(bloblist):
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    table.append(scores)

#Todas as palavras
for blob in bloblist:
    for word in blob.words:
        if word not in allWords:
            allWords.append(word)

#Gerando vetores das Palavras por Documento
for word in allWords:

    for document in table:
        #Pegar a pontuação de cada palavra no Documento, caso a p
        score = document[word] if document.__contains__(word) else 0

        if wordsPerDocument.__contains__(word):
            wordsPerDocument[word].append(score)
        else:
            wordsPerDocument[word] = [score]

#Calculando a similaridade das palavras com 'apple' através do cosseno
appleVector = wordsPerDocument.pop('apple')
for nameWord in wordsPerDocument:

    cos = get_cosine(appleVector, wordsPerDocument[nameWord])
    if cos > 0.5:
        print (nameWord, cos)


