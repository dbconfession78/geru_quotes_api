import requests
from random import sample
"""
Module: quotes - uses the API class to query the 'Zen of Python' api
"""


class API:
    def __init__(self):
        """
        __init__ - initializes an instance of the API class
        """
        self.api_url = "https://1c22eh3aj8.execute-api.us-east-1.amazonaws.com/challenge/quotes"
        self.api_messages = [" is not a valid quote id.",
                             "unable to connect to api."]
        self.n = None
        """
        self.quotes = {
            "quotes": [
                "Beautiful is better than ugly.",
                "Explicit is better than implicit.",
                "Simple is better than complex.",
                "Complex is better than complicated.",
                "Flat is better than nested.",
                "Sparse is better than dense.",
                "Readability counts.",
                "Special cases aren't special enough to break the rules.",
                "Although practicality beats purity.",
                "Errors should never pass silently.",
                "Unless explicitly silenced.",
                "In the face of ambiguity, refuse the temptation to guess.",
                "There should be one-- and preferably only one --obvious way to do it.",
                "Although that way may not be obvious at first unless you're Dutch.",
                "Now is better than never.",
                "Although never is often better than *right* now.",
                "If the implementation is hard to explain, it's a bad idea.",
                "If the implementation is easy to explain, it may be a good idea.",
                "Namespaces are one honking great idea -- let's do more of those!"
            ]
        }
        """
    def get_quotes(self):
        """
        get_quotes - api request for all quotes from 'Zen of Python'
        :Return: a dictionary with either the requested quote or an api message
        """
        r = requests.get(self.api_url)
        if r.status_code == 200:
            return r.json()
        else:
            return {"quotes": ["Unable to retrieve quotes"]}

    def get_quote(self, n):
        """
        get_quote - api request for quote based on input quote index, 'n'
        :n: api quote index
        :Return: dictionary with either the requested quote or error message
        """
        self.n = None
        r = requests.get(self.api_url)
        if r.status_code == 200:
            quotes = r.json()["quotes"]
            _len = len(quotes)
            if not n.isnumeric():
                if n == "random":
                    n = sample(range(1, _len+1), 1)[0]
            else:
                n = int(n)

            self.n = n
            if type(n) != int:
                val = "{}".format(self.api_messages[0])
                return {"quote": "{}".format(val)}

            val = quotes[self.n-1] if n > 0 and n <= _len else \
                self.api_messages[0]
        else:
            val = self.api_messages[1]
        return {"quote": "{}".format(val)}
