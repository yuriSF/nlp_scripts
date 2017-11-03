from nltk import word_tokenize, sent_tokenize, pos_tag, FreqDist
from morphology import Morph
verb_tags = ['VB', 'VBD', 'VBG', 'VBP', 'VBN', 'VBZ']
noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
adj_tags = ['JJ', 'JJR', 'JJS']
adv_tags = ['RB', 'RBR', 'RBS', 'RP']


class Corpus:
    def __init__(self, text_as_string, lang):
        self.text_as_string = text_as_string
        self.lang = lang
        self.sents = None
        self.tokens = None
        self.tokens_in_sents = None
        self.vectors = None
        self.tags = []
        self.lemmatized_tags = []

    def replace_newline(self):
        self.text_as_string = self.text_as_string.replace('\n', '. ')
        return self.text_as_string

    def tokenize_words(self):
        tokens = word_tokenize(self.text_as_string, language=self.lang)
        self.tokens = [token.lower() for token in tokens]
        return self.tokens

    def sentencize(self):
        if '\n' in self.text_as_string:
            paras = [sent_tokenize(p) for p in self.text_as_string.split('\n') if p]
            self.sents = [p for subparas in paras for p in subparas]
        else:
            self.sents = sent_tokenize(self.text_as_string, language=self.lang)
        return self.sents

    def flatten_sents_to_tokens(self):
        # this method flattens sents into one array of tokens
        self.tokens = []
        for sent in self.sents:
            sent_tokens = word_tokenize(sent)
            sent_tokens_lower = [token.lower() for token in sent_tokens]
            self.tokens.extend(sent_tokens_lower)
        return self.tokens

    def query_characters(self, query):
        self.sentencize()
        hits = []
        for ind, sentence in enumerate(self.sents):
            if query in sentence:
                target = '\n' + sentence + '\n'
                #target = target.replace(query, query.upper())
                hits.append(target)
        return hits

    def tokenize_within_sents(self):
        # this method tokenizes sents while keeping original sentence boundaries
        self.tokens_in_sents = [word_tokenize(sentence) for sentence in self.sents]
        return self.tokens_in_sents

    def vectorize_sents(self):
        from gensim.models import Word2Vec as wv
        self.sentencize()
        self.tokenize_sents()
        self.vectors = wv(self.tokenized_sents)
        return

    def find_similar(self, word, threshold=0.7):
        from gensim.models import Word2Vec as wv
        self.vectorize_sents()
        all_hits = self.vectors.most_similar(word, topn=100)
        filtered_hits = [hit for hit in all_hits if hit[1] > threshold]
        return filtered_hits

    def calc_freq(self):
        fdist_list = []
        if self.tokens != None:
            fdist = FreqDist(self.tokens)
            for key in fdist:
                row = (key, fdist[key])
                fdist_list.append(row)
            sorted_freq_dist = sorted(fdist_list, key=lambda x: x[1], reverse=True)
            return sorted_freq_dist
        else:
            return 'no tokens have been supplied'

    def calc_freq_by_pos(self, tokens):
        fdist_list = []
        fdist = FreqDist(tokens)
        for key in fdist:
            row = (key, fdist[key])
            fdist_list.append(row)
        sorted_freq_dist = sorted(fdist_list, key=lambda x: x[1], reverse=True)
        return sorted_freq_dist

    def tag(self):
        # sentences are flattened into an array
        for sent in self.tokens_in_sents:
            tagged_sent = pos_tag(sent)
            self.tags.extend(tagged_sent)
        return self.tags

    def filter_tokens_by_pos(self, tags, tag_list):
        filtered_list = []
        for tag in tags:
            if tag[1] in tag_list:
                filtered_list.append(tag[0].lower())
        return filtered_list

    def lemmatize(self):
        for tag in self.tags:
            try:
                word = Morph(tag[0])
                print tag[0]
                if tag[1] in verb_tags:
                    lemma = word.lemmatize_verb()
                elif tag[1] in noun_tags:
                    lemma = word.lemmatize_noun()
                elif tag[1] in adj_tags:
                    lemma = word.lemmatize_noun()
                elif tag[1] in adv_tags:
                    lemma = word.lemmatize_noun()
                else:
                    lemma = tag[0]
                new_tag = (lemma, tag[1])
                self.lemmatized_tags.append(new_tag)
            except UnicodeDecodeError:
                new_tag = tag
        return

class SentCorpus(Corpus):
    def __init__(self, sents_as_lines, lang):
        self.lang = lang
        self.sents = sents_as_lines
        self.tokens = None
        self.tokens_in_sents = None
        self.vectors = None
        self.tags = []
        self.lemmatized_tags = []
        self.vectorized_corpus = []
        self.text_as_string = " ".join(self.sents)

    def vectorize_sents(self):
        from gensim.models import Word2Vec as wv
        self.tokenize_within_sents()
        self.vectors = wv(self.tokens_in_sents)
        return

    def get_wv_vector(self, word):
        from gensim.models import Word2Vec as wv
        return self.vectors[word]

    def vectorize_sent(self, sent_tokens):
        vecs = []
        for token in sent_tokens:
            print token
            vec = self.get_wv_vector(token.lower())
            vecs.append(vec)
            print vec
        return(vecs)

    def vectorize_corpus(self):
        for sent in self.tokens_in_sents[0:20]:
            try:
                sent_vector = self.vectorize_sent(sent)
                self.vectorized_corpus.append(sent_vector)
            except:
                pass
        return
