from pyramid.httpexceptions import HTTPSeeOther, HTTPForbidden
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(
    route_name='start_page',
    renderer='/templates/mytemplate.mako'
)
def start_page(request):
    try:
        books = request.dbsession.query(models.Book).all()
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    return {'books': books}


@view_config(
    route_name="view_book_info",
    renderer="/templates/book_info.mako"
)
def book_info(request):
    book = request.context.book
    print(request.context)
    return {
        "book": book
    }


@view_config(
    route_name="edit_book",
    renderer="/templates/edit_book.mako",
    permission="edit"
)
def edit_book(request):
    book = request.context.book
    if request.method == "POST":
        book.description = request.params["description"]
        next_url = request.route_url("view_book_info", book_name=book.name)
        return HTTPSeeOther(location=next_url)
    return dict(
        book_name=book.name,
        description=book.description,
        url=request.route_url("edit_book", book_name=book.name)
    )


@view_config(
    route_name="add_new_book",
    renderer="/templates/edit_book.mako"
)
def add_book(request):
    book_name = request.context.book_name
    if request.method == 'POST':
        description = request.params['description']
        book = models.Book(name=book_name, description=description)
        book.author = request.identity
        request.dbsession.add(book)
        next_url = request.route_url('view_book_info', book_name=book_name)
        return HTTPSeeOther(location=next_url)
    url = request.route_url('add_new_book', book_name=book_name)
    return dict(book_name=book_name, description='', url=url)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
