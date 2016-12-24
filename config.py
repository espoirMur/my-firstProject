class Config(object):
    ''''global config "'''

class DevellopementConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    #config for devellopement
class ProductionConfig(Config):
    DEBUG = False

app_config ={
    'development':DevellopementConfig,
    'production':ProductionConfig
}
