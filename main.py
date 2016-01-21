

def main ():
    file = open('dataset/sentences.txt')
    sentences = file.readlines()
    sentences = filter(None, sentences)


    print sentences

main()