# conding: utf-8


class Node:
    def __init__(self, form, feat, ldeps = [], rdeps = [], tree = None):
        self.form = form
        self.feat = feat
        self.ldeps = ldeps
        self.rdeps = rdeps
        self.tree = tree

    # def add_ldeps(self, deps):
    #     self.ldeps.append(deps)

    # def add_rdeps(self, deps):
    #     self.rdeps.append(deps)


    # def to_str(self):
    #     return '%s %s %s' %(' '.join([d.to_str() for d in self.ldeps]),\
    #                         self.form,\
    #                         ' '.join([d.to_str() for d in self.rdeps]))

    # def len(self):
    #     return 1 + sum(d.len() for d in self.ldeps + self.rdeps)

    def struct(self):
        for d in self.ldeps:
            d.struct()
        print '\t', self.form, '\n'
        for d in self.rdeps:
            d.struct()

    def show(self):
        print self.info()
        print 'left: [%s]' % ' '.join([n.info() for n in self.ldeps]) #filter punctuations
        print 'right: [%s]' % ' '.join([n.info() for n in self.rdeps])

    def info(self):
        return '(%s/%s)' % (self.form, self.feat) 



class Tree:
    def __init__(self):
        self.root = None
        self.nodes = [] #unsorted list, but not set
        self.glob_feat = None

    def len(self):
        return len(self.nodes)

    def char_len(self):
        return sum(len(n.form) + 1 for n in self.nodes)

    def to_str(self):
        # return self.root.to_str()
        return ' '.join([n.form for n in self.nodes])

    def add_node(self, node):
        self.nodes.append(node)

