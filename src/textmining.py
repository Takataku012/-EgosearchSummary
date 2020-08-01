import csv
import re

import MeCab
import numpy as np
from PIL import Image
from wordcloud import WordCloud

import config

# CSVの読み込み
def readCsv(fileName):
    data = []
    with open(fileName + '.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            data = data + row

    return data

# テキストの整形
def textFormat(text):
    text = re.sub(r"#(\w+)", "", text) # ハッシュタグの削除
    text = re.sub(r"@([A-Za-z0-9_]+) ", "", text) # ユーザー名の削除
    return text

# 単語抽出
def wordExtract(data):
    wordChain = ''
    for text in data:
        # MeCabの準備
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(textFormat(text))

        # 名詞抽出
        wordList = []
        while node:
            wordType = node.feature.split(',')[0]
            if (wordType == '名詞' or wordType == '形容詞') and node.surface not in config.NG_WORD:
                wordList.append(node.surface)
            node = node.next

        wordChain += ' '.join(wordList)

    return wordChain

# ワードクラウド作成
def wordCloud(data, fileName):
    W = WordCloud(width=2500, height=2500, font_path='./font/mplus-2m-bold.ttf').generate(data)
    W.to_file(fileName + '.png')
