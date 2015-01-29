#coding: utf-8

from random import choice
import re


class Corpus(dict):
    def __init__(self, corpus_file, cfg_file, limit = 999999):
        print 'reading corpus...'
        self.pattern = Pattern()
        lines = []
        cfg = self.read_cfg(cfg_file)
        for line in open(corpus_file):
            if len(line) > 2:
                lines.append(line)
            else:
                self[len(self)] = Tree(lines, cfg)
                lines = []
                if len(self) >= limit:
                    break
                if len(self) % 10000 == 0:
                    print len(self)


    def read_cfg(self, cfg_file):
        cfg = {}
        for line in open(cfg_file):
            if len(line) > 1:
                tmp = line.split('=')
                cfg[tmp[0].strip()] = eval(tmp[1])
        return cfg
    
    def add_node_pattern(self, args):
        print 'adding node pattern... %s' % str(tuple(sorted(args)))
        for i in self:
            for j in self[i].nodes:
                self.pattern.add_node(self[i].nodes[j], args)

    def add_tree_pattern(self, head_args, deps_args = None):
        if not deps_args:
            deps_args = head_args
        print 'adding tree pattern... %s' % str((tuple(sorted(head_args)),tuple(sorted(deps_args))))
        for i in self:
            for j in self[i].nodes:
                self.pattern.add_tree(self[i].nodes[j], head_args, deps_args)

    def add_pair_pattern(self, head_args, deps_args = None):
        if not deps_args:
            deps_args = head_args
        print 'adding pair pattern... %s' % str((tuple(sorted(head_args)),tuple(sorted(deps_args))))
        for i in self:
            for j in self[i].nodes:
                self.pattern.add_pair(self[i].nodes[j], head_args, deps_args)



    def random_node(self, args):
        args = tuple(sorted(args))
        values = choice(self.pattern.node[args].keys())
        node = choice(self.pattern.node[args][values])
        return node

    # def random_node_with_constraint(self, args, values):
    #     return choice(self.pattern.node[args][values])

    def generate_with_filter(self, args, nodes, filtern):
        wlist = []
        for node in nodes:
            # new_node = self.random_node_with_constraint(args, tuple([node[arg] for arg in args]))
            # if self.pattern.node['form'][node['form']]

            same_form = self.pattern.node[('form',)][(node['form'],)]
            if len(same_form) > 10:
                new_node = choice(same_form)
            else:
                values = tuple([node[arg] for arg in args])
                new_node = choice(self.pattern.node[args][values])
            if filtern(new_node):
                wlist += self.random_tree(args, new_node, filtern)
        return wlist

    def random_tree(self, args, node, filtern):
        args = tuple(sorted(args))
        wlist = self.generate_with_filter(args, node.ldeps, filtern)
        wlist += [node]
        wlist += self.generate_with_filter(args, node.rdeps, filtern)      
        return wlist        

    def random_sentence(self, args, filtern = lambda x: True):
        sent = None
        while not sent:
            root = choice(self).root
            wlist = self.random_tree(args, root, filtern)
            sent = Sentence(wlist)
            if not sent.is_valid():

                sent = None

        return sent.post_process()
        
        


class Sentence():
    def __init__(self, nodes):
        self.nodes = nodes
        self.forms = []

    # select random trees with constraints
    def is_valid(self):
        s = ' '.join([n['form'] for n in self.nodes])
        if len(s) > 100 or len(s) < 50:
            return False

        # At most a pair of quote
        lq = len([n for n in self.nodes if n['form'] == '``'])
        rq = len([n for n in self.nodes if n['form'] == '\'\''])
        if lq != rq or lq + rq > 2:
            return False

        if not any([n for n in self.nodes if n['pos'] not in ['VBZ', 'VBP', 'VBD']]):
            return False

        for i in range(len(self.nodes) - 1):
            if self.nodes[i]['pos'] == 'CD' and self.nodes[i+1]['pos'] == 'CD':
                return False

        return True

    # def pre_process(self):
    #     new_nodes = []
    #     for node in self.nodes:
            


    def post_process(self):
        def no_space_before(m):
            if m.group(0):
                return m.group(0)[1:]

        def no_space_after(m):
            if m.group(0):
                return m.group(0)[:-1]

        def capitalize(m):
            if m.group(0):
                return m.group(0).upper()

        # lowercase words that are not proper noun
        for node in self.nodes:
            if node['pos'] in ['NNP', 'NNPS'] or node['lemma'] in ['i']:
                self.forms.append(node['form'])
            else:
                self.forms.append(node['form'].lower())


        s = ' '.join(self.forms)
        # simple replacement
        s = s.replace('{', '(').replace('}', ')').replace('\/', '/').replace('n\'t', 'not')
        s = re.sub(r'`` | \'\'', '"', s)
        s = re.sub(r' [.,:!?;\'%\-)&]', no_space_before, s) # delete the space before some symbol
        s = re.sub(r'[($\-&] ', no_space_after, s) # delete the space after some symbol
        s = re.sub(r'\$\D', '$3.14', s)
        s = re.sub(r' \D+%', ' 3.14%', s)


        s = re.sub(r'\w', capitalize, s, count = 1)
        return s




