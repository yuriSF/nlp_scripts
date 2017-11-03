from nltk.corpus import treebank
import nltk
t = treebank.parsed_sents('/Users/yuriyerastov/Documents/arg_struct/out/searchMovie.parsed.txt')[2]





def getNodes(parent, node_label):
    #print parent
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == node_label:
                print node.label(), node.leaves()
                print 'type ', type(node)
            else:
                getNodes(node, node_label)

getNodes(t, 'NP')
# print ''
# print t
