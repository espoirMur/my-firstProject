import os
class Config(object):
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    FLASKY_MAIL_SUBJECT_PREFIX = 'Welcome'
    FLASKY_MAIL_SENDER = 'espoir.mur@gmail.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    ''''global config "'''

class DevellopementConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': os.environ.get('FACEBOOK_ID'),
            'secret': os.environ.get('FACEBOOK_SECRET')

        },
        'twitter':{
          'id':os.environ.get('TWITTER_ID'),
           'secret':os.environ.get('TWITTER_SECRET')
        },
        'google':{
            'id': os.environ.get('GOOGLE_ID'),
            'secret': os.environ.get('GOOGLE_SECRET')

        }

    }
    #config for production
class ProductionConfig(Config):
    DEBUG = False
    """want to send error log to admin email evry time it occurs in production mode """
    @classmethod
    def init_app(cls,app):
        import  logging
        from logging.handlers import SMTPHandler
        credentials=None
        secure=None
        if getattr(cls,'MAIL_USERNAME',None) is not None:
            credentials=(cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure=()
        mail_handler=SMTPHandler(
            mailhost=(cls.MAIL_SERVER,cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=cls.FLASKY_ADMIN,
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application error',
            credentials=credentials,secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


   # configuration for testing
class TestingConfig(Config):
    WTF_CSRF_ENABLED = False

app_config ={
    'development':DevellopementConfig,
    'production':ProductionConfig,
    'test':TestingConfig
}

class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
