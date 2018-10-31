#!/usr/bin/python
# coding: utf-8

import os
import re


def _read_file(txt_file):
    """读取txt文件"""
    return open(txt_file, 'rb').read().decode("gbk", 'ignore')


def extract_class_content(doc):
    """提取分类和内容"""
    url = doc.split('<url>')[1].split('</url>')[0]
    content = doc.split('<content>')[1].split('</content>')[0]
    category = re.findall(r"http://(.*?).sohu.com/", url)
    return category[0], content


def file_writer(category, content):
    dir_name = '/home/libin/data/'
    path = os.path.join(dir_name, category)
    f = open(path, 'a', encoding='utf-8')
    f.write(category + '\t' + content + '\n')
    f.close()


def category_data(txt_file):
    """将每个文件中不同类别的新闻分别存储"""
    f = _read_file(txt_file)
    docs_xmls = f.split('<doc>\n')
    for doc in docs_xmls:
        if doc:
            category, content = extract_class_content(doc)
            file_writer(category, content)


if __name__ == '__main__':
    for file in os.listdir('/home/libin/data/SogouCS.reduced/'):
        file_path = os.path.join('/home/libin/data/SogouCS.reduced', file)
        category_data(file_path)
