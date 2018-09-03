from node.api.debug import bp as debug
from node.api.auth import bp as auth
from node.api.organizations import bp as organizations
from node.api.departments import bp as departments
from node.api.groups import bp as groups
from node.api.specializations import bp as specializations
from node.api.reviews import bp as reviews
from node.api.persons import bp as persons
from node.api.skills import bp as skills
from node.api.group_tests import bp as group_tests
from node.api.surveys import bp as surveys

from node.api.debug import api_v2 as debug_v2

def register_api_default(app):
    app.register_blueprint(debug)
    app.register_blueprint(auth)
    app.register_blueprint(organizations)
    app.register_blueprint(departments)
    app.register_blueprint(groups)
    app.register_blueprint(specializations)
    app.register_blueprint(reviews)
    app.register_blueprint(persons)
    app.register_blueprint(skills)
    app.register_blueprint(group_tests)
    app.register_blueprint(surveys)


def register_api_v1(app):
    app.register_blueprint(debug, url_prefix="/v1")
    app.register_blueprint(auth, url_prefix="/v1")
    app.register_blueprint(organizations, url_prefix="/v1")
    app.register_blueprint(departments, url_prefix="/v1")
    app.register_blueprint(groups, url_prefix="/v1")
    app.register_blueprint(specializations, url_prefix="/v1")
    app.register_blueprint(reviews, url_prefix="/v1")
    app.register_blueprint(persons, url_prefix="/v1")
    app.register_blueprint(skills, url_prefix="/v1")
    app.register_blueprint(group_tests, url_prefix="/v1")
    app.register_blueprint(surveys, url_prefix="/v1")


def register_api_v2(app):
    app.register_blueprint(debug_v2, url_prefix="/v2")