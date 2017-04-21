# common/errors.py

from main import main
from  flask import make_response

@main.app_errorhandler(404)
def page_not_found():
    return { 'error': 'page not found'}, 404