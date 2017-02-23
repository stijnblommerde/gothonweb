"""
session tutorial
session is een dictionary die opgeslagen wordt op de harde schijf
de 'count' variabele is irrelevant. je kunt het vervangen door 'foo'
enige punt wat ze maken is dat je data kunt opslaan. de waarde van de count
blijft bestaan na het sluiten en heropenen van de browser.
de waarde verdwijnt met het kill commando
"""

import web

# session don't work in debug mode
web.config.debug = False
urls = (
    "/count", "Count",
    "/reset", "Reset"
)
app = web.application(urls, locals())
session = web.session.Session(
    app, web.session.DiskStore('sessions'),
    initializer={'count': 0})


class Count(object):
    def GET(self):
        session.count += 1
        return str(session.count)

class Reset(object):
    def GET(self):
        # kill the session
        session.kill()
        return ""

if __name__ == "__main__":
    app.run()

