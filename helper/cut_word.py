# coding: utf-8


import jieba


stopwords_path = 'stopwords.txt'


class CutWord(object):
    def __init__(self, stopwords_path=stopwords_path):
        self.stopwords_path = stopwords_path

    def add_dictionary(self, dict_list):
        map(lambda x: jieba.load_userdict(x), dict_list)

    def seg_sentence(self, sentence, stopwords_path=None):
        if not stopwords_path:
            stopwords_path = self.stopwords_path

        def stopwords_list(file_path):
            stopwords = [line.strip() for line in open(file_path, 'r').readlines()]
            return stopwords

        segmented_sentence = jieba.cut(sentence.strip())
        stopwords_list = stopwords_list(stopwords_path)
        out_str = ''

        for word in segmented_sentence:
            if word not in stopwords_list:
                out_str += word
                out_str += ' '
        return out_str
