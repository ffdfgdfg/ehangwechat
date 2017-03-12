# -*- coding: utf-8 -*-
import json
from utils import SearchServes

articledic = {
    'item_count': 2,
    'total_count': 2,
    'item':[
        {
            'content':{
                'news_item':[
                    {
                        'thumb_media_id': 'KyA0LE5sGj2s2sIOuHeh7sQUuxu15rYkO3iH3tqM6Qw',
                        'content': '测试号真tm不好用',
                        'url': 'http://mp.weixin.qq.com/s?__biz=MzIwNDI1OTA4NQ==&mid=100000006&idx=1&sn=37b5ecfa5eb4099c43048ef1a8c199cf&chksm=16c3ab6421b4227292c9cac75e7e8d2ab46b4c3be21c18c71f3911356bb074a73ab7b96c3b79#rd',
                        'show_cover_pic': 1,
                        'title': '文章测试233',
                        'content_source_url': '',
                        'author': 'test',
                        'digest': '卧槽成功了',
                        'thumb_url': 'http://mmbiz.qpic.cn/mmbiz_png/zElfHMRc6cVUxcOfnSYT7DazJ1iaFfopuSlFgFOPzAbQPEoTxakXSq9u8UvVfRL8IbM2VtgtjYos6ssnAJwkguQ/0?wx_fmt=png'
                    }
                ],
                'create_time': 1489261108,
                'update_time': 1489261108
            },
        'update_time': 1489261108,
        'media_id': 'KyA0LE5sGj2s2sIOuHeh7oy66AKFYmXtSGMNxBbVQL0'
        },
        {
            'content':{
                'news_item':[
                    {
                        'thumb_media_id': 'KyA0LE5sGj2s2sIOuHeh7p2L88ikdKG2DH_qcBIGBJo',
                        'content': '测试号真tm不好用',
                        'url': 'http://mp.weixin.qq.com/s?__biz=MzIwNDI1OTA4NQ==&mid=100000003&idx=1&sn=c06eb8b9ed392fc8c030b75ab46167fd&chksm=16c3ab6121b422774c560bd8adeb5f2df61f540e8c4c5966f399b7eda92c924d38c0121c0eda#rd',
                        'show_cover_pic': 0,
                        'title': '文章测试',
                        'content_source_url': '',
                        'author': 'test',
                        'digest': '这是一个测试',
                        'thumb_url': 'http://mmbiz.qpic.cn/mmbiz_jpg/zElfHMRc6cVUxcOfnSYT7DazJ1iaFfopud29D1hrib2YqBsicHSiaFVWv038clXQJcdtEE38iayVwb7zKAthEXibcJVQ/0?wx_fmt=jpeg'
                    }
                ],
                'create_time': 1489260655,
                'update_time': 1489260655},
        'update_time': 1489260655,
        'media_id': 'KyA0LE5sGj2s2sIOuHeh7knpdUALP3Vl6N0f_N-lDvc'
        }
    ]
}

addser = SearchServes.Serves()
'''
items = articledic['item']
for item in items:
    #这才是内容的dict
    media_id = item['media_id']
    content = item['content']
    news_items = content['news_item']
    for news_item in news_items:
        #文章的dict
        title = news_item['title']
        description = news_item['digest']
        url = news_item['url']
        thumb_url = news_item['thumb_url']
        addser.AddIndex(news_item)
    print('添加记录成功！')
'''

print(addser.search('测试'))
