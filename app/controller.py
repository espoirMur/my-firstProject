from flask_mail import Message
from flask import render_template,redirect,url_for,request,session,json
from . import mail
from app import app_config
from rauth.service import OAuth2Service,OAuth1Service
#from .. import smtpserver
import requests,json

from email.mime.text import MIMEText
def send_mail_flask(to,subject,template,**kwargs):
    msg = Message(subject=subject, sender=app_config.get('development').FLASKY_MAIL_SENDER, recipients=to)
    msg.body=render_template(template+'.txt', **kwargs)
    msg.html=render_template(template+'.html', **kwargs)
    mail.send(msg)
    return True

#for sending mail for the api
def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/samples.mailgun.org/messages",
        auth=("api", "key-3ax6xnjp29jd6fds4gc373sgvjxteol0"),
        data={"from": "Excited User <excited@samples.mailgun.org>",
              "to": ["devs@mailgun.net"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!"})

def send_smsbyMblox():
    headers={"Authorization": "Bearer {898d66d1576d46b4aa7f1353bfd23e7e}",
             "Content-Type": "application/json"}
    body={"from":"Mblox",
          "to":["+243993505357"],
          "body":"Hi this is my first message using Mbs SMS REST API"}
    url = "https://api.clxcommunications.com/xms/v1/macabesear12/"
    return requests.post(url=url,headers=headers,body=json(body)
    )
#sending mail from python direcly with gmail
"""def send_mail(you):
    #in app this doesn't work i don't know why you must put real username and password be able to send mail
    login =app_config.get('development').MAIL_USERNAME
    paswd = app_config.get('development').MAIL_PASSWORD
    textfile="/auth/new_user.txt"
    fp =open(textfile,'rb')
    msg=MIMEText(fp.read())
    fp.close()
    msg['Subject'] = 'The contents of %s' % textfile
    msg['From'] = login
    msg['To'] = you
    try:
        smtpserver.login(login,paswd)
        smtpserver.sendmail( msg['From'],[you],msg.as_string())
    finally:
        smtpserver.quit()
    return True """

class AuthSignIn(object):
    providers=None

    def __init__(self,provider_name):
        self.provider_name=provider_name
        credentials=app_config.get("development").OAUTH_CREDENTIALS.get(provider_name) #les logins fournis par facebook
        self.consumer_id=credentials.get('id')
        self.consumer_secret=credentials.get('secret')
    def authorize(self):
        pass

    def callback(self):
        pass
    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name,_external=True)

    @staticmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(AuthSignIn):
    def __init__(self):
        super(FacebookSignIn,self).__init__('facebook')
        self.service=OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )
    def authorize(self):
        print  self.service.client_id
        print self.service.client_secret
        return redirect(self.service.get_authorize_url(scope='public_profile,email', response_type='code',
                                                       redirect_uri=self.get_callback_url()))
    def callback(self):
        if 'code' not in request.args:
            return None,None,None
        print request.args
        oauth_session= self.service.get_auth_session(data={
            'code':request.args['code'],
            'grant_type':'authorization_code',
            'redirect_uri':self.get_callback_url()

        })
        print oauth_session.access_token
        print '-----------------------------------------'
        print oauth_session.params
        me=oauth_session.get('me?fields=id,email,first_name,last_name').json()
        print me
        return ('facebook$'+me['id'],me.get('email').split('@')[0],me.get('email'),me.get('first_name')+" "+me.get('last_name'))

class TwitterSignIn(AuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url=' https://api.twitter.com/oauth/request_token',
            authorize_url=' https://api.twitter.com/oauth/authenticate',
            access_token_url=' https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/')

    def authorize(self):

        print " key is :" +self.service.consumer_key
        print "secret is :"+self.service.consumer_secret
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token

        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token=session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None,None,None
        oauth_session=self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None
class GoogleSignIn(AuthSignIn):
    def __init__(self):
        super(GoogleSignIn,self).__init__('google')
        self.service =OAuth2Service(
        name='google',
        client_id=self.consumer_id,
        client_secret=self.consumer_secret,
        access_token_url="https://www.googleapis.com/oauth2/v4/token",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        base_url="https://www.googleapis.com/oauth2/v3/userinfo"

     )
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )
    def callback(self):
        print request.args
        if 'code' not in request.args:
            return None,None,None

        oauth_session =self.service.get_auth_session(
            data={
                'code':request.args['code'],
                'grant_type':'authorization_code',
                'redirect_uri':self.get_callback_url()
            },
            decoder=json.loads
        )

        me=oauth_session.get('').json()
        return ('google$'+me['sub'],me.get('email').split('@')[0],me.get('email'),me['name'])