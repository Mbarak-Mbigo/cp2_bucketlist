#!/usr/bin/env python
"""Launch script.

manage.py
used to start the application.
"""
import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from api.models import User, BucketList, BucketItem

from api import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, user=User, buckelist=BucketList, bucketitem=BucketItem)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unittests."""
    import unittest
    create_app(os.getenv('FLASK_CONFIG') or 'testing')
    tests = unittest.TestLoader().discover('api/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()
