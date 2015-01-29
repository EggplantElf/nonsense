# conding: utf-8

import random
from tree import *
# from filt import *

class Generator:
    def __init__(self, corpus, filt):
        self.feat_dict = corpus.feat_dict
        self.root_dict = corpus.root_dict
        self.filt = filt

    # default first choice, need overriding
    # assuming cand_dict is a dict, may change
    def choose(self, cand_dict):
        i = random.random()
        for k in cand_dict:
            if cand_dict[k][0] < i < cand_dict[k][1]:
                return k
        return k

    # def choose_random_root(self):
    #     i = random.random()
    #     for k in self.root_dict:
    #         if self.root_dict[k][0] < i < self.root_dict[k][1]:
    #             return k


    # expand constraint 
    def decode(self, feat):
        count = 0
        while True:
            count += 1
            form, dep_feats = self.choose(self.feat_dict[feat])
            if self.filt.check(form) or count == 5:
                self.filt.add_dyn_form(form)
                break
        # print form, dep_feats

        [lfeats, rfeats] = dep_feats.split('|')
        ldeps = [self.decode(f) for f in lfeats.split(' ') if f]
        rdeps = [self.decode(f) for f in rfeats.split(' ') if f]
        return Node(form, feat, ldeps, rdeps)

    def generate(self):
        root = self.choose(self.root_dict)
        tree = Tree(self.decode(root))
        self.filt.reset_dyn_form()
        return tree
