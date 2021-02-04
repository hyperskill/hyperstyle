import requests


def do_search(bookstore_url, params):
    return requests.get(url=bookstore_url,
                        params=params)
