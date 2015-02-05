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

    # recursive
    def grow_down(self, tree, feat, dep_str = '', form = ''):
        if not form:
            form, dep_str = self.choose(self.corpus.feat_td_dict[feat])

        node = Node(form, feat)
        [lfeats, rfeats] = dep_str.split('|')
        node.ldeps = [self.grow_down(tree, f) for f in lfeats.split(' ') if f]
        tree.add_node(node)
        node.rdeps = [self.grow_down(tree, f) for f in rfeats.split(' ') if f]
        return node

    # non-recursive
    def grow_up(self, tree, node):
        # print node.feat
        form, feat, dep_str = self.choose(self.corpus.feat_bu_dict[node.feat])
        head = Node(form, feat)
        [lfeats, rfeats] = dep_str.split('|')
        head.ldeps = [(node if f == '@_@' else self.grow_down(tree, f)) for f in lfeats.split(' ') if f]
        tree.add_node(head)
        head.rdeps = [(node if f == '@_@' else self.grow_down(tree, f)) for f in rfeats.split(' ') if f]
        return head

    def generate(self, given_word = ''):
        tree = Tree()
        if not given_word:
            root_feat = self.choose(self.corpus.root_dict)
            node = self.grow_down(tree, root_feat)
            tree.settle(node)
        elif given_word in self.corpus.form_dict:
            feat, dep_str = self.choose(self.corpus.form_dict[given_word])
            node = self.grow_down(tree, feat, dep_str, given_word)
            while node.feat not in self.corpus.root_dict:
                node = self.grow_up(tree, node)
            tree.settle(node)
        else:
            raise Exception('Out of vocabulary')
            exit(0)

        return tree

        
    def generate_given_word(self, form):
        pass




