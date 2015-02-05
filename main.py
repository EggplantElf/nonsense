# conding: utf-8
import sys
from corpus import *
from generator import *
from editor import *


def test3():
    edi = Editor()
    cor = Corpus('corpora/english.conll09', edi, 1000)
    gen = Generator(cor, edi)
    i = 0
    while True:
        t = gen.generate()
        if 40 < t.char_len() < 100:
            print t.to_str()
            i += 1
            break

def test4(word):
    edi = Editor()
    cor = Corpus('corpora/english.conll09', edi, 1000)
    gen = Generator(cor, edi)
    i = 0
    while True:
        t = gen.generate(word)
        if 30 < t.char_len() < 80:
            print t.to_str()
            i += 1
        # if i > 500:
            break

if __name__ == '__main__':
    # test3()
    test4(sys.argv[1])