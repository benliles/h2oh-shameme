from logging import getLogger
from os.path import dirname, join

from jinja2 import Environment, FileSystemLoader
import webapp2
from google.appengine.api import users



log = getLogger('goal_shame.handlers')

class BaseHandler(webapp2.RequestHandler):
    def get_current_user(self):
        return users.get_current_user()

class ApiHandler(BaseHandler):
    def get_current_user(self):
        email = self.request.get('email', None)
        if email is not None:
            return users.User(email=email)
        return super(ApiHandler, self).get_current_user()

class HomeHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        return webapp2.redirect_to('dashboard')

class TemplateHandler(BaseHandler):
    template = 'index.html'

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
        context = {}
        context['user'] = self.get_current_user()
        context['users'] = users
        context['request'] = self.request
        context['app'] = self.app
        context['handler'] = self

        context.update(kwargs)

        return context

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

