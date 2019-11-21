from flask import Flask, g
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login/'

with app.app_context():
	from jursi import read_config
	g.config_params = read_config.parse()

# start BackgroundJobs

import jursi.views

