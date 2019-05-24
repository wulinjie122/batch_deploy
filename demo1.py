import requests

response = requests.get("http://www.baidu.com")
#print(response.text)
print(response.encoding)
print(response.status_code)
print(response.headers['content-type'])

classmates = (1,)
print(classmates)
