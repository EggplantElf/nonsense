import sys

def reformat(input, output):
	g = open(output, 'w')
	for line in open(input):
		if len(line) > 2:
			(id, wf, lm, posg, posp, mf, head, rel, und1, und2) = line.strip().split('\t')
			g.write('\t'.join([id, wf, lm, lm, posg, posp, mf, mf, head, head, rel, rel, und1, und2]) + '\n')
		else:
			g.write('\n')
	g.close()

reformat(sys.argv[1], sys.argv[2])