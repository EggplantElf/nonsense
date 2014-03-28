# conding: utf-8

from random import randint

PU = {'sw': ['MAD','MID'],
      'de': ['$.', '$,', '$('],
      'pt': ['punc'],
      'ch': ['PU']}


def read_corpus(filename):
    f = open(filename)
    corpus = {}
    count = 1
    for line in f:
        if len(line) > 2:
            items = line.split()
            index, word, pos, mor, link, label = int(items[0].split('_')[-1]), items[1], items[4], \
                    items[6], int(items[8]), items[10]
            if count not in corpus:
                corpus[count] = {}
            corpus[count][index] = (word, pos, mor, link, label)
        else:
            count += 1 
    return corpus

def select(corpus, hd, pos, mor, label, head, seed):
    cand = []
    prior_cand = []
    for sid in corpus:
        for index in corpus[sid]:
            if corpus[sid][index][1] == pos and corpus[sid][index][2] == mor and corpus[sid][index][4] == label:
                cand.append((corpus[sid][index], sid, index))
                if head != '-ROOT-' and corpus[sid][index][0] != seed and corpus[sid][index][0] in hd[head]:
                    prior_cand.append((corpus[sid][index], sid, index))
    #print seed, prior_cand
    if prior_cand:
        return prior_cand[randint(0, len(prior_cand) - 1)]
    else:
        return cand[randint(0, len(cand) - 1)]

def children(corpus, hd, pos, mor, label, head, seed, lan):
    ((word, pos, mor, link, label), sid, index) = select(corpus, hd, pos, mor, label, head, seed)
    tree = [(word, pos)]
    for i in corpus[sid]:
        if corpus[sid][i][3] == index and corpus[sid][i][1] not in PU[lan]:
            p, m, l = corpus[sid][i][1], corpus[sid][i][2], corpus[sid][i][4]
            if i < index:
                tree = [children(corpus, hd, p, m, l, corpus[sid][index][0], corpus[sid][i][0], lan)] + tree
            else:
                tree = tree + [children(corpus, hd, p, m, l, corpus[sid][index][0], corpus[sid][i][0], lan)]
    return tree
    
def generate(corpus, hd, language):
    roots = []
    for sid in corpus:
        for i in corpus[sid]:
            if corpus[sid][i][3] == 0:
                roots.append((corpus[sid][i][0], corpus[sid][i][1], corpus[sid][i][2], corpus[sid][i][4]))
    (word, pos, mor, label) = roots[randint(0, len(roots) - 1)]
    tree = children(corpus, hd, pos, mor, label, '-ROOT-', word, language)
    tree = adjust(tree, language)
    sentence = to_str(tree)
    pos = to_pos(tree)
    return sentence, pos

def adjust(tree, language):
    if language == 'de':
        # change the place of article
        tree = check_art(tree)
    return tree
        
        
def check_art(tree):
    new_tree = []
    #print 1, tree
    for node in tree:
        if type(node) == tuple:
            new_tree.append(node)
        if type(node) == list:
            if len(node) > 1:
                new_tree.append(check_art(node))
            elif len(node) == 1:
                if node[0][1] == 'ART': # or more specific
                    new_tree = [node] + new_tree
                else:
                    new_tree.append(node)
    #print 2, new_tree
    return new_tree                
    
def read_tree(tree):
    wlist = []
    for node in tree:
        if type(node) == tuple:
            wlist.append(node[0])
        else:
            wlist += read_tree(node)
    return wlist

def to_str(tree):
    wlist = read_tree(tree)
    return ' '.join(wlist)

def to_pos(tree):
    pos_tree = []
    for node in tree:
        if type(node) == tuple:
            pos_tree.append(node[1])
        else:
            pos_tree.append(to_pos(node))
    return pos_tree
            

def hd_pair(corpus):
    pairs = {}
    for sid in corpus:
        for index in corpus[sid]:
            if corpus[sid][index][3] != 0:
                dep = corpus[sid][index][0]
                head = corpus[sid][corpus[sid][index][3]][0]
                if head not in pairs:
                    pairs[head] = {}
                if dep not in pairs[head]:
                    pairs[head][dep] = 1
                else:
                    pairs[head][dep] += 1
    return pairs

def dh_pair(corpus):
    pairs = {}
    for sid in corpus:
        for index in corpus[sid]:
            if corpus[sid][index][3] != 0:
                dep = corpus[sid][index][0]
                head = corpus[sid][corpus[sid][index][3]][0]
                if dep not in pairs:
                    pairs[dep] = {}
                if head not in pairs[dep]:
                    pairs[dep][head] = 1
                else:
                    pairs[dep][head] += 1
    return pairs
    
def dep(corpus):
    dep_hd = {}
    dep_dh = {}
    for sid in corpus:
        for index in corpus[sid]:
            (dep, pos, mor, link, label) = corpus[sid][index]
            if link == 0:
                # 
                continue
            head = corpus[sid][link][0]
            if label not in dep_hd:
                dep_hd[label] = {}
                dep_dh[label] = {}
            if dep not in dep_dh[label]:
                dep_dh[label][dep] = {}
            if head not in dep_dh[label][dep]:
                dep_dh[label][dep][head] = 1
            else:
                dep_dh[label][dep][head] += 1
            if head not in dep_hd[label]:
                dep_hd[label][head] = {}
            if dep not in dep_hd[label][head]:
                dep_hd[label][head][dep] = 1
            else:
                dep_hd[label][head][dep] += 1
    return (dep_hd, dep_dh)
    
    
if __name__ == '__main__':
    corpus = read_corpus('german.conll09')
#    (hd, dh) = dep(corpus)
#    for h in hd['NK']:
#        print h
#        for d in hd['NK'][h]:
#            print '\t', d, hd['NK'][h][d]
    hd = hd_pair(corpus)
    o = open('output5.txt', 'w')
    for i in range(200):
        s, p = generate(corpus, hd, 'de')
        if len(p) < 20:
            print s
        #print p
            o.write(s + '\n')
    o.close()

    
    print 'done'