from nltk import stem
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, sent_tokenize
from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()
from gensim.models import Word2Vec as wv

class Morph:
    def __init__(self, word):
        self.word = word

    def lemmatize_verb(self):
        return stem.WordNetLemmatizer().lemmatize(self.word, 'v').lower()

    def lemmatize_noun(self):
        return stem.WordNetLemmatizer().lemmatize(self.word, 'n').lower()

    def lemmatize_adj(self):
        return stem.WordNetLemmatizer().lemmatize(self.word, 'a').lower()

    def lemmatize_adv(self):
        return stem.WordNetLemmatizer().lemmatize(self.word, 'r').lower()

    def lemmatize_particleVerb(self):
        if ' ' in self.word:
            spl = self.word.split(' ')
            verb_proper, part = spl[0].lower(), spl[1].lower()
            lemma = stem.WordNetLemmatizer().lemmatize(verb_proper, 'v').lower()
            return lemma + ' ' + spl[1]
        return None

    def get_synset(self):
        return wn.synsets(self.word)

    def pos_list(self):
        sn = wn.synsets(self.word)
        return [item.pos() for item in sn]

    def similar_word(self, second_word):
        return wns.word_similarity(self.word, second_word, 'lin')

    def similar_list(self, word_list, sim_threshold):
        temp = []
        temp.append(self.word)
        for second_word in word_list:
            sim = wns.word_similarity(self.word, second_word, 'lin')
            if sim > sim_threshold:
                print 'similarity ratio: ', sim
                temp.append(second_word)
        return set(temp)

    def similar_word_wv(self, sents):
        return wv(sents)


if __name__ == "__main__":
    pos_tags = Morph('stonehurst').pos_list()
    if (pos_tags and 'v' not in pos_tags) or (not pos_tags):
        print True
