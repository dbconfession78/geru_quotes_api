"""
Module: app - uses 'QueryManager' object to execute application and make
              queries to the "quotes" api.
"""
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config

from quotes import API
from random import sample
from uuid import uuid4
from waitress import serve
from wsgiref.simple_server import make_server

sf = SignedCookieSessionFactory("Ican'ttellyoumysecretnowcanI?")


class QueryManager:
    def __init__(self):
        """
        __init__ - initializer for the QueryManager class
        """
        self.api = API()

    def render_title_page(self, request):
        """
        render_title_page - renders empty page with title of project
        :request: http request made for page.
        :Return: instace of the 'Response' class
        """
        # TODO:make sure 'id' is not in the sessions string
        request.session['id'] = str(uuid4)
        return {"content": "Web Challenge 1.0"}

    @view_config(route_name="get_quote")
    def query_api(self, request):
        """
        query_api - fetches specific quote from API().quotes
        :request: incoming http request headers, including desired quote number
        Return: string cast dictionary object containing requested quote(s)
        """
        def query_quote_by_id(n):
            return self.api.get_quote(n)

        n = request.matchdict.get('quote_num')
        if n:
            quotes = query_quote_by_id(n)
        else:
            quotes = self.api.get_quotes()
        return {"dct": quotes, "n": self.api.n}


def main():
    """
    main - application entry point
    """
    q_manager = QueryManager()
    with Configurator() as config:
        config.include("pyramid_jinja2")
        config.set_session_factory(sf)

        config.add_route('title', '/')
        config.add_route('get_quotes', '/quotes')
        config.add_route('get_quote', '/quotes/{quote_num}')
        config.add_route('get_random_quote', '/quotes/random')

        config.add_view(q_manager.render_title_page,
                        route_name='title',
                        renderer="./templates/index.jinja2")

        config.add_view(q_manager.query_api,
                        route_name='get_quotes',
                        renderer="./templates/index.jinja2")

        config.add_view(q_manager.query_api,
                        route_name='get_quote',
                        renderer="./templates/index.jinja2")

        config.add_view(q_manager.query_api,
                        route_name='get_random_quote',
                        renderer="./templates/index.jinja2")

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()


if __name__ == '__main__':
    main()
