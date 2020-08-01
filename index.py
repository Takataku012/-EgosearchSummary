#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as dt

from src import twitter
from src import textmining as tm
import config

def main():
    # 日付の設定 (デフォルト昨日に設定)
    day = str(dt.date.today() - dt.timedelta(days=1))
    fileName = './output/' + day

    # ツイート取得
    tweetData = twitter.getTweet(day)
    twitter.writeCsv(fileName, tweetData)

    # ワードクラウド作成
    tm.wordCloud(tm.wordExtract(tm.readCsv(fileName)), fileName)


if __name__ == '__main__':
    main()
