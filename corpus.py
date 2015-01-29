# conding: utf-8
from __future__ import division
from tree import *

class Corpus:
    # need refine feat: pos_label, word_pos_label, sense_pos_label, rhyme_pos_label etc.
    # compute freq for dict
    def __init__(self, corpus_file, limit = 999999):
        self.feat_dict = {}
        self.root_dict = {}
        self.read(corpus_file, limit)
        freq2dist(self.root_dict)
        for key in self.feat_dict:
            freq2dist(self.feat_dict[key])



    def read(self, corpus_file, limit):
        count = 0
        lines = []
        for line in open(corpus_file):
            if line.strip():
                lines.append(line.strip())
            else:
                self.add_feats(self.temp_tree(lines), True)
                count += 1
                lines = []
                if count >= limit:
                    break



    def temp_tree(self, lines):
        # nodes = [(-1, Node('ROOT', 'ROOT', [], []))]
        nodes = {}
        for line in lines:
            items = line.split('\t')
            nid, form, pos, hid, label = int(items[0]), items[1], items[4], int(items[8]), items[10]
            nodes[nid] = (hid, Node(form, '%s_%s' % (pos, label), [], []))

        root = None
        for nid in nodes:
            hid, node = nodes[nid]
            if hid == 0:
                root = node
            elif nid < hid:
                nodes[hid][1].ldeps.append(node)
            else:
                nodes[hid][1].rdeps.append(node)
        assert root
        return root

    def add_feats(self, tree, is_root = False):
        f = tree.feat
        if f not in self.feat_dict:
            self.feat_dict[f] = {}
        deps_str = ' '.join([d.feat for d in tree.ldeps]) + '|' + ' '.join([d.feat for d in tree.rdeps])
        p = (tree.form, deps_str)
        if p not in self.feat_dict[f]:
            self.feat_dict[f][p] = 1
        else:
            self.feat_dict[f][p] += 1
        if is_root:
            if f not in self.root_dict:
                self.root_dict[f] = 1
            else:
                self.root_dict[f] += 1
        for d in tree.ldeps + tree.rdeps:
            self.add_feats(d)






def freq2dist(dic):
    s = sum(dic.values())
    low = 0
    for k in sorted(dic.keys(), key = lambda x: dic[x], reverse= True):
        high = low + dic[k] / s 
        dic[k] = (low, high)
        low = high







