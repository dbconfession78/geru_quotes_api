"""
Module: app - uses 'QueryManager' object to execute application and make
              queries to the "quotes" api.
"""
from datetime import datetime
from models.page_request import PageRequest
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from quotes import API
from models import storage
from uuid import uuid4
from wsgiref.simple_server import make_server


class QueryManager:
    """
    QueryManager - handles api requests, session cookies and page rendering
    """
    def __init__(self):
        self.api = API()
        self.session_factory = SignedCookieSessionFactory(
            "Ican'ttellyoumysecretnowcanI?")

    def render_title_page(self, request):
        """
        render_title_page - renders empty page with title of project
        :param request: http request made for page.
        :return: instace of the 'Response' class
        """
        self.handle_session(request)
        return {"content": "Web Challenge 1.0"}

    def query_api(self, request):
        """
        query_api - fetches specific quote from API().quotes
        :param request: incoming http request headers, including desired quote
                        number
        :return: string cast dictionary object containing requested quote(s)
        """
        def query_quote_by_id(n):
            return self.api.get_quote(n)

        self.handle_session(request)
        n = request.matchdict.get('quote_num')
        if n:
            quotes = query_quote_by_id(n)
        else:
            quotes = self.api.get_quotes()
        return {"dct": quotes, "n": self.api.n}

    def handle_session(self, request):
        """
        handle_session - stores session info in db
        :param request: session request
        :return: None
        """
        if 'id' not in request.session:
            request.session['id'] = str(uuid4())
            print("new session ID created.")
        else:
            print("this session ID exists.")

        req_url = request.path_url
        new_request = PageRequest(session_id=request.session['id'],
                                  datetime=datetime.now(),
                                  request=req_url)
        storage.new(new_request)
        storage.save()


def main():
    """
    main - application entry point
    """
    q_manager = QueryManager()
    with Configurator() as config:
        config.include("pyramid_jinja2")
        config.set_session_factory(q_manager.session_factory)

        config.add_route('title', '/')
        config.add_route('get_quotes', '/quotes')
        config.add_route('get_quote', '/quotes/{quote_num}')
        config.add_route('get_random_quote', '/quotes/random')

        # First view, available at http://localhost:6543/
        config.add_view(q_manager.render_title_page,
                        route_name='title',
                        renderer="./templates/index.jinja2")

        # /quotes
        config.add_view(q_manager.query_api,
                        route_name='get_quotes',
                        renderer="./templates/index.jinja2")

        # /quotes/<quote number>
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
