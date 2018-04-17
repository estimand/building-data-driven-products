from flask import Flask

from . import talks


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_pyfile('config.py', silent=True)

app.register_blueprint(talks.bp)

app.add_url_rule('/', endpoint='talks.index')
