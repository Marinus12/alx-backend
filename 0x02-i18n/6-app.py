#!/usr/bin/env python3
"""Change your get_locale function to use a user’s preferred local if supported
   """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    login_as = request.args.get('login_as')
    if login_as:
        user_id = int(login_as)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    g.user = get_user()


@babel.localeselector
def get_locale():
    locale = request.args.get('locale')
    if locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    if g.user and g.user['locale'] in app.config['BABEL_SUPPORTED_LOCALES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config
                                               ['BABEL_SUPPORTED_LOCALES'])


@app.route('/')
def index():
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(debug=True)