class Node(dict):
    def __init__(self, features):
        for f in features:
            self[f] = features[f]
        self.head = None
        self.deps = []
        self.ldeps = []
        self.rdeps = []
        self.level = -1

    def pattern(self, args):
        pairs = [(arg, self[arg]) for arg in args]
        return dict(pairs)

    def values(self, args):
        return tuple([self[arg] for arg in args])

class Tree:
    def __init__(self, lines, cfg):
        self.nodes = {}
        for line in lines:
            tmp = line.split()
            features = {}
            for f in cfg:
                features[f] = cfg[f][1](tmp[cfg[f][0]])
            self.nodes[features['id']] = Node(features)
        h = -1        
        for nid in self.nodes:
            head_id = self.nodes[nid]['head_id'] 
            if head_id == 0:
                h = nid
            else:
                head = self.nodes[head_id]
                self.nodes[nid].head = head
                head.deps.append(self.nodes[nid])
                if nid < head_id:
                    head.ldeps.append(self.nodes[nid])
                else:
                    head.rdeps.append(self.nodes[nid])
        self.root = self.nodes[h]
        self.__set_level(self.root, 0)


    # Helper for pretty print 
    def __set_level(self, node, level):
        node.level = level
        for c in node.deps:
            self.__set_level(c, level + 1)


    def pprint(self, dep = True, arg = 'form'):
        for i in self.nodes:
            if self.nodes[i].head:
                if self.nodes[i].head['id'] < i:
                    sign = '\\-- '
                else:
                    sign = '/-- ' 
            else:
                sign = ''
            print '\t' * self.nodes[i].level + sign + self.nodes[i][arg],
            if dep:
                print '(%s/%s)' % (self.nodes[i]['pos'], self.nodes[i]['label'])
            else:
                print

