import unittest
import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app = create_app)

@cli.command()
def cov():
    tests = unittest.TestLoader().discover('project/tests')
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

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    db.session.add(User(username= "natalie.curtis", email= "natalie.curtis@example.com"))
    db.session.add(User(username= "alexa.bishop", email= "alexa.bishop@example.com"))
    db.session.add(User(username= "joshua.wood", email= "joshua.wood@example.com"))
    db.session.add(User(username= "jeanette.garcia", email= "jeanette.garcia@example.com"))
    db.session.add(User(username= "vicki.wells", email= "vicki.wells@example.com"))
    db.session.add(User(username= "scott.bishop", email= "scott.bishop@example.com"))
    db.session.add(User(username= "jennifer.wood", email= "jennifer.wood@example.com"))
    db.session.add(User(username= "mabel.rhodes", email= "mabel.rhodes@example.com"))
    db.session.add(User(username= "teresa.mills", email= "teresa.mills@example.com"))
    db.session.add(User(username= "janet.nichols", email= "janet.nichols@example.com"))
    db.session.add(User(username= "sandra.mason", email= "sandra.mason@example.com"))
    db.session.add(User(username= "gabriella.simmons", email= "gabriella.simmons@example.com"))
    db.session.add(User(username= "lorraine.owens", email= "lorraine.owens@example.com"))
    db.session.add(User(username= "jamie.perry", email= "jamie.perry@example.com"))
    db.session.add(User(username= "renee.harvey", email= "renee.harvey@example.com"))
    db.session.add(User(username= "melvin.stanley", email= "melvin.stanley@example.com"))
    db.session.add(User(username= "yvonne.gardner", email= "yvonne.gardner@example.com"))
    db.session.add(User(username= "wanda.morales", email= "wanda.morales@example.com"))
    db.session.add(User(username= "stella.pena", email= "stella.pena@example.com"))
    db.session.add(User(username= "frank.vargas", email= "frank.vargas@example.com"))
    db.session.add(User(username= "joe.mcdonalid", email= "joe.mcdonalid@example.com"))
    db.session.add(User(username= "isobel.schmidt", email= "isobel.schmidt@example.com"))
    db.session.add(User(username= "roberto.mitchell", email= "roberto.mitchell@example.com"))
    db.session.add(User(username= "teresa.fowler", email= "teresa.fowler@example.com"))
    db.session.add(User(username= "lillie.gilbert", email= "lillie.gilbert@example.com"))
    db.session.commit()

if __name__ == '__main__':
    cli()
