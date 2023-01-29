# Config file
from datetime import timedelta


class Config:
    """Flask Config"""

    # Variables
    FLASK_ENV = 'development'
    SECRET_KEY = "1cedcfbf2442ee6368042ed734f6d5fa"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SESSION_PERMANENT = 'FALSE'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
