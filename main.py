from libs.func import ConsoleAction
helpmsg='''
控制台帮助
-----------------------------------
help 显示帮助
downloadskin 下载皮肤
getuuid 获取玩家uuid(支持盗版、正版)
downloadclient 下载Minecraft客户端client.jar文件
downloadjson 下载Minecraft客户端client.json文件
downloadserver 下载Minecraft服务端server.jar文件
getnames 以UUID获取玩家的名称、历史名称(仅支持正版)
-----------------------------------
'''
def command(userdo):
    ca=ConsoleAction(userdo)
    if userdo == 'stop':
        ca.stop()
    elif userdo == 'downloadskin':
        ca.downloadskin()
    elif userdo == 'getuuid':
        ca.getuuid()
    elif userdo == 'help':
        print(helpmsg)
    elif userdo == 'downloadclient':
        ca.downloadmc('client.jar')
    elif userdo == 'downloadjson':
        ca.downloadmc('json')
    elif userdo == 'downloadserver':
        ca.downloadmc('server.jar')
    elif userdo == 'getnames':
        ca.getnames()
    else:
        print('指令错误')
        return
#初始化
print('欢迎使用MinecraftHelper，使用指令help获得帮助')
while True:
    print('')
    userdo = input('>')
    command(userdo)
    if userdo == 'stop':
        break
