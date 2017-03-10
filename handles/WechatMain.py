# coding=utf-8

import tornado.escape
import tornado.web
from wechatpy.utils import check_signature
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.replies import create_reply
from wechatpy.replies import EmptyReply
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
import config
from utils import PassiveReply
from utils import DataBase



class wechat(tornado.web.RequestHandler):
    def Wechat_msg_Process(self, body, **kwargs):
        #消息预处理方法，主要依靠消息类型，分别调用不同方法
        if isinstance(body.type, 'text'):
            content = body.content  # 消息内容
            #消息内容用于实例化自动回复类
            auto_reply = PassiveReply.ReplySystem(content, source=body.source)
            if len(body.content.replace(' ', '')) == 0:
                return None
            reply = auto_reply.TextMsgProcess()
            return reply
        elif isinstance(body.type, 'image'):
            picurl = body.image                     # PicUrl
            media_id = body.media_id                 # MediaId
        elif isinstance(body.type, 'voice'):
            media_id = body.media_id                 # MediaId
            format = body.format                     # Format
            recognition = body.recognition           # Recognition
        elif isinstance(body.type, 'video') or isinstance(body.type, 'shortvideo'):
            media_id = body.media_id                 # MediaId
            thumb_media_id = body.thumb_media_id     # ThumbMediaId
        elif isinstance(body.type, 'location'):  # location
            location_x = body.location_x  # 地理位置纬度
            location_y = body.location_y  # 地理位置经度
            scale = body.scale  # 地图缩放大小
            label = body.label  # 地理位置信息
            location = body.location  # (纬度, 经度) 元组
        elif isinstance(body.type, 'link'):
            title = body.title  # 链接标题
            description = body.description  # 链接描述
            url = body.url  # 链接地址

        #事件类型预处理
        elif isinstance(body.type, 'event'):
            if isinstance(body.event, 'subscribe'):  # subscribe
                return '欢迎关注'
            elif isinstance(body.event, 'unsubscribe'):  # unsubscribe
                db=DataBase.MongoUtil()
                db.delete(CollectionName='user', by='openid', openid=body.source)
                return '再见'
            elif isinstance(body.event, 'subscribe_scan'): # 未关注用户扫描带参数二维码事件
                scene_id = body.scene_id  # 带参数二维码 scene_id，去除了前缀 qrscene_
                ticket = body.ticket  # 带参数二维码 ticket
            elif isinstance(body.event, 'scan'):  # 已关注用户扫描带参数二维码事件
                scene_id = body.scene_id              # 带参数二维码 scene_id
                ticket = body.ticket                  # 带参数二维码 ticket
            elif isinstance(body.event, 'location'):  # 上报地理位置事件
                latitude = body.latitude              # 地理位置纬度
                longitude = body.longitude            # 地理位置经度
                precision = body.precision            # 地理位置精度
            elif isinstance(body.event, 'click'):  # 点击菜单拉取消息事件
                key = body.key                       # 自定义菜单 key 值

                auto_reply = PassiveReply.ReplySystem(body.content)
                auto_reply.ClickEventProcess(key)
            elif isinstance(body.event, 'view'):  # 点击菜单跳转链接事件
                url = body.url                        # 跳转链接 url
                return url
            elif isinstance(body.event, 'templatesendjobfinish'):  # 模板消息发送任务完成事件
                status = body.status                  # 模板消息发送状态
            elif isinstance(body.event, 'scancode_push'):  # 扫码推事件
                key = body.key  # 自定义菜单 key
                scan_type = body.scan_type  # 扫描类型
                scan_result = body.scan_result	# 扫描结果
            elif isinstance(body.event, 'scancode_waitmsg'):  # 扫码推事件且弹出“消息接收中”提示框
                key = body.key  # 自定义菜单 key
                scan_type = body.scan_type  # 扫描类型
                scan_result = body.scan_result	# 扫描结果
            elif isinstance(body.event, 'pic_sysphoto'):  # 弹出系统拍照发图事件
                key = body.key  # 自定义菜单 key
                count = body.count  # 发送的图片数量
                pictures = body.pictures  # 图片列表
            elif isinstance(body.event, 'pic_photo_or_album'):  # 弹出拍照或者相册发图事件
                key = body.key  # 自定义菜单 key
                count = body.count  # 发送的图片数量
                pictures = body.pictures  # 图片列表
            elif isinstance(body.event, 'pic_weixin'):  # 弹出微信相册发图器事件
                key = body.key  # 自定义菜单 key
                count = body.count  # 发送的图片数量
                pictures = body.pictures  # 图片列表
            elif isinstance(body.event, 'location_select'):  # 弹出地理位置选择器事件
                key = body.key  # 自定义菜单 key
                location_x = body.location_x  # 地理位置纬度
                location_y = body.location_y  # 地理位置经度
                scale = body.scale  # 地理位置精度
                label = body.label  # 地理位置信息
                location = body.location  # (纬度, 经度) 元组
                poiname = body.poiname  # 朋友圈 POI 的名字，可能为空
            else:
                # 微信认证事件推送
                # 微信扫一扫事件
                # 太多了，而且不知道有什么用
                pass

        return '知道了'

    def get(self):
        '''tornado 处理get请求方法'''
        # 解析http封包包头信息
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        echostr = self.get_argument('echostr', 'default')
        #get方式验证
        if signature != 'default' and timestamp != 'default' and nonce != 'default' and echostr != 'default' \
                and check_signature(config.token, signature, timestamp, nonce):
            self.write(echostr)
        # 处理其他莫名其妙的get请求。。。。
        else:
            self.write('Page Not Available')

    def post(self):
        '''tornado 处理post请求方法'''
        #解析http封包包头信息
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        # 检测是不是微信服务器发送的封包
        if signature != 'default' and timestamp != 'default' and nonce != 'default' \
                and check_signature(config.token, signature, timestamp, nonce):
            #解析http封包包体
            body = self.request.body.decode('utf-8') # 由utf-8转化为unicode为解码decode，反之为encode

            # 解析明文xml消息
            if config.encrypt_mode == 'normal':
                msg = parse_message(body)
            # 解析加密xml消息
            elif config.encrypt_mode == 'aes':
                crypto = WeChatCrypto(config.token, config.encoding_aes_key, config.appid)
                try:
                    decrypted_xml = crypto.decrypt_message(
                        body,
                        signature,
                        timestamp,
                        nonce
                    )
                    msg = parse_message(decrypted_xml)
                except (InvalidAppIdException, InvalidSignatureException):
                    print('InvalidAppIdException, InvalidSignatureException)')
                    msg = None
            else:
                msg = None
                print('Wrong encrypt mode')

            #消息处理后结果回复
            try:
                id = msg.id  # 消息 id, 64 位整型。
                target = msg.target  # 消息的目标用户
                source = msg.source  # 消息的来源用户，即发送消息的用户。
                time = msg.time  # 消息的发送时间，UNIX 时间戳
                type = msg.type  # 消息的类型
                if isinstance(type, 'event'): #事件类型分类
                    event = msg.event
                ReplyContent = self.Wechat_msg_Process(msg)
                if ReplyContent is not None:
                    # 消息处理为xml
                    result=create_reply(ReplyContent, message=msg)
                    xml = result.render()
                    #是否加密xml
                    if config.encrypt_mode == 'normal':
                        self.write(xml)
                    elif config.encrypt_mode == 'aes':
                        crypto = WeChatCrypto(config.token, config.encoding_aes_key, config.appid)
                        encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
                        self.write(encrypted_xml)
                    else:
                        print('Wrong encrypt mode')
                else:
                    self.write(EmptyReply)
            except (IOError):
                return IOError
        #处理其他莫名其妙的post请求。。。。
        else:
            self.write('Page Not Available')

