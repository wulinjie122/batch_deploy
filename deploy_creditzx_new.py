import logging
from logging.handlers import RotatingFileHandler

import pexpect
import simplejson as json
from pexpect.popen_spawn import PopenSpawn
from host import Host

copyr = """
***********************************************************
******* bluewind batch deploy script ---- by chenz ********
***********************************************************
"""
print
copyr

# 日志模块配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )
#################################################################################################
# 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大1M
Rthandler = RotatingFileHandler('./log/deploy.log', maxBytes=1 * 1024 * 1024, backupCount=5)
Rthandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(filename)s  %(levelname)s   %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
################################################################################################

# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')


# 开发环境重启
def devReboot(handle):
    pass

# 批量执行命令
def runCmd(ctype, appName):
    with open('config/server.js') as config_file:
        config = json.load(config_file)

    if (ctype == 1):
        # 开发环境
        hostConfig = config['develop']
        env = hostConfig['env']

    elif (ctype == 2):
        # 测试环境
        hostConfig = config['test']
        env = hostConfig['env']

    # 解析环境
    hostList = []
    for host in hostConfig['hosts']:
        # 初始化主机实例
        item = Host(host['ip'],  host['port'], host['username'], host['password'], host['path'], host['apollo.bootstrap.namespaces'], host['app.id']);
        # 追加到主机列表
        hostList.append(item)

    for host in hostList:
        ssh_newkey = 'Are you sure you want to continue connecting'


        logging.info('ENV: %s, Host: %s' % (env, host.getIp()))

        # 首先登陆到服务器
        #child = pexpect.popen_spawn.PopenSpawn('ssh %s@%s' % (userName, ip))
        child = pexpect.popen_spawn.PopenSpawn('ssh -tt %s@%s' % (host.getUserName(), host.getIp()))
        i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', '[#\$] '])
        if (i == 0):
            logging.error('SSH could not login. Here is what SSH said:')
            logging.error(child.before, child.after)
            return None

        elif (i == 1):
            child.sendline('yes')
            child.expect('password: ')
            child.sendline(host.getPassword())
            logging.info('1.login successfully')
            # return child

        elif (i == 2):
            child.sendline(host.getPassword())
            logging.info('2.login successfully')

        # 登陆成功后，关闭服务端口
        logging.info('关闭服务端口: %s' % (host.getPort()))
        child.sendline('fuser -k %s/tcp' % (host.getPort()))
        child.expect([str(host.getPort()) + '/tcp', '[#\$] '])
        # print(child.before)

        # 重新打包部署
        logging.info('开始重启服务, 环境: %s, 主机: %s' % (env, host.getIp()))
        child.sendline(
            'find ~/project/creditzx/%s/target -name "%s*.jar" | xargs awk \'END{ var=FILENAME; n=split (var,a,/\//); print a[n]}\'' % (
                appName, appName))
        child.expect(['creditzx-job-1.0-SNAPSHOT.jar', pexpect.EOF], timeout=30)
        jar = child.after.decode("utf-8")
        child.sendline('cd %s' % (host.getPath()))
        child.sendline(
            'nohup java -Dapollo.bootstrap.namespaces=%s -Dapollo.bootstrap.enabled=true -Dapp.id=%s -jar %s > /dev/null 2>&1 & tail -f /data/logs/tomcat/%s.log' % (
                host.getNamespaces(), host.getAppId(), jar, appName))
        while True:
            try:
                i = child.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
                if i == 0:
                    print(child.before.decode("utf-8"))
                else:
                    break
            except pexpect.EOF:
                break

        logging.info('服务器[%s]执行命令完毕' % (host.getIp()))
        # child.close()

# main函数
def main():
    env = int(input('请选择部署环境: \n 1-DEV \n 2-TEST \n'))
    dtype = int(input('请选择要执行的命令:\n\
                  1-重启creditzx-job服务\n\
                  2-重启creditzx-web服务\n\
                  3-重启creditzx-api服务\n\
                  4-更新并重启creditzx-job服务\n\
                  5-更新并重启creditzx-web服务\n\
                  6-更新并重启creditzx-api服务\n\
                  7-关闭creditzx-job服务\n\
                  8-关闭creditzx-web服务\n\
                  9-关闭creditzx-api服务\n'))

    if (dtype == 1):
        runCmd(env, 'creditzx-job')
    elif(dtype == 2):
        runCmd(env, 'creditzx-web')
    elif(dtype == 3):
        runCmd(env, 'creditzx-api')

if __name__ == '__main__':
    main()
