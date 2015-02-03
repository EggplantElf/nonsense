# conding: utf-8

import random
from tree import *

class Generator:
    def __init__(self, corpus, editor):
        self.feat_dict = corpus.feat_dict
        self.root_dict = corpus.root_dict
        self.editor = editor

    # assuming cand_dict is a dict, may change
    def choose(self, cand_dict):
        i = random.random()
        for k in cand_dict:
            if cand_dict[k][0] < i < cand_dict[k][1]:
                return k
        return k

    # expand constraint 
    def grow_down(self, tree, feat):
        # count = 0
        # while True:
        #     count += 1
        #     form, dep_feats = self.choose(self.feat_dict[feat])
        #     if self.editor.check(form) or count == 5:
        #         self.editor.add_dyn_form(form)
        #         break

        form, dep_feats = self.choose(self.feat_dict[feat])

        node = Node(form, feat)

        [lfeats, rfeats] = dep_feats.split('|')
        node.ldeps = [self.grow_down(tree, f) for f in lfeats.split(' ') if f]
        tree.add_node(node)
        node.rdeps = [self.grow_down(tree, f) for f in rfeats.split(' ') if f]
        return node

    def grow_up(self, feat):
        pass

    def generate(self):
        tree = Tree()
        root_feat = self.choose(self.root_dict)
        root = self.grow_down(tree, root_feat)
        tree.root = root
        # self.editor.reset_dyn_form()
        return tree

    def generate_given_word(self, form):
        pass




