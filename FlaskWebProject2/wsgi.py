from whitenoise import WhiteNoise
from FlaskWebProject2 import app

application = WhiteNoise(app)
application.add_files('static/', prefix='static/')
