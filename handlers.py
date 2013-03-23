from logging import getLogger
from os.path import dirname, join

from jinja2 import Environment, FileSystemLoader
import webapp2
from google.appengine.api import users


log = getLogger('goal_shame.handlers')

class TemplateHandler(webapp2.RequestHandler):
    template = 'index.html'

    def get_current_user(self):
        return users.get_current_user()

    def get_template(self):
        log.debug('%s.get_template()' % (repr(self),))
        return self.template

    def get_jinja_environment(self):
        log.debug('%s.get_jinja_environment()' % (repr(self),))
        return Environment(
                loader=FileSystemLoader(self.app.config.get('jinja_templates',
                    join(dirname(__file__),'templates'))))

    def get_context_data(self, **kwargs):
        log.debug('%s.get_context_data(**kwargs=%s)' % (repr(self),
            unicode(kwargs),))
        kwargs['user'] = self.get_current_user()
        if kwargs['user']:
            kwargs['logout_url'] = users.create_logout_url("/")
        else:
            kwargs['login_url'] = users.create_login_url("/")

        return kwargs

    def __call__(self, request, *args, **kwargs):
        log.debug('%s(request=%s, *args=%s, **kwargs=%s)' % (repr(self),
            repr(request), unicode(args), unicode(kwargs),))
        return self.get(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        log.debug('%s.get(*args=%s, **kwargs=%s)' % (repr(self),
            unicode(args), unicode(kwargs),))
        self.render(self.get_context_data())

    def render(self, context={}):
        log.debug('%s.render(context=%s)' % (repr(self), unicode(context),))
        template = \
            self.get_jinja_environment().get_template(self.get_template())
        self.response.write(template.render(context))

class Dashboard(TemplateHandler):
    template = 'dashboard.html'
