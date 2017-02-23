"""
app.py is executable. no relative imports possible
"""

import web
from web import template, seeother, session, config, database

import map
import lexicon
import my_parser
from utils import hash_password
from forms import login_form, register_form, game_form
from my_parser import ParserError

urls = (
    '/', 'Index',
    '/auth', 'Register',
    '/login','Login',
    '/logout', 'Logout',
    '/game', 'GameEngine',
    '/reset', 'Reset',
)

app = web.application(urls, globals())

web.config.debug = True

db = database(dbn='postgres', db='mydb', user='', password='')

# test if database connection works
entries = db.select('example_users')

# little hack so that debug mode works with sessions
if config.get('_session') is None:
    store = session.DiskStore('sessions')
    session = session.Session(
        app,
        store,
        initializer={'room': None, 'login': 0, 'help_user': 0})
    config._session = session
else:
    session = config._session

render = template.render('templates/',
                         base="layout",
                         globals={'session': session})


class Index(object):
    def GET(self):
        if not logged():
            seeother("/login")
        else:
            # this is used to 'setup' the session with starting values
            session.room = map.START
            seeother("/game")


class Register(object):
    def GET(self):
        # 1. call form to create copy, 2. pass form to template
        form = register_form()
        return render.register(form)

    def POST(self):
        form = register_form()

        if form.validates():
            hashed_password, salt = hash_password(form['password'].value)
            # TODO: replace hardcoded privilege
            privilege = 1
            db.insert('example_users',
                      username=form['username'].value,
                      email=form['email'].value,
                      privilege=privilege,
                      hashed_password=hashed_password,
                      salt=salt)
            seeother('/login')
        else:
            return render.register(form)


def logged():
    return session.get('login') == 1


class Login(object):
    def GET(self):
        form = login_form()
        return render.login(form)

    def POST(self):
        form = login_form()

        if form.validates():
            session.login = 1
            seeother('/')
        else:
            return render.login(form)


class Logout(object):
    def GET(self):
        session.kill()
        seeother('/')


class GameEngine(object):
    def GET(self):
        form = game_form()
        help_user = False
        if session.help_user == 1:
            help_user = True
            session.help_user = 0
        if session.room:
            return render.show_room(room=session.room,
                                    form=form,
                                    help_user=help_user)
        else:
            # why is this here? do you need it?
            return render.you_died()

    def POST(self):
        print 'enter game post'
        form = game_form()

        if form.validates():
            print 'form valid'

            # show help if user types 'help'
            if form['answer'].value == 'help':
                session.help_user = 1

            word_list = lexicon.scan(form['answer'].value)
            sentence = my_parser.parse_sentence(word_list)

            # there is a bug here, can you fix it?
            if session.room and sentence:
                sentence_str = sentence.build_string()
                session.room = session.room.go(sentence_str)

        else:
            return render.show_room(room=session.room,
                                    form=form,
                                    help_user=False)

        seeother("/game")


class Reset(object):
    def GET(self):
        session.kill()
        return ""


def validate_password():
    pass


if __name__ == '__main__':
    app.run()