class Pattern:
    def __init__(self):
        self.node = {}
        self.tree = {}
        self.hd_pair = {}
        self.dh_pair = {}

    def add_node(self, node, args):
        args = tuple(sorted(args))
        values = tuple([node[arg] for arg in args])        
        if args not in self.node:
            self.node[args] = {}
        if values not in self.node[args]:
            self.node[args][values] = []
        self.node[args][values].append(node)
    
    def add_pair(self, node, head_args, deps_args = None):
        if not deps_args:
            deps_args = head_args
        head_args = tuple(sorted(head_args))
        deps_args = tuple(sorted(deps_args))
        head_values = tuple([node[arg] for arg in head_args])
        #deps_values = [tuple([dep[arg] for arg in deps_args]) for dep in node.deps]
        args = (head_args, deps_args)
        for dep in node.deps:
            dep_values = tuple([dep[arg] for arg in deps_args])
            # hd_pair
            if args not in self.hd_pair:
                self.hd_pair[args] = {}
            if head_values not in self.hd_pair[args]:
                self.hd_pair[args][head_values] = {}
            if dep_values not in self.hd_pair[args][head_values]:
                self.hd_pair[args][head_values][dep_values] = []
            self.hd_pair[args][head_values][dep_values].append((node, dep))
            # dh_pair
            if args not in self.dh_pair:
                self.dh_pair[args] = {}
            if dep_values not in self.dh_pair[args]:
                self.dh_pair[args][dep_values] = {}
            if head_values not in self.dh_pair[args][dep_values]:
                self.dh_pair[args][dep_values][head_values] = []
            self.dh_pair[args][dep_values][head_values].append((dep, node))
           


    # may not be necessary 
    def add_tree(self, node, head_args, deps_args = None):
        if not deps_args:
            deps_args = head_args
        head_args = tuple(sorted(head_args))
        deps_args = tuple(sorted(deps_args))
        head_values = tuple([node[arg] for arg in head_args])
        deps_values = tuple([tuple([dep[arg] for arg in deps_args]) for dep in node.deps])
        args = (head_args, deps_args)
        values = (head_values, deps_values)
        if args not in self.tree:
            self.tree[args] = {}
        if head_values not in self.tree[args]:
            self.tree[args][head_values] = {}
        if deps_values not in self.tree[args][head_values]:
            self.tree[args][head_values][deps_values] = []
        self.tree[args][head_values][deps_values].append((node, node.deps))

    def print_node_pattern(self):
        for p in self.node:
            for v in self.node[p]:
                print v, self.node[p][v]

    def print_tree_pattern(self):
        for p in self.tree:
            for v in self.tree[p]:
                print v, self.tree[p][v]
    
    def node_statistics(self, args, values, output_args, limit = 0):
        if type(output_args) == str:
            output_args = tuple([output_args])
        if type(values) == str:
            values = tuple([values])
        pairs = sorted(zip(args, values))        
        args = tuple([p[0] for p in pairs])
        values = tuple([p[1] for p in pairs])
        stat = {}
        for arg in output_args:
            stat[tuple([arg])] = {}
        for inst in self.node[args][values]:
            for arg in output_args:
                arg = tuple([arg])
                v = inst.values(arg)
                if v not in stat[arg]:
                    stat[arg][v] = []
                stat[arg][v].append(inst)
        for arg in output_args:
            arg = tuple([arg])
            for (v, i) in sorted(stat[arg].items(), key = lambda x: len(x[1]), reverse = True):
                if len(stat[arg][v]) > limit:
                    print ', '.join(v), len(stat[arg][v])


    def tree_statistics(self, head_args, deps_args = None):
        if not deps_args:
            deps_args = head_args
        head_args = tuple(sorted(head_args))
        deps_args = tuple(sorted(deps_args))
        args = (head_args, deps_args)
        dic = self.tree[args]
        print '-' * 30
        print 'tree statistics for args:', head_args, deps_args
        for (head, deps) in sorted(dic.items(), key = lambda x: sum([len(x[1][inst]) for inst in x[1]]), reverse = True):
            print ', '.join(head),  '\t\t', sum([len(deps[inst]) for inst in deps])
            for (value, instances) in sorted(deps.items(), key = lambda x: len(x[1]), reverse = True):
                if value:
                    output = ', '.join(['(' + ', '.join(p) + ')' for p in value])
                else:
                    output = 'None'

                print '\t', output, '\t',  len(instances)

    def pair_statistics(self, direction, head_args, deps_args = None):
        if not deps_args:
            deps_args = head_args
        head_args = tuple(sorted(head_args))
        deps_args = tuple(sorted(deps_args))
        args = (head_args, deps_args)
        if direction == 'hd':
            pair = self.hd_pair[args]
        elif direction == 'dh':
            pair = self.dh_pair[args]
        else:
            print 'incorrect argument'
            return
        print '-' * 30
        print direction + '_pair statistics for args:', head_args, deps_args
        for (head, deps) in sorted(pair.items(), key = lambda x: sum([len(x[1][inst]) for inst in x[1]]), reverse = True):
            print ', '.join(head), '\t\t',  sum([len(deps[inst]) for inst in deps])
            for (value, instances) in sorted(deps.items(), key = lambda x: len(x[1]), reverse = True):
                print '\t', ', '.join(value), '\t', len(instances)


def generate(output):
    args = ['pos', 'label']
    corpus = Corpus('corpora/english.conll09', 'config/english.cfg', 1000)
    corpus.add_node_pattern(args)
    corpus.add_node_pattern(['form'])      

    g = open(output, 'w')
    for i in range(100):
        sent = corpus.random_sentence(args)#'$' not in x['pos'])
        g.write(sent + '\n')
    g.close()



def demo(): 
    args = ['pos']
    head_args = ['pos']
    deps_args = ['dep']
    corpus = Corpus('train.German.gold.conll', 'german.cfg', 100)
    corpus.add_node_pattern(args)
#    corpus.add_pair_pattern(head_args, deps_args)
#    corpus.add_tree_pattern(head_args, deps_args) 
    
    #corpus.pattern.pair_statistics('hd', args)
#    corpus.pattern.node_statistics(args, 'ADJA', 'lm',  3)
#    corpus.pattern.pair_statistics('hd', head_args, deps_args)
#    corpus.pattern.tree_statistics(head_args, deps_args)
       
if __name__ == '__main__':
    #demo()
    generate('a.txt')







