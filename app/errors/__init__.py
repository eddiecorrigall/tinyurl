from flask import Blueprint

blueprint = Blueprint('errors', __name__)

from app.errors import views
