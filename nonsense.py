# coding: utf-8

from random import randint

def read_corpus(filename):
    f = open(filename)
    corpus = {}
    count = 1
    for line in f:
        if len(line) > 2:
            items = line.split()
            index, word, pos, head, label = int(items[0]), items[1], items[4], int(items[8]), items[10]
            if count not in corpus:
                corpus[count] = {}
            corpus[count][index] = (word, pos, head, label)
        else:
            count += 1 
    return corpus




if __name__ == '__main__':
    corpus = read_corpus('english.conll09')
    print corpus[1]

