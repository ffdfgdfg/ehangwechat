# -*- coding: utf-8 -*-
###处理被动回复部分,是由用户发送消息或请求，回复对应的消息或请求
import json
import re
from utils import DataBase
from utils import SearchServes
from utils import BaseMsg

class ReplySystem(BaseMsg.MsgBase):
    __doc__ = '''自动回复类'''
    def __init__(self, msg, *args, **kwargs):
        #这里为用户发送的消息
        self.msg = msg
        self.source = kwargs['source']
        self.time = kwargs['time']
        self.db = DataBase.MongoUtil()

    #这里为自动回复的消息
    def TextReply(self, reply):
        #回复文字消息方法
        if not isinstance(reply, str):
            try:
                reply = str(reply)
            except:
                pass
            raise TypeError('Expected a string')
        reply = super().MsgCheck(reply)
        return reply
    def ArticleReply(self, reply):
        #回复文章消息方法
        if not isinstance(reply, list) or isinstance(reply, dict):
            raise TypeError('Expected a list or dict')
        reply = super().MsgCheck(reply)
        return reply
    def MediaReply(self, reply):
        #回复媒体消息方法，包含图片，语音等等
        if not isinstance(reply, str):
            try:
                reply = str(reply)
            except:
                pass
            raise TypeError('Expected a string')
        reply = super().MsgCheck(reply)
        return reply

    def KeyWordCheck(self, key):
        if self.msg.find(key) != -1 and len(key) == len(self.msg):
            #完全对应,返回true
            return True
        elif self.msg.find(key) != -1:
            #不完全匹配，长度不对，返回false
            return False
        else:
            #完全不匹配返回None
            return None
    def MenuTraversal(self, buttons):
        for button in buttons:
            # 遍历所有的按钮
            if button.get('sub_button', default=None) is None:
                # 这是普通按钮
                type = button['type']
                name = button['name']
                key = button['key']
            else:
                # 这是下一级菜单按钮，再次遍历
                self.MenuTraversal(button['button'])
    def MenuLevel(self, *args, **kwargs):
        #菜单级别细分
        with open("menu.json") as f:
            menu_str = f.read()
            MenuDict = json.loads(menu_str)
            if 	MenuDict.get('button', default=None) is not None:
                buttons=MenuDict['button']
                self.MenuTraversal(buttons)

    def SearchProcess(self):
        #搜索对象的方法
        search=SearchServes.Serves()
        results = search.search(self.msg)
        if results is not None:
            return self.ArticleReply(results)
        else:
            return self.TextReply('已经记录消息，等待回复')

    def auth(self, *args, **kwargs):
        #预认证过程，用于改变用户类型
        #需要传入args验证类型,kwargs欢迎消息，失败消息
        if self.db.query(CollectionName='user', by='openid', openid=self.source) is None:
            # 数据表中不存在，插入数据
            self.db.insert(CollectionName='user', openid=self.source, nickname='', type=args[0])
            # 回复欢迎验证消息
            return self.TextReply(kwargs['Welcom_auth_msg'])
        elif self.db.query(CollectionName='user', by='openid', openid=self.source) is not None:
            # 数据表中存在用户
            if args[0] == 'sign':
                if self.db.query(CollectionName='signlog', by='openid', openid=self.source) is not None:
                    # 验证失败，发送失败消息
                    return self.TextReply(kwargs['Auth_fail_msg'])
                else:
                    # 改变用户状态
                    self.db.update(CollectionName='user', by='openid', openid=self.source, type=args[0])
                    # 回复欢迎验证消息
                    return self.TextReply(kwargs['Welcom_auth_msg'])
            elif args[0] == 'adminlogin':
                # 直接改变用户状态，进入下一步验证
                self.db.update(CollectionName='user', by='openid', openid=self.source, type=args[0])
                # 发送欢迎验证消息
                return self.TextReply(kwargs['Welcom_auth_msg'])
            else:
                # 验证失败，发送失败消息
                return self.TextReply(kwargs['Auth_fail_msg'])
        else:
            pass

    def SignProcess(self):
        #签到的方法
        student = re.compile(r'(QD)\+(\d{9})\+(.{2,8})')  # 匹配签到的正则表达式
        Chi = re.compile(u"([\u4e00-\u9fff]+)")  # 匹配中文的正则表达式
        match_student = student.match(self.msg)  # 匹配签到
        if match_student is not None:
            match_chinese = Chi.match(match_student.group(3))  # 匹配中文
            if match_chinese is not None:
                student_id = match_student.group(2)
                student_name = match_student.group(3)
                # 完全匹配成功
                if self.db.query(CollectionName='signlog', by='openid', openid=self.source) is None and \
                                self.db.query(CollectionName='signlog', by='student_id', student_id=student_id) is None:
                    self.db.insert(CollectionName='signlog', openid=self.source, student_id=student_id, student_name=student_name)
                    self.db.update(CollectionName='user', by='openid', openid=self.source, type='normal')
                    return self.TextReply('签到成功！')
                elif self.db.query(CollectionName='signlog', by='student_id', student_id=student_id)['student_id'] == student_id:
                    self.db.update(CollectionName='user', by='openid', openid=self.source, type='normal')
                    return self.TextReply('该学号已签到！若想签到另外的学号，请重新回复 签到')
                elif self.db.query(CollectionName='signlog', by='openid', openid=self.source)['openid'] == self.source \
                        and self.db.query(CollectionName='signlog', by='student_id', student_id=student_id)['student_id'] == student_id:
                    self.db.update(CollectionName='user', by='openid', openid=self.source, type='normal')
                    return self.TextReply('已签到成功')
            else:
                return self.TextReply('请输入中文姓名！！')
        else:
            return self.TextReply('输入格式有误，请重新输入！')

    def AdminAuthProcess(self):
        # 匹配用户名和密码
        admin = re.compile(r'(.)\+(.)')
        match_admin = admin.match(self.msg)
        if match_admin is not None:
            username = match_admin.group(1)
            password = match_admin.group(2)
        else:
            self.db.update(CollectionName='user', by='openid', openid=self.source, type='normal')
            return self.TextReply('输入格式有误,请重新回复admincp登陆')
        result = self.db.query(CollectionName='adminauth', by='username', username=username)
        if result is not None:
            # 在管理表中存在
            # 验证账号密码
            if result['password'] == password:
                self.db.update(CollectionName='adminauth', by='username', username=username, access='online')
                self.db.update(CollectionName='user', by='openid', openid=self.source, type='admin')
                return self.TextReply('登陆成功')
            else:
                self.db.update(CollectionName='user', by='openid', openid=self.source, type='normal')
                return self.TextReply('账号或密码验证失败,请重新回复admincp登陆')
    def AdminOperateProcess(self):
        #管理员操作
        from utils import ActiveOperate
        op = ActiveOperate.OperateSystem()
        if self.KeyWordCheck('更新菜单') is True:
            op.UpdateMenu()
            return self.TextReply('更新菜单成功')
        elif self.KeyWordCheck('获取菜单') is True:
            op.GetMenu()
            return self.TextReply('获取菜单成功')
        elif self.KeyWordCheck('更新素材') is True:
            op.AutoChekingMaterialProcess()
            return self.TextReply('更新素材成功')
        elif self.KeyWordCheck('导出签到') is True:
            op.ExportSignLog()
            return self.TextReply('导出签到记录成功')
        elif self.KeyWordCheck('退出') is True:
            self.db.update(CollectionName='user', by='openid', openid=self.source, type='normal')
            return self.TextReply('退出成功')

    def TextMsgProcess(self):
        #消息处理方法，用于区分用户状态，并根据输入的语句选择方法发送    处理文字消息
        # 需要先区分用户状态
        result = self.db.query(CollectionName='user', by='openid', openid=self.source)
        if result is None:
            pass
        else:
            #获取用户类型
            result = result['type']

        if result is None or result == 'normal':
            #普通状态
            # 分为特殊关键字与检索
            # 签到类型
            if self.KeyWordCheck('/h') is True or self.KeyWordCheck('/help') is True or self.KeyWordCheck('/帮助') is True:
                return self.TextReply('帮助信息')
            elif self.KeyWordCheck('签到') is True:
                return self.auth('sign', Welcom_auth_msg='请回复:QD+您的学号+姓名，例如：QD+111111111+王尼玛',
                          Auth_fail_msg='该账号已签到，请勿用同一账号签到！')
            elif self.KeyWordCheck('admincp') is True:
                return self.auth('adminlogin', Welcom_auth_msg='请输入:账号+密码用于登陆验证',
                          Auth_fail_msg='未知错误卧槽,args传入调用问题')
            # 其他文字为检索
            else:
                return self.SearchProcess()
        elif result == 'sign':
            #签到状态
            if self.KeyWordCheck('/h') is True or self.KeyWordCheck('/help') is True or self.KeyWordCheck('/帮助') is True:
                return self.TextReply('签到帮助信息')
            else:
                return self.SignProcess()
        elif result == 'adminlogin':
            #管理登陆状态
            if self.KeyWordCheck('/h') is True or self.KeyWordCheck('/help') is True or self.KeyWordCheck('/帮助') is True:
                return self.TextReply('管理登陆帮助信息')
            else:
                return self.AdminAuthProcess()
        elif result == 'admin':
            # 管理状态
            if self.KeyWordCheck('/h') is True or self.KeyWordCheck('/help') is True or self.KeyWordCheck('/帮助') is True:
                return self.TextReply('管理帮助信息')
            else:
                return self.AdminOperateProcess()
        #不满足自动回复的任何条件
        else:
            self.db.insert(CollectionName='comlog', openid=self.source, msg=self.msg, time=self.time)
            return self.TextReply("已经记录消息，等待回复")

    def ClickEventProcess(self, key):
        #点击事件被动回复方法
        #根据key来处理事件，可以回复消息，记录操作等等，貌似不影响菜单的操作
        pass

