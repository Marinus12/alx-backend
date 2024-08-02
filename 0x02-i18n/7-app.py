#!/usr/bin/env python3
"""a get_timezone function and use the babel.timezoneselector decorator
   """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz import exceptions as pytz_exceptions


app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'


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
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    # 2. Locale from user settings
    if g.user and g.user['locale'] in app.config['BABEL_SUPPORTED_LOCALES']:
        return g.user['locale']
    # 3. Locale from request header
    return request.accept_languages.best_match(app.config
                                               ['BABEL_SUPPORTED_LOCALES'])


@babel.timezoneselector
def get_timezone():
    # 1. Timezone from URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz_exceptions.UnknownTimeZoneError:
            pass
    # 2. Timezone from user settings
    if g.user:
        user_timezone = g.user.get('timezone')
        if user_timezone:
            try:
                pytz.timezone(user_timezone)
                return user_timezone
            except pytz_exceptions.UnknownTimeZoneError:
                pass
    # 3. Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(debug=True)
