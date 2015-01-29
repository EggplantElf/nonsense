# conding: utf-8

from corpus import *
from generator import *
from constraint import *

def test1():
    cor = Corpus('corpora/english.conll09', 1000)
    print len(cor.feat_dict)
    # for k in sorted(cor.feat_dict.keys(), key = lambda x: sum(cor.feat_dict[x].values()), reverse = True):
        # print k, cor.feat_dict[k]
        # print k, sum(cor.feat_dict[k].values())
    for k in cor.root_dict:
        print k, cor.root_dict[k]
    print cor.feat_dict[k]

def test2():
    cor = Corpus('corpora/english.conll09', 1000)
    filt = Filter()
    gen = Generator(cor, filt)
    t = gen.generate()
    print t.str


def test3():
    cor = Corpus('corpora/english.conll09', 1000)
    filt = Filter()
    gen = Generator(cor, filt)
    while True:
        t = gen.generate()
        # print t.len
        if 5 < t.len < 15:
            print t.str
            break


if __name__ == '__main__':
    test3()