#!/usr/bin/env python3
"""Based on the inferred time zone
   display the current time on the home page in the default format.
   """

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz import exceptions as pytz_exceptions
from datetime import datetime

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
    """Retrieve a user dictionary or None if the user ID is not found."""
    login_as = request.args.get('login_as')
    if login_as:
        user_id = int(login_as)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """Executed before all other functions to set the current user."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determine the best match for supported languages.

    Priority:
    1. Locale from URL parameters.
    2. Locale from user settings.
    3. Locale from request header.
    4. Default locale.
    """
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
    """
    Determine the best match for supported timezones.

    Priority:
    1. Timezone from URL parameters.
    2. Timezone from user settings.
    3. Default to UTC.
    """
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
    """Render the home page with current time based on the inferred timezone"""
    timezone = get_timezone()
    local_time = datetime.now(pytz.timezone(timezone))
    formatted_time = local_time.strftime('%b %d, %Y, %I:%M:%S %p')
    if get_locale() == 'fr':
        formatted_time = local_time.strftime('%d %b %Y à %H:%M:%S')
    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(debug=True)
