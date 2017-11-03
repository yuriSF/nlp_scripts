from general import *
from file_ops import *
from corpus import *
from nltk import Text, word_tokenize, pos_tag_sents, pos_tag
import pickle
import sys
import nltk
#from morphology import Corpus
import os
import time
start_time = time.time()

def check_tags(tags):
    for tag in tags:
        if tag[1] in verb_tags:
            return tag
    return False

def display_targets(query, query_w, query_second):
    for item in query:
        lines = item.split('\n')
        for line in lines:
            if query_w in line and query_second in line:
                print line
    return

def display_verbless(query, query_w):
    print "BEGIN"
    for item in query:
        lines = item.split('\n')
        for line in lines:
            if query_w in line:
                tags = pos_tag(word_tokenize(line))
                if tags:
                    check = check_tags(tags)
                    if check == False:
                        print line
    return

def display_verbs(query, query_w):
    verb_list = []
    print "BEGIN"
    for item in query:
        lines = item.split('\n')
        for line in lines:
            if query_w in line:
                tags = pos_tag(word_tokenize(line))
                if tags:
                    check = check_tags(tags)
                    if check:
                        verb = check[0]
                        print check[0].upper(), line
                        verb_list.append(verb)
    uniqs = list(set(verb_list))
    freq_dist = []
    for verb in uniqs:
        row = (verb, verb_list.count(verb))
        freq_dist.append(row)
    return freq_dist

def match_words(words, tokens):
    words = [word.lower() for word in words]
    tokens = [token.lower() for token in tokens]
    for word in words:
        if word not in tokens:
            return False
    return True

def get_token_matches(query_list, sentencized_corpus):
    # corpus_structure: [ [sentence [word], [word] ] ]
    matches = []
    for sent in sentencized_corpus:
        flag = False
        if match_words(query_list, sent):
            print(sent)
            matches.append(sent)
    return matches

def concatenate_tokens(sent):
    concatenated = ' '.join(sent)
    return concatenated


def write_freq(fd):
    print fd
    verb_file = raw_input('File to save verb frequency: ')
    os.chdir('/Users/yuriyerastov/Documents/arg_struct/output/')
    freq_dist = sorted(fd, key=lambda x: x[1], reverse=True)
    for item in freq_dist:
        print item
        with open(verb_file, 'a') as f:
            line = '{0}: {1}\n'.format(item[0], item[1])
            f.write(line)
    return

def dump_corpus(directory, pickle_file):
    import pickle
    data = read_files_string(directory, 'txt')
    corpus = Corpus(data, 'english')
    corpus.sentencize()
    tokenized_sentences = corpus.get_sentence_tokens()
    pickle.dump(tokenized_sentences, open(pickle_file, 'w'))
    print('dumped')

if __name__ == '__main__':
    print os.getcwd()
    args = sys.argv[1:]
    p_file = '/Users/yuriyerastov/Documents/arg_struct/filtered_intents/corpus_temp.p'
    #dump_corpus('/Users/yuriyerastov/Documents/arg_struct/filtered_intents', p_file)
    corpus = pickle.load(open(p_file, 'rb'))
    token_matches = get_token_matches(args, corpus)
    sorted_lists = sort_sents(token_matches, args[0])
    table_left = prettify_conc(sorted_lists[0])
    table_right = prettify_conc(sorted_lists[1])
    print table_left
    print table_right
    print("--- %s seconds ---" % (time.time() - start_time))
