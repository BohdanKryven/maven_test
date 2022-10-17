import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    author_admin = models.author.Author(
        initials="Bohdan Kryven",
        role="editor"
    )
    author_admin.set_password("editor")
    author_basic = models.author.Author(
        initials="Basic User",
        role="basic"
    )
    author_basic.set_password("basic")
    dbsession.add_all([author_admin, author_basic])

    admin_book = models.models.Book(
        name="Admin book",
        description="admin book",
        author=author_admin
    )
    basic_book = models.models.Book(
        name="Basic book",
        description="basic book",
        author=author_basic
    )
    dbsession.add_all([admin_book, basic_book])


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
