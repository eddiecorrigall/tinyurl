from flask import Blueprint

blueprint = Blueprint('tinyurl', __name__)

from app.tinyurl import views
