from corpus import *
from nltk import FreqDist

class Frequency(SentCorpus):
    def __init__(self, sent_as_lines, lang):
        SentCorpus.__init__(self, sent_as_lines, lang)
        self.sorted_freq = None

    def get_freq_dist(self):
        l = []
        # print('text_as_string')
        # print(self.text_as_string)
        self.tokenize_within_sents()
        self.flatten_sents_to_tokens()
        freq_dist = FreqDist(self.tokens)
        for key in freq_dist:
            print(key, freq_dist[key])
            row = [key, freq_dist[key]]
            l.append(row)
        self.sorted_freq = sorted(l, key=lambda x: x[1], reverse=True)
        for ind, row in enumerate(self.sorted_freq):
            row.append(ind)
        return self.sorted_freq
