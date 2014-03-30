import cPickle
import re
import gzip
import time

class Corpus(list):
    def __init__(self, corpus_file, limit = 999999):
        self.read(corpus_file, limit)


    def read(self, corpus_file, limit):
        lines = []
        for line in open(corpus_file):
            if line.strip():
                lines.append(line.strip())
            else:
                # self[len(self)] = self.build_node(lines)
                self.append(self.build_node(lines))
                lines = []
                if len(self) >= limit:
                    break

    def build_node(self, lines):
        root = None
        nodes = {}
        for line in lines:
            items = line.split('\t')
            nid, form, lemma, pos, hid, label = int(items[0]), items[1], items[2], items[4], int(items[8]), items[10]
            nodes[nid] = (hid, Node(form, lemma, pos, label))

        for nid in nodes:
            (hid, node) = nodes[nid]
            if hid != 0:
                # node['head'] = nodes[hid][1]
                head = nodes[hid][1]
                if nid < hid:
                    # node['head']['ldeps'].append(node)
                    head['ldeps'].append(node)
                else:
                    # node['head']['rdeps'].append(node)
                    head['rdeps'].append(node)
            else:
                root = node
        return root



class Node(dict):
    def __init__(self, form, lemma, pos, label):
        self['form'] = form
        self['lemma'] = lemma
        self['pos'] = pos
        self['label'] = label
        # self['head'] = None
        self['ldeps'] = []
        self['rdeps'] = []

    def show(self):
        print self.info()
        print 'left: [%s]' % ' '.join([n.info() for n in self['ldeps']]) #filter punctuations
        print 'right: [%s]' % ' '.join([n.info() for n in self['rdeps']])

    def info(self):
        return '(%s/%s/%s)' % (self['form'], self['pos'], self['label']) 


class Collection(dict):
    def __init__(self):
        self = {}

    # def add_pattern(self, pattern):
    #     self[pattern] = []

    def save( self, filename ):
        stream = gzip.open(filename,'wb')
        cPickle.dump(self,stream,-1)
        stream.close()

    def load( self, filename ):
        stream = gzip.open(filename,'rb')
        self = cPickle.load(stream)
        stream.close()
        return self


    def scan(self, pattern, node):
        if pattern.match(node):
            self[pattern].append(node)
        for n in node['ldeps']:
            self.scan(n)
        for n in node['rdeps']:
            self.scan(n)

    def add_corpus(self, corpus, node_attrs, dep_attrs):
        for node in corpus:
            self.add_node(node, node_attrs, dep_attrs)

    def add_node(self, node, node_attrs, dep_attrs):
        p = Pattern().simulate(node, node_attrs, dep_attrs)
        pstr = p.to_string()
        if pstr not in self:
            self[pstr] = []
        self[pstr].append(node)
        for dep in node['ldeps'] + node['rdeps']:
            self.add_node(dep, node_attrs, dep_attrs)

    def filter(self, filter_pattern):
        new_collection = {}
        for p in self:
            nodes = filter(filter_pattern.match, self[p])
            if nodes:
                new_pstr = str(dict(filter_pattern.items() + eval(p).items()))
                new_collection[new_pstr] = nodes
        return new_collection


class Pattern(dict):
    def __init__(self, form = None, lemma = None, pos = None, label = None, ldeps = None, rdeps = None):
        self['form'] = form
        self['lemma'] = lemma
        self['pos'] = pos
        self['label'] = label
        self['ldeps'] = ldeps
        self['rdeps'] = rdeps

    # need extension
    def simulate(self, node, node_attrs, dep_attrs):
        for attr in node_attrs:
            self[attr] = node[attr]

        if dep_attrs:
            self['ldeps'], self['rdeps'] = [], []    
            for dep in node['ldeps']:
                p = Pattern().simulate(dep, dep_attrs, None)
                self['ldeps'].append(p)
            for dep in node['rdeps']:
                p = Pattern().simulate(dep, dep_attrs, None)
                self['rdeps'].append(p)
        return self



    def to_string(self):
        return str(self)

    def from_string(self, string):
        self.__init__(eval(string))


    def match(self, node):
        if any([(self[attr] and self[attr] != node[attr]) for attr in ['form', 'lemma', 'pos', 'label']]):
            return False
        if self['ldeps'] != None and (len(self['ldeps']) != len(node['ldeps']) \
                or not all([p.match(n) for (p, n) in zip(self['ldeps'], node['ldeps'])])):
            return False
        if self['rdeps'] != None and (len(self['rdeps']) != len(node['rdeps']) \
                or not all([p.match(n) for (p, n) in zip(self['rdeps'], node['rdeps'])])):
            return False
        return True





def test1():
    corpus = Corpus('corpora/english.conll09', 2)
    collection = Collection()
    # collection.add_corpus(corpus, ['pos'], ['pos'])
    collection.add_node(corpus[1], ['pos'], ['pos'])
    for k in collection:
        if len(collection[k]) > 0:
            print k, len(collection[k])
            for inst in collection[k]:
                print '\t', inst

def test2():
    t0 = time.time()
    print 'read',
    corpus = Corpus('corpora/english.conll09')
    t1 = time.time()
    print t1 - t0

    print 'collect',
    collection = Collection()
    collection.add_corpus(corpus, ['pos'], ['pos'])
    t2 = time.time()
    print t2 - t1

    print 'save',
    collection.save('test.gz')
    t3 = time.time()
    print t3 - t2

    print 'load',
    collection = Collection().load('test.gz')
    print time.time() - t3

def test3():
    corpus = Corpus('corpora/english.conll09', 1000)
    collection = Collection()
    collection.add_corpus(corpus, ['form'], ['pos', 'label'])
    filter_pattern = Pattern(pos = 'VBD')
    # print filter_pattern
    new_collection = collection.filter(filter_pattern)

    for p in sorted(new_collection.keys(), key = lambda x: len(new_collection[x]), reverse = True)[:20]:
        print p, len(new_collection[p])



if __name__ == '__main__':
    test3()



