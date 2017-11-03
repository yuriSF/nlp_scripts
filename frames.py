import pickle, csv
from nltk import stem


def write_csv_rows(f, rows):
    with open(f, 'wb') as csvfile:
        csv.writer(csvfile).writerows(rows)

def write_csv_rows(f, rows):
    with open(f, 'wb') as csvfile:
        csv.writer(csvfile).writerows(rows)

def lemmatize(verbs):
    lemmas = []
    for verb in verbs:
        if ' ' in verb:
            spl = verb.split(' ')
            #print spl
            verb_proper, part = spl[0], spl[1]
            lemma = stem.WordNetLemmatizer().lemmatize(verb_proper, 'v')
            lemma = lemma + ' ' + spl[1]
        else:
            lemma = stem.WordNetLemmatizer().lemmatize(verb, 'v')

        lemmas.append(lemma)
    return lemmas


def count_list(l, uniq_l):
    counts = []
    for item in uniq_l:
        n = l.count(item)
        row = [item, n]
        counts.append(row)
    ordered = sorted(counts, key = lambda row: row[1], reverse=True)
    return ordered


verbs = pickle.load(open('V.p', 'rb'))
verbs_filt = [verb.lower() for verb in verbs]
lemmas = lemmatize(verbs_filt)
uniqs = list(set(lemmas))
ordered_l = count_list(lemmas, uniqs)
write_csv_rows('verb_summary.csv', ordered_l)
