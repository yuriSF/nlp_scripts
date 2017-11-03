import pickle, csv
import os
from nltk import stem

buy = pickle.load(open('srl_output/buy.p', 'rb'))
request = pickle.load(open('srl_output/requestInfo.p', 'rb'))
searchM = pickle.load(open('srl_output/searchMovie.p', 'rb'))
searchTh = pickle.load(open('srl_output/searchTheater.p', 'rb'))
searchR = pickle.load(open('srl_output/searchReview.p', 'rb'))
searchS = pickle.load(open('srl_output/searchScreening.p', 'rb'))
searchT = pickle.load(open('srl_output/searchTrailer.p', 'rb'))

results = {'buy' : buy, 'requestInfo' : request,  'searchMovie' : searchM,
            'searchTheater' : searchTh,  'searchReview' : searchR,
            'searchScreening' : searchS , 'searchTrailer' :  searchT}

def write_csv_rows(f, rows):
    with open(f, 'wb') as csvfile:
        csv.writer(csvfile).writerows(rows)

def get_lemma(verb):
    if ' ' in verb:
        spl = verb.split(' ')
        verb_proper, part = spl[0].lower(), spl[1].lower()
        lemma = stem.WordNetLemmatizer().lemmatize(verb_proper, 'v').lower()
        return lemma + ' ' + spl[1]
    else:
        return stem.WordNetLemmatizer().lemmatize(verb, 'v').lower()


def lemmatize(verbs):
    lemmas = []
    verbs_lower = [verb.lower() for verb in verbs]
    verbs_filt = list(set(verbs_lower))
    for verb in verbs_filt:
        lemma = get_lemma(verb)
        lemmas.append(lemma)
    return lemmas

def verb_lemma():
    for result in results.values():
        for l in result:
            verb = l[0]
            lemma = get_lemma(verb)
            l[0] = lemma

def merge(rows):
    cols = []
    for i in range(len(rows[0])):
        l = []
        cols.append(l)

    for ind, row in enumerate(rows):
        for i in range(len(cols)):
            cols[i].append(row[i])

    new_rows = []
    for col in cols:
        new_col = list(set(col))
        new_row = [item for item in new_col if item != '']
        new_row2 = '\n'.join(new_row)
        new_rows.append(new_row2)
    return new_rows


if __name__ == "__main__":
    verb_lemma()
    for result in results:
        lemmas = [row[0] for row in results[result][1:]]
        first_row = results[result][0]
        lemmas_set = list(set(lemmas))
        all_rows = []
        all_rows.append(first_row)
        for lemma in lemmas_set:
            rows = []
            for row in results[result]:
                if row[0] == lemma:
                    print row[0], lemma
                    rows.append(row)
            lemma_merged = merge(rows)
            print 'merged ', lemma_merged
            all_rows.append(lemma_merged)
        out_csv = 'merged_srl/' + result + '.csv'
        out_p = 'merged_srl/' + result + '.p'
        write_csv_rows(out_csv, all_rows)
        pickle.dump(all_rows, open(out_p, 'wb'))
