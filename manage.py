#!/usr/bin/env python
"""Launch script.

manage.py
used to start the application.
"""
import os
import unittest

import coverage
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from api.models import User, BucketList, BucketItem

from api import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, BucketList=BucketList, BucketItem=BucketItem )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

COV = coverage.coverage(
    branch=True,
    omit=[
        'api/tests/*',
        '*/virtualenvs/*',
        'manage.py',
        'api/models.py',
        'api/__init__.py'
    ]
)
COV.start()

@manager.command
def create_db():
    """Creates db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops db tables."""
    db.drop_all()
    
@manager.command
def test():
    """Run the unittests."""
    create_app(os.getenv('FLASK_CONFIG') or 'testing')
    tests = unittest.TestLoader().discover('api/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
@manager.command
def cov():
    """Run tests with coverage."""
    create_app(os.getenv('FLASK_CONFIG') or 'testing')
    tests = unittest.TestLoader().discover('api/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
