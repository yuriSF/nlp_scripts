from nltk import word_tokenize, sent_tokenize
import nltk

def get_all_lines():
    all_data = []
    for f in files:
        path = d + f
        data = open_file(path)
        all_data.extend(data)
    return all_data

def get_sentences(lines):
    all_sents = []
    for line in lines:
        sents = sent_tokenize(line)
        all_sents.extend(sents)
    return all_sents

def get_freq_dist(arr):
    # takes in a list of tokens; outputs list of tuples sorted by frquency
    fdist = nltk.FreqDist(arr)
    fdist_list = [(item, fdist[item]) for item in fdist]
    fdist_list_sorted = sorted(fdist_list, key=lambda x: x[1], reverse = True)
    return fdist_list_sorted

def tokenize(sents):
    all_tokens = []
    for sent in sents:
        tokens = word_tokenize(sent)
        all_tokens.extend(tokens)
    return all_tokens

def tokenize(words):
    return nltk.word_tokenize(words)

def find_ngrams_ByWord(word, tokens, n):
    ngrams = nltk.ngrams(tokens, n)
    l = []
    for gram in ngrams:
        if word in gram:
            l.append(gram)
    return l

def find_ngrams(tokens, n):
    ngrams = nltk.ngrams(tokens, n)
    l = []
    for gram in ngrams:
        l.append(gram)
    return l

def sort_ngrams(colls, lower_limit=2):
    collocations = []
    fdist = nltk.FreqDist(colls)
    for key in fdist:
        t = key, fdist[key]
        if fdist[key] > lower_limit:
            collocations.append(t)
    coll_sorted = sorted(collocations, key=lambda x: x[1], reverse=True)
    return coll_sorted

def prettify_colls(coll_sorted, w):
    from prettytable import PrettyTable
    t = PrettyTable(['BEFORE', 'TARGET', 'AFTER', 'FREQUENCY'])
    t.align['BEFORE'] = 'r'
    t.align['TARGET'] = 'c'
    t.align['AFTER'] = 'l'
    t.align['FREQUENCY'] = 'l'
    t.border = False
    for item in coll_sorted:
        coll = item[0]
        pivot = coll.index(w)
        before = ' '.join(coll[0:pivot])
        after = ' '.join(coll[pivot+1:-1])
        freq = item[1]
        t.add_row([before, coll[pivot], after, freq])
    return t

def prettify_conc(coll_sorted):
    from prettytable import PrettyTable
    t = PrettyTable(['BEFORE', 'TARGET', 'AFTER'])
    t.align['BEFORE'] = 'r'
    t.align['TARGET'] = 'c'
    t.align['AFTER'] = 'l'
    #t.align['FREQUENCY'] = 'l'
    t.border = False
    for item in coll_sorted:
        t.add_row([item[0], item[1], item[2]])
    return t

def my_conc(tokens, w,
            window_left=10,
            window_right=10,
            sort_direction=''):
    hits = []

    for ind, token in enumerate(tokens):
        if token == w:
            before = ' '.join(reversed(tokens[ind-window_left:ind]))
            after = ' '.join(tokens[ind+1:ind+window_right])
            row = [before, token, after]
            hits.append(row)

    if sort_direction == 'left':
        sorted_hits = sorted(hits, key=lambda x: x[0], reverse=False)
    elif sort_direction == 'right':
        sorted_hits = sorted(hits, key=lambda x: x[2], reverse=False)
    else:
        sorted_hits = hits

    for hit in sorted_hits:
        hit[0] = ' '.join(reversed(hit[0].split(' ')))
        # hit[0] = ' '.join(reversed(list(hit[0])))
        # print hit[0]
    return sorted_hits

def sort_sents(tokenized_sents, w):
    hits = []
    for tokens in tokenized_sents:
        for ind, token in enumerate(tokens):
            if token == w:
                before = tokens[0:ind]
                after = tokens[ind+1:len(tokens)+1]
                row = [before, token, after]
                hits.append(row)
    # hits is a tokenized/ sentencized list
    #hits = [item[0].reverse() for item in hits]
    left = sorted(hits, key=lambda x: reversed(x[0]), reverse=False)
    right = sorted(hits, key=lambda x: x[2], reverse=False)
    new_left, new_right = [], []
    for item in left:
        print 'before ', item
        print item[0]
        zero = ' '.join(item[0])
        print item[0]
        two = ' '.join(item[2])
        print 'after ', item
        one = item[1]
        new_left.append([zero, one, two])
    for item in right:
        print 'before ', item
        print item[0]
        zero = ' '.join(item[0])
        print item[0]
        two = ' '.join(item[2])
        print 'after ', item
        one = item[1]
        new_right.append([zero, one, two])
    print new_left
    print new_right
    return(new_left, new_right)
