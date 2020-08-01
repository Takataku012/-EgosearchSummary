import csv
import json
import re

import emoji
from requests_oauthlib import OAuth1Session

import config

# テキストの整形
def textFormat(text):
    text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI) # 絵文字の削除
    text = text.replace('\n','') # 改行の削除
    text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" , text) # テキスト内のURL削除
    return text

# ツイート取得
def getTweet(day):
    # API_Keyの設定
    CK = config.TWITTER_API['CONSUMER_KEY']
    CS = config.TWITTER_API['CONSUMER_SECRET']
    AT = config.TWITTER_API['ACCESS_TOKEN']
    AS = config.TWITTER_API['ACCESS_SECRET']
    twitter = OAuth1Session(CK, CS, AT, AS)

    # ツイート取得のリクエスト
    tweetData = []
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    for i in range(24):
        hour = str(i).zfill(2)
        time = ' since:'+day+'_'+hour+':00:00_JST until:'+day+'_'+hour+':59:59_JST'
        params = {
            'count' : 100,
            'q'     : config.KEYWORD + time
            }

        req = twitter.get(url, params = params)
        if req.status_code == 200:
            res = json.loads(req.text)
            for line in res['statuses']:
                tweetData.append([textFormat(line['text'])])
        else:
            print("Failed: %d" % req.status_code)

    return tweetData

# CSVの書き出し
def writeCsv(fileName, tweetData):
    with open(fileName + '.csv', 'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["text"])
        writer.writerows(tweetData)
    pass
