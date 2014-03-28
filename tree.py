def build(head, rest, index): 
    if not rest:
        return head
    removed = []
    for i in rest:
        (word, pos, mor, link, label) = rest[i]
        if link == index:
            removed.append(i)
            head[1].append([(index, word, pos, mor, label), []])
    for i in removed:
        rest.pop(i)
    for child in head[1]:
        child[1] = build(child, rest, child[0][0]) 
    return head
    
def print_tree(tree, d):
    print tree[0]
    if tree[1]:
        for child in tree[1]:
            print '\t' * (d + 1),
            print_tree(child, d + 1)


f = open('swedish.conll09')
corpus = {}
sid = 0
tmp = {}

for line in f:
    if len(line) > 2:
        items = line.split()
        index, word, pos, mor, link, label = int(items[0].split('_')[-1]), items[1], items[4], \
                    items[6], int(items[8]), items[10]
        tmp[index] = (word, pos, mor, link, label)
    else:
        rindex = [i for i in tmp if tmp[i][3] == 0][0]
        (word, pos, mor, link, label) = tmp[rindex]
        root = [(index, word, pos, mor, label), []]
        tree = build(root, tmp, rindex)
        break
    
print_tree(tree, 0)