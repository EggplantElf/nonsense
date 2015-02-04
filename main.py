# conding: utf-8
import sys
from corpus import *
from generator import *
from editor import *

def test1():
    edi = Editor()    
    cor = Corpus('corpora/english.conll09', edi, 1000)
    print len(cor.feat_dict)
    # for k in sorted(cor.feat_dict.keys(), key = lambda x: sum(cor.feat_dict[x].values()), reverse = True):
        # print k, cor.feat_dict[k]
        # print k, sum(cor.feat_dict[k].values())
    for k in cor.root_dict:
        print k, cor.root_dict[k]
    print cor.feat_dict[k]

def test2():
    edi = Editor()    
    cor = Corpus('corpora/english.conll09', edi, 1000)
    gen = Generator(cor, edi)
    t = gen.generate()
    print t.str


def test3():
    edi = Editor()
    cor = Corpus('corpora/english.conll09', edi, 1000)
    gen = Generator(cor, edi)
    i = 0
    while True:
        t = gen.generate()
        print sum(len(n.form) + 1 for n in t.nodes)
        if 50 < t.char_len() < 100:
            print t.to_str()
            i += 1
        # if i > 500:
            break

def test4(word):
    edi = Editor()
    cor = Corpus('corpora/english.conll09', edi, 1000)
    gen = Generator(cor, edi)
    i = 0
    while True:
        t = gen.generate(word)
        print sum(len(n.form) + 1 for n in t.nodes)
        if 50 < t.char_len() < 100:
            print t.to_str()
            i += 1
        # if i > 500:
            break

if __name__ == '__main__':
    test4(sys.argv[1])