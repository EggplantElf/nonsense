# conding: utf-8

import random
from tree import *

class Generator:
    def __init__(self, corpus, editor):
        self.corpus = corpus
        self.editor = editor

    # assuming cand_dict is a dict, may change
    def choose(self, cand_dict):
        i = random.random()
        for k in cand_dict:
            if cand_dict[k][0] < i < cand_dict[k][1]:
                return k
        return k

    # expand constraint 
    def grow_down(self, tree, feat, form = ''):
        if form:
            dep_feats = feat
        else:
            form, dep_feats = self.choose(self.corpus.feat_dict[feat])

        node = Node(form, feat)
        [lfeats, rfeats] = dep_feats.split('|')
        node.ldeps = [self.grow_down(tree, f) for f in lfeats.split(' ') if f]
        tree.add_node(node)
        node.rdeps = [self.grow_down(tree, f) for f in rfeats.split(' ') if f]
        return node


    def grow_up(self, feat):
        pass

    def generate(self, given_word = ''):
        tree = Tree()
        if not given_word:
            root_feat = self.choose(self.corpus.root_dict)
            root = self.grow_down(tree, root_feat)
            tree.root = root
        elif given_word in self.corpus.form_td_dict:
            feat = self.choose(self.corpus.form_td_dict[given_word])
            root = self.grow_down(tree, feat, given_word)
            tree.root = root
        else:
            self.out_of_vocabulary()

        return tree

    def out_of_vocabulary(self):
        raise OutOfVocab('Out of vocabulary')
        exit(0)

    def generate_given_word(self, form):
        pass




