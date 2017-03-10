#主动操作部分，主要为更新、获取菜单，获取素材,获取用户信息等
from wechatpy import WeChatClient
import json
import config
from utils import DataBase
from utils import SearchServes

class OperateSystem:
    def __init__(self):
        # 实例化client类
        self.client = WeChatClient(config.appid, config.appsecret)
        # 实例化database类
        self.db = DataBase.DBcontrol()

    def GetUserInformation(self, openid, *args, **kwargs):
        #获取用户信息
        userdict = json.load(self.client.user.get(openid, lang=u'zh_CN'))
        nickname=userdict['nickname']
        sex=userdict['sex']
        language=userdict['language']
        city=userdict['city']
        province=userdict['province']
        country=userdict['country']
        headimgurl=userdict['headimgurl']
        subscribe_time=userdict['subscribe_time']
        unionid=userdict['unionid']
        remark=userdict['remark']
        groupid=userdict['groupid']
        if args == 'get' and kwargs is not None:
            return exec(kwargs['GetWhat'])
        elif args == 'update' and kwargs is not None:
            if kwargs['UpdateWhat'] == 'nickname':
                self.db.update(tablename='user', by='openid', how='nickname', openid=openid, nickname=nickname)
                return 'Update Success'
            else:
                raise AttributeError
        else:
            pass

    def GetMaterial(self, *args, **kwargs):
        #获取素材
        count = self.client.material.get_count()
        if self.db.query(tablename='oplog', by='materialcount',materialcount=count) is None:
            HavingMaterial=self.db.query(tablename='oplog', by='id', id=1).materialcount
            ArticlesDic = json.loads(self.client.api.WeChatMaterial.batchget('news', offset=HavingMaterial, count=20))
            articles = ArticlesDic['item']
            add=SearchServes.Serves()
            for article in articles:
                add.AddIndex(article)
                self.db.update(tablename='oplog', by='id', how='materialcount', id=1, materialcount=HavingMaterial+1)

    def GetMenu(self, *args, **kwargs):
        #获取当前菜单
        menu = self.client.menu.get()
        JsonMenu = json.dumps(menu)
        with open("menu.json", 'w+') as f:
            f.write(JsonMenu)

    def UpdateMenu(self, *args, **kwargs):
        #更新菜单
        with open("menu.json") as f:
            menu_str = f.read()
            js = json.loads(menu_str)
            self.client.menu.delete()
            self.client.menu.create(js)

    def AutoChekingMaterialProcess(self, *args, **kwargs):
        #检测更新素材,任务计划是在tornado的ioloop里面
        import time
        LocalTime = int(time.time())
        self.GetMaterial()
        self.db.update(tablename='oplog', by='id', how='materialuptime', id=1, materialuptime=LocalTime)
        print('Update materials in %s' % (time.asctime(time.localtime(LocalTime))))

