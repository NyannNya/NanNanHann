def line_token():
    return 'line_token'

def line_secret():
    return 'line_secret'

def admin():
    return []

def imgur():
    return 'imgur api account'

def redis(dict):
    data = {
        'host' : 'redis-xxx.xxx.xxx.cloud.redislabs.com',
        'port' : 'xxxxx',
        'password' : 'xxxxxx'
    }
    return data[dict]