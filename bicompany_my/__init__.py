from pyramid.config import Configurator
from bicompany_my.security import MySecurityPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    policy = MySecurityPolicy(secret=settings["auth.secret"])
    config.set_security_policy(policy)

    config.include('pyramid_mako')
    config.include('.security')
    config.include('.routes')
    config.include('.models')

    config.scan()
    return config.make_wsgi_app()
