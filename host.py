# 主机类
class Host:

    def __init__(self, ip, port, username, password, path, namespaces, appId):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.path = path
        self.namespaces = namespaces
        self.appId = appId

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port

    def getUserName(self):
        return self.username

    def getPassword(self):
        return self.password

    def getPath(self):
        return self.path

    def getNamespaces(self):
        return self.namespaces

    def getAppId(self):
        return self.appId
