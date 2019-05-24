import logging
from logging.handlers import RotatingFileHandler

import pexpect
import simplejson as json
from pexpect.popen_spawn import PopenSpawn

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

# 命令列表
cmdList = {
    'creditzx-job-reboot-dev': [
        'fuser -k 8888/tcp',
        #'JARFILE=$(find ~/project/creditzx/creditzx-job/target -name "creditzx-job*.jar" | xargs awk \'END{ var=FILENAME; n=split (var,a,/\//); print a[n]}\')',
        'cd /root/deployer/creditzx',
        'nohup java -Dapollo.bootstrap.namespaces=creditzx-job -Dapollo.bootstrap.enabled=true -Dapp.id=9f84cc5e3294333b95d03b3f5de3d99e -jar creditzx-job-1.0-SNAPSHOT.jar > /dev/null 2>&1'
    ]
}


# 批量执行命令
def reboot(ctype):
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

    for host in hostConfig['hosts']:
        ssh_newkey = 'Are you sure you want to continue connecting'
        ip = host['ip']
        port = host['port']
        userName = host['username']
        password = host['password']
        namespaces = host['apollo.bootstrap.namespaces']
        appId = host['app.id']
        path = host['path']

        logging.info('ENV: %s, Host: %s' % (env, ip))

        #child = pexpect.popen_spawn.PopenSpawn('ssh %s@%s' % (userName, ip))
        child = pexpect.popen_spawn.PopenSpawn('ssh -tt %s@%s' % (userName, ip))
        i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', '[#\$] '])
        if (i == 0):
            logging.error('SSH could not login. Here is what SSH said:')
            logging.error(child.before, child.after)
            return None

        elif (i == 1):
            child.sendline('yes')
            child.expect('password: ')
            child.sendline(password)
            logging.info('1.login successfully')
            # return child

        elif (i == 2):
            child.sendline(password)
            logging.info('2.login successfully')

        logging.info('关闭服务端口: %s' % (port))
        child.sendline('fuser -k %s/tcp' % (port))
        child.expect(['8888/tcp', '[#\$] '])
        #print(child.before)

        logging.info('开始重启服务, ENV: %s, Host: %s' % (env, ip))
        child.sendline('find ~/project/creditzx/creditzx-job/target -name "creditzx-job*.jar" | xargs awk \'END{ var=FILENAME; n=split (var,a,/\//); print a[n]}\'')
        child.expect(['creditzx-job-1.0-SNAPSHOT.jar', pexpect.EOF], timeout=30)
        jar = child.after.decode("utf-8")
        child.sendline('cd %s' % (path))
        child.sendline('nohup java -Dapollo.bootstrap.namespaces=%s -Dapollo.bootstrap.enabled=true -Dapp.id=%s -jar %s > /dev/null 2>&1 & tail -f /data/logs/tomcat/creditzx-job.log' % (namespaces, appId, jar))
        while True:
            try:
                child.expect('\n')
                print(child.before.decode("utf-8"))
            except pexpect.EOF:
                break
        #child.close()
        logging.info('服务器[%s]执行命令完毕' % (ip))



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
        reboot(env)

if __name__ == '__main__':
    main()
