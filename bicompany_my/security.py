from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import Everyone, ACLHelper, Authenticated
from pyramid.csrf import CookieCSRFStoragePolicy
from pyramid.request import RequestLocalCache

from . import models

import bcrypt


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)


USERS = {'editor': hash_password('editor'),
         'viewer': hash_password('viewer')}


class MySecurityPolicy:
    def __init__(self, secret):
        self.authtkt = AuthTktCookieHelper(secret)
        self.identity_cache = RequestLocalCache(self.load_identity)

    def load_identity(self, request):
        identity = self.authtkt.identify(request)
        if identity is None:
            return None

        userid = identity['userid']
        user = request.dbsession.query(models.Author).get(userid)
        return user

    def identity(self, request):
        return self.identity_cache.get_or_create(request)

    def authenticated_userid(self, request):
        user = self.identity(request)
        if user is not None:
            return user.id

    def remember(self, request, userid, **kw):
        return self.authtkt.remember(request, userid, **kw)

    def forget(self, request, **kw):
        return self.authtkt.forget(request, **kw)

    def permits(self, request, context, permission):
        principals = [Everyone]
        if self.identity is not None:
            principals.append(Authenticated)
            principals.append(request.identity)
            principals.append('role:' + request.identity.role)
        return ACLHelper().permits(context, principals, permission)


def includeme(config):
    settings = config.get_settings()

    config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
    config.set_default_csrf_options(require_csrf=True)

    config.set_security_policy(MySecurityPolicy(settings['auth.secret']))
