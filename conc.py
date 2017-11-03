from general import *
from file_ops import *
from nltk import Text, word_tokenize, pos_tag_sents, pos_tag
import pickle
import sys
import nltk
#from morphology import Corpus
import os

# def get_tokens_string(directory, file_extension='txt'):
#     corpus = read_files_string(directory, file_extension)
#     tokens = nltk.word_tokenize(corpus)
#     return tokens

def display_grams_view(tokens, word, ngram_size=4, freq_lowest=2):
    coll_dist = find_ngrams_ByWord(word, tokens, ngram_size)
    coll_sorted = sort_ngrams(coll_dist, freq_lowest)
    pretty = prettify_colls(coll_sorted, word)
    user_path = raw_input('Path to directory to save results: ')
    path = user_path + word + str(ngram_size) + '.txt'
    with open(path, 'w') as f:
        sys.stdout = f
        print(pretty)
    return "Saved to file {}".format(path)

def word_view(tokens, word, directory):
    conc_left = my_conc(tokens, word, sort_direction='left')
    view_left = prettify_conc(conc_left)
    path =  directory + 'left.txt'
    with open(path, 'w') as f:
        sys.stdout = f
        print(view_left)

    conc_right = my_conc(tokens, word, sort_direction='right')
    view_right = prettify_conc(conc_right)
    path = directory + 'right.txt'
    with open(path, 'w') as f:
        sys.stdout = f
        print(view_right)
    f.close()
    return

def query_by_characters(data, word_first, word_second):
    # data is a list of lines
    for item in data:
        lines = item.split('\n')
        for line in lines:
            if word_first in line and word_second in line:
                print line
    return


def check_tags(tags):
    for tag in tags:
        if tag[1] in verb_tags:
            return tag
    return False

def get_verbless_sents(data):
    # input data are a list of lines
    verbless = []
    for item in data:
        lines = item.split('\n')
        for line in lines:
            if data_w in line:
                tags = pos_tag(word_tokenize(line))
                if tags:
                    check = check_tags(tags)
                    if check == False:
                        verbless.append(line)
    return verbless

def calculate_verb_frequency(data):
    verb_list = []
    for item in data:
        lines = item.split('\n')
        for line in lines:
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
    sorted_frequency = sorted(freq_dist, key=lambda x: x[1], reverse=True)
    return(sorted_frequency)
