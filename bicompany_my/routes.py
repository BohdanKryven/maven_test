from pyramid.authorization import Allow, Everyone
from pyramid.httpexceptions import HTTPNotFound, HTTPSeeOther

from . import models


def includeme(config):
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("start_page", "/")
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route("view_book_info", "/{book_name}", factory=view_book_factory)
    config.add_route("add_new_book", "/add_book/{book_name}", factory=new_book_factory)
    config.add_route("edit_book", "/edit_book/{book_name}", factory=view_book_factory)


def view_book_factory(request):
    book_name = request.matchdict["book_name"]
    book = request.dbsession.query(models.Book).filter_by(name=book_name).first()
    if book is None:
        raise HTTPNotFound
    return BookResource(book)


class BookResource:
    def __init__(self, book):
        self.book = book

    def __acl__(self):
        return [
            (Allow, Everyone, "view"),
            (Allow, "role:editor", "edit"),
            (Allow, self.book.author, "edit"),
        ]


def new_book_factory(request):
    book_name = request.matchdict["book_name"]
    if request.dbsession.query(models.Book).filter_by(name=book_name).count() > 0:
        next_url = request.route_url("edit_book_info", book_name=book_name)
        raise HTTPSeeOther(location=next_url)
    return NewBook(book_name)


class NewBook:
    def __init__(self, book_name):
        self.book_name = book_name

    def __acl__(self):
        return [
            (Allow, "role:editor", "create"),
            (Allow, "role:basic", "create"),
        ]
