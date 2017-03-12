from utils import ActiveOperate
op = ActiveOperate.OperateSystem()
print('上传图片')
dic = op.UploadPic('logo.png')
url = dic['url']
media_id = dic['media_id']
print('上传文章')
article_media_id = op.AddArticle(media_id)
print(article_media_id)
#"thumb_media_id": "KyA0LE5sGj2s2sIOuHeh7p2L88ikdKG2DH_qcBIGBJo"
#{'media_id': 'KyA0LE5sGj2s2sIOuHeh7knpdUALP3Vl6N0f_N-lDvc'}