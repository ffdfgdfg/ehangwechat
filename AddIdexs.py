# -*- coding: utf-8 -*-
import json
from utils import SearchServes

addser = SearchServes.Serves()
with open("indexs.json") as f:
    index_str = f.read()
    articles = json.loads(index_str)
    for article in articles:
        media_id = article['media_id']
        news_items = article['content']['news_item']
        for news_item in news_items:
            addser.AddIndex(news_item)
    print('添加记录成功！')