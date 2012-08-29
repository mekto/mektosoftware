from flask.ext.script import Manager
from flask.ext.frozen import Freezer
from mektosoftware import app


manager = Manager(app)

@manager.command
def freeze():
    """ Freezes application into a set of static files. """
    freezer = Freezer(app)
    freezer.freeze()

@manager.command
def freeze_test():
    """ Freezes application and starts an HTTP server to test the build result. """
    freezer = Freezer(app)
    freezer.run()

if __name__ == '__main__':
    manager.run()
