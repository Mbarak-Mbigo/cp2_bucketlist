# api/main/__init__.py
from flask import Blueprint

# create a blueprint
# arguments: blueprint name and a module/package where the blueprint is located
main = Blueprint('api_v1', __name__)

from common import errors
#and import views