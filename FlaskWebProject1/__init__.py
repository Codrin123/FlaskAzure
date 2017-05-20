"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config.update(dict(
	SECRET_KEY="dev key"
))

import FlaskWebProject1.views
