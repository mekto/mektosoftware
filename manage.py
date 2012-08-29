from flask.ext.script import Manager
from flask.ext.frozen import Freezer
from mektosoftware import app


manager = Manager(app)

@manager.option('-t', '--test', action='store_true', dest='test', default=False, help='start an HTTP server to test the build result')
def freeze(test):
    """ Freezes application into a set of static files. """
    freezer = Freezer(app)
    if test:
        freezer.run()
    else:
        freezer.freeze()

if __name__ == '__main__':
    manager.run()
