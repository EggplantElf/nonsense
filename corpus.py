# conding: utf-8
from __future__ import division
from tree import *
from editor import *

class Corpus:
    # need refine feat: pos_label, word_pos_label, sense_pos_label, rhyme_pos_label etc.
    # compute freq for dict
    def __init__(self, corpus_file, editor, limit = 999999):
        self.feat_dict = {}
        self.root_dict = {}
        self.editor = editor
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
            form = self.editor.map(pos, form)
            nodes[nid] = (hid, Node(form, self.editor.encode_feat(form, pos, label), [], []))

        root = None
        for nid in filter(lambda x:x, nodes):
            hid, node = nodes[nid]
            if hid == 0:
                root = node
            elif node.feat.split('_')[0] in self.editor.pos_blacklist or node.form in self.editor.form_blacklist:
                pass
            elif nid < hid:
                nodes[hid][1].ldeps.append(node)
            else:
                nodes[hid][1].rdeps.append(node)
        assert root
        return root

    def add_feats(self, node, is_root = False):
        f = node.feat
        if f not in self.feat_dict:
            self.feat_dict[f] = {}
        deps_str = ' '.join([d.feat for d in node.ldeps]) + '|' + ' '.join([d.feat for d in node.rdeps])
        p = (node.form, deps_str)
        if p not in self.feat_dict[f]:
            self.feat_dict[f][p] = 1
        else:
            self.feat_dict[f][p] += 1
        if is_root:
            if f not in self.root_dict:
                self.root_dict[f] = 1
            else:
                self.root_dict[f] += 1
        for d in node.ldeps + node.rdeps:
            self.add_feats(d)






def freq2dist(dic):
    s = sum(dic.values())
    low = 0
    for k in sorted(dic.keys(), key = lambda x: dic[x], reverse= True):
        high = low + dic[k] / s 
        dic[k] = (low, high)
        low = high







