# conding: utf-8
from __future__ import division
from tree import *
from editor import *

class Corpus:
    # need refine feat: pos_label, word_pos_label, sense_pos_label, rhyme_pos_label etc.
    # compute freq for dict
    def __init__(self, corpus_file, editor, limit = 999999):
        self.feat_td_dict = {}
        self.feat_bu_dict = {}
        self.root_dict = {}
        self.form_dict = {}
        self.editor = editor
        self.read(corpus_file, limit)
        freq2dist(self.root_dict)
        for key in self.feat_td_dict:
            freq2dist(self.feat_td_dict[key])
        for key in self.form_dict:
            freq2dist(self.form_dict[key])
        for key in self.feat_bu_dict:
            freq2dist(self.feat_bu_dict[key])



    def read(self, corpus_file, limit = 999999):
        count = 0
        lines = []
        for line in open(corpus_file):
            if line.strip():
                lines.append(line.strip())
            else:
                self.add_feats(self.temp_tree(lines), True)
                # k = self.feat_bu_dict.keys()[1]
                # print k, self.feat_bu_dict[k]
                # exit(0)
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
        w = node.form

        # add root dict
        if is_root:
            if f not in self.root_dict:
                self.root_dict[f] = 1
            else:
                self.root_dict[f] += 1

        # add feat_td_dict
        deps_str = ' '.join([d.feat for d in node.ldeps]) \
                 + '|' + ' '.join([d.feat for d in node.rdeps])
        p = (w, deps_str)
        if f not in self.feat_td_dict:
            self.feat_td_dict[f] = {}
        if p not in self.feat_td_dict[f]:
            self.feat_td_dict[f][p] = 1
        else:
            self.feat_td_dict[f][p] += 1

        # add form_dict
        p = (node.feat, deps_str)
        if w not in self.form_dict:
            self.form_dict[w] = {}
        if p not in self.form_dict[w]:
            self.form_dict[w][p] = 1
        else:
            self.form_dict[w][p] += 1

        # add feat_bu_dict
        # left deps
        for l in node.ldeps:
            deps_str = ' '.join([(d.feat if d != l else '@_@') for d in node.ldeps]) \
                     + '|' + ' '.join([d.feat for d in node.rdeps])
            f = l.feat
            t = (node.form, node.feat, deps_str)
            if f not in self.feat_bu_dict:
                self.feat_bu_dict[f] = {}
            if t not in self.feat_bu_dict[f]:
                self.feat_bu_dict[f][t] = 1
            else:
                self.feat_bu_dict[f][t] += 1
        # right deps
        for r in node.rdeps:
            deps_str = ' '.join([d.feat for d in node.ldeps]) + '|' \
                     + ' '.join([(d.feat if d != r else '@_@') for d in node.rdeps])
            f = r.feat
            t = (node.form, node.feat, deps_str)
            if f not in self.feat_bu_dict:
                self.feat_bu_dict[f] = {}
            if t not in self.feat_bu_dict[f]:
                self.feat_bu_dict[f][t] = 1
            else:
                self.feat_bu_dict[f][t] += 1

        # recursively add feats for deps
        for d in node.ldeps + node.rdeps:
            self.add_feats(d)






def freq2dist(dic):
    s = sum(dic.values())
    low = 0
    for k in sorted(dic.keys(), key = lambda x: dic[x], reverse= True):
        high = low + dic[k] / s 
        dic[k] = (low, high)
        low = high







