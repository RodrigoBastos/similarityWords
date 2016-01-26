# coding=utf-8
import math
from textblob import TextBlob as tb
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


#STOPWORDS
stopwords = stopwords.words('portuguese')
stopwords.append('pra')


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

def get_bloblist(sentences):
    bloblist = []
    for phrase in sentences:
        bloblist.append(tb(phrase))

    return bloblist

def get_words(bloblist):
    allWords = []
    #Todas as palavras
    for blob in bloblist:
        for word in blob.words:
            if word not in allWords:
                allWords.append(word)
    return allWords

def get_scores (bloblist):
    #Gerando TFIDF das palavras
    table = []
    for i, blob in enumerate(bloblist):
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        table.append(scores)
    return table

def get_vectors (words, table):
    #Gerando vetores das Palavras por Documento
    wordsPerDocument = {}
    for word in words:

        for document in table:
            #Pegar a pontuação de cada palavra no Documento, caso a p
            score = document[word] if document.__contains__(word) else 0

            if wordsPerDocument.__contains__(word):
                wordsPerDocument[word].append(score)
            else:
                wordsPerDocument[word] = [score]

    return wordsPerDocument

def get_similarity_words (wordsPerDocument):
    #Calculando a similaridade das palavras com 'apple' através do cosseno
    response = []
    appleVector = wordsPerDocument.pop('apple')
    for nameWord in wordsPerDocument:
        value = get_cosine(appleVector, wordsPerDocument[nameWord])
        if value > 0.5:
            response.append({'word': nameWord,'value': value})

    return response

def main ():

    #Lendo arquivo com sentenças
    file = open('dataset/sentences.txt')
    sentences = file.readlines()
    sentences = filter(None, sentences)

    #Removendo stopwords (para remover retire o comentário da linha abaixo)
    #sentences = remove_stopwords(sentences)

    #Inicializando Bloblist
    bloblist = get_bloblist(sentences)
    allWords = get_words(bloblist)
    table = get_scores(bloblist)
    wordsPerDocument = get_vectors(allWords, table)

    response = get_similarity_words(wordsPerDocument)

    for item in response:
        print (item['word'], item['value'])

main()
