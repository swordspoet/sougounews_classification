#!/usr/bin/python
# coding: utf-8

import os
from cut_word import CutWord
from multiprocessing import Pool


CutWord = CutWord()
global CutWord


def _read_file(file):
    f = open(file).readlines()
    return f


def _unpack_line(line):
    category, content = line.strip('\n').split('\t')
    return category, content


def save_file(dir_name):
    # 按照 4:0.4:1 从分类数据中提取训练集、验证集和测试集
    f_train = open('../data/news_train.txt', 'w', encoding='utf-8')
    f_test = open('../data/news_test.txt', 'w', encoding='utf-8')
    f_val = open('../data/news_val.txt', 'w', encoding='utf-8')
    # for category in os.listdir(dir_name):
    for category in ['business', 'sports', 'news', 'yule']:  # 取4个类别的数据
        cat_file = os.path.join(dir_name, category)
        fp = _read_file(cat_file)
        count = 0
        for line in fp:
            category, content = _unpack_line(line)
            if category and content:
                if count < 5000:
                    f_train.write(category + '\t' + content + '\n')
                elif count < 6000:
                    f_test.write(category + '\t' + content + '\n')
                elif count < 6500:
                    f_val.write(category + '\t' + content + '\n')
                else:
                    break
                count += 1

        print('Finished', category, count)

    f_train.close()
    f_test.close()
    f_val.close()


def seg_file(paths):
    """文件分词"""
    file_path, write_path = paths
    with open(write_path, 'w') as w:
        fp = _read_file(file_path)
        count = 0
        for line in fp:
            category, content = _unpack_line(line)
            content = CutWord.seg_sentence(content)
            if category and content:
                w.write(category + '\t' + content + '\n')
            count += 1

    print('Word segment finished', category, count)


if __name__ == '__main__':
    raw_file_dir = '/home/libin/data/sougounews'  # 原始数据文件
    seg_file_dir = '/home/libin/data/seged_sougounews'  # 分词数据存储路径
    file_list = [os.path.join(raw_file_dir, file_name) for file_name in os.listdir(raw_file_dir)]
    write_list = [os.path.join(seg_file_dir, file_name) for file_name in os.listdir(seg_file_dir)]

    # 多进程分词
    pool = Pool(processes=6)
    for file_path, write_path in zip(file_list, write_list):
        paths = [file_path, write_path]
        pool.apply_async(seg_file, (paths,))
    pool.close()
    pool.join()
    print('Word segment finished...')

    save_file(seg_file_dir)
    print(len(open('../data/news_train.txt', 'r', encoding='utf-8').readlines()))
    print(len(open('../data/news_test.txt', 'r', encoding='utf-8').readlines()))
    print(len(open('../data/news_val.txt', 'r', encoding='utf-8').readlines()))
