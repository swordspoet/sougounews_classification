# coding: utf-8

import os
import sys
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, metrics
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegressionCV, SGDClassifier
from sklearn.naive_bayes import MultinomialNB


def read_file(file_name):
    contents, categories = [], []
    with open(file_name) as f:
        for line in f:
            try:
                category, content = line.strip().split('\t')
                contents.append(content)
                categories.append(category)
            except:
                pass

    return contents, categories


def tf_idf(contents):
    """提取文本特征tf-idf"""
    vectorizer = CountVectorizer(min_df=1e-5)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(contents))
    return tfidf


def cat_to_id(categories):
    """给类别编码"""
    encoder = preprocessing.LabelEncoder()
    encode_category = encoder.fit_transform(categories)
    return encode_category


def process_file(dir_name):
    """全量数据"""
    corpus_set, categories = [], []
    for file in os.listdir(dir_name):
        if file.endswith('txt'):
            file_path = os.path.join(dir_name, file)
            contents, labels = read_file(file_path)
            corpus_set += contents
            categories += labels
    return corpus_set, categories


def prepare_ttv(dir_name):
    """准备训练、验证和测试数据"""
    corpus_set, categories = process_file(dir_name)
    x = tf_idf(corpus_set)
    y = cat_to_id(categories)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0, random_state=1212)
    return x_train, y_train, x_test, y_test


def lr_model():
    # logistic regression
    print('Training logistic regression model...')
    lr_model = LogisticRegressionCV(solver='newton-cg', multi_class='multinomial', cv=10, n_jobs=-1)
    lr_model.fit(x[:20000], y[:20000])
    y_pred = lr_model.predict(x[20000:24000])
    print(metrics.confusion_matrix(y[20000:24000], y_pred))
    print(classification_report(y[20000:24000], y_pred, target_names=['business', 'sports', 'news', 'yule']))


def svm_model():
    # 线性支持向量机
    svm_model = SGDClassifier(n_jobs=-1)
    svm_model.fit(x[:20000], y[:20000])

    y_pred = svm_model.predict(x[20000:24000])
    print(metrics.confusion_matrix(y[20000:24000], y_pred))
    print(classification_report(y[20000:24000], y_pred, target_names=['business', 'sports', 'news', 'yule']))


def nb_model():
    # 朴素贝叶斯
    by_model = MultinomialNB()
    by_model.fit(x[:20000], y[:20000])

    y_pred = by_model.predict(x[20000:24000])
    print(metrics.confusion_matrix(y[20000:24000], y_pred))
    print(classification_report(y[20000:24000], y_pred, target_names=['business', 'sports', 'news', 'yule']))


if __name__ == '__main__':
    x, y, _, _ = prepare_ttv('/home/libin/ml-project/text_classification/data/')

    if len(sys.argv) != 2 or sys.argv[1] not in ['svm', 'lr', 'nb']:
        raise ValueError("""please use: python run.py [svm / lr / nb]""")

    if sys.argv[1] == 'svm':
        svm_model()
    elif sys.argv[1] == 'lr':
        lr_model()
    else:
        nb_model()