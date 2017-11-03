'''
This script annotates sentences for semantic roles.
'''

from nltk import sent_tokenize
from practnlptools.tools import Annotator

annotator=Annotator()
args = ['R-A0', 'R-A1', 'AM-MNR', 'V', 'R-A2', 'AM-EXT', 'A1', 'A0',
        'A3', 'A2', 'A4', 'C-V', 'AM-DIR', 'AM-DIS', 'AM-TMP', 'AM-PNC',
        'AM-LOC', 'AM-MOD', 'AM-CAU', 'C-A1', 'AM-ADV', 'AM-NEG']

def annotate(data):
    #the data input is a list of lines
    arg_dict = []
    for ind, line in enumerate(data):
        print ind, line, 'out of ', len(data)
        sents = sent_tokenize(line)
        for sent in sents:
            parse = annotator.getAnnotations(sent, dep_parse=True)['srl']
            print parse
            for item in parse:
                arg_dict.append(item)
                labels = item.keys()
                print 'label ', labels
                for label in labels:
                    if label not in arg_roles.keys():
                        arg_roles[label] = 0

    return arg_dict
