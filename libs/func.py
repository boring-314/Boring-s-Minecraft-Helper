from typing import Counter
import requests
import json
import re
import base64
import os
import time
class ConsoleAction():
    def __init__(self, userdo):
        self.userdo = userdo
    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    def stop(self):
        print('感谢使用本工具,goodbye。')
    def the_resolution_time(self,timestamp):
        timestamp/=1000
        time_local = time.localtime(timestamp)
        dt = time.strftime('%Y-%m-%d %H:%M:%S', time_local)
        return dt
    def check_the_ver(self,ver):
        version_manifest = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
        versionlist=[]
        for i in version_manifest['versions']:
            versionlist.append(i['id'])
        return ver in versionlist
    def input_username(self, action_name):
        while True:
            username = input(f'[{action_name}] 输入用户名>>>')
            error = False
            if len(username) <= 3 or len(username) > 16:
                print(f'[{action_name}] 你输入的名字过短/过长了')
                error = True
            if not re.match('^[0-9a-zA-Z_]+$', username):
                print(f'[{action_name}] 你输入的名字格式有误，必须要以字母、数字、下划线组成')
                error = True
            if error:
                continue
            else:
                break
        return username
    def split_uuid(self,uuid):
        splitted=[]
        splitted.append(uuid[0:8])
        splitted.append(uuid[8:12])
        splitted.append(uuid[12:16])
        splitted.append(uuid[16:20])
        splitted.append(uuid[20:32])
        splitted_uuid = '-'.join(splitted)
        return splitted_uuid
    def downloadskin(self, username=None):
        if username is None:
            username = self.input_username('皮肤下载')
        self.mkdir('./download')
        with open('./download/skin.png', 'wb') as img:
            img.write(
                requests.get(
                    json.loads(
                        base64.b64decode(
                            requests.get(
                                'https://sessionserver.mojang.com/session/minecraft/profile/{}'.format(
                                    requests.get(
                                        'https://api.mojang.com/users/profiles/minecraft/{}'.format(
                                            username)
                                    ).json()['id']
                                )
                            ).json()['properties'][0]['value']
                        )
                    )['textures']['SKIN']['url']
                ).content
            )
        print('[皮肤下载] 下载完毕，保存于./download/skin.png中')

    def getuuid(self, username=None, mode=None):
        uuid = '0'
        splited_uuid = '0'
        if username is None:
            username = self.input_username('UUID')
        if mode is None:
            while True:
                mode = input(
                    '[UUID] 请输入获取模式\nonline -在线模式(正版)\noffline -离线模式(盗版)\n>>>')
                print(mode)
                error = False
                if mode != 'online' and mode != 'offline':
                    print('[UUID] 输的什么玩意儿?')
                    error = True
                if error:
                    continue
                else:
                    break
        if mode == 'online':
            
            try:
                uuid=requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()['id']
                splited_uuid = self.split_uuid(uuid)
            except:
                pass
        elif mode == 'offline':
            try:
                uuid = requests.get(f'http://tools.glowingmines.eu/convertor/nick/{username}').json()['offlineuuid']
                splited_uuid = requests.get(f'http://tools.glowingmines.eu/convertor/nick/{username}').json()['offlinesplitteduuid']
            except:
                pass
        print('[UUID] 获取成功')
        print('[UUID] 标准UUID:'+ uuid)
        print('[UUID] 带连字符的UUID:'+ splited_uuid)
    def downloadmc(self, type, version=None):
        while True:
            if version is None:
                version = input('[游戏文件] 请输入要获取的版本号\n>>>')
                if self.check_the_ver(version):
                    break
                else:
                    version = None
                    print('[游戏文件] 您输入的版本号无法获取！')
                    continue
            elif self.check_the_ver(version):
                break
            else:
                print('[游戏文件] 您输入的版本号无法获取！')
                version = None
                continue
        version_manifest=requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
        for i in version_manifest['versions']:
            if i['id'] == version:
                json_url = i['url']
                break
        if type == 'json':
            file_name = 'client.json'
            file_url = json_url
        elif type == 'client.jar':
            file_name = 'client.jar'
            file_url = requests.get(json_url).json()['downloads']['client']['url']
        elif type == 'server.jar':
            file_name = 'server.jar'
            file_url = requests.get(json_url).json()['downloads']['server']['url']
        self.mkdir(f'./download/{version}')
        with open(f'./download/{version}/{file_name}','wb') as file:
            file.write(requests.get(file_url).content)
        print(f'[游戏文件] 下载完毕,保存于./download/{version}/{file_name}')
    def getnames(self,uuid=None):
        if uuid is None:
            uuid = input('[用户名] 请输入UUID(无连字符)\n>>>')
        names = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names').json()
        num = 0
        for i in names:
            if num == 0:
                i['time']='未知'
                num+=1
            else:
                i['time']=self.the_resolution_time(i['changedToAt'])
        print('---用户名列表---')
        print('格式:名称 - 更改时间 - 序号')
        print('----------------------现用名------------------------')
        print(f"{names[-1]['name']} - {names[-1]['time']} - {names.index(names[-1])+1}")
        print('----------------------所有名称------------------------')
        for i in range(len(names)):
            t = i+1
            print(f"{names[i]['name']} - {names[i]['time']} - {t}")
            