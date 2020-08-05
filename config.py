import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x8dy&\xba\xb8bc\xcf\xf1S\x0f\xebcB\xe9\xe1'
    MONGODB_SETTINGS = { 'db' : 'ABC_HMS'}


