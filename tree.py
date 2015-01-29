# conding: utf-8


class Node:
    def __init__(self, form, feat, ldeps, rdeps):
        self.form = form
        self.feat = feat
        self.ldeps = ldeps
        self.rdeps = rdeps

    def to_str(self):
        return '%s %s %s' %(' '.join([d.to_str() for d in self.ldeps]),\
                            self.form,\
                            ' '.join([d.to_str() for d in self.rdeps]))




    def len(self):
        return 1 + sum(d.len() for d in self.ldeps + self.rdeps)

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
    def __init__(self, root):
        self.root = root
        self.glob_feat = None
        self.len = root.len()
        self.str = root.to_str()
        self.wlist = self.str.split(' ')


class Feat:
    def __init__(self):
        pass

    def get_feat(self):
        return None