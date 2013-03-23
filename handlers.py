from logging import getLogger
from os.path import dirname, join

from jinja2 import Environment, FileSystemLoader
import webapp2



log = getLogger('goal_shame.handlers')

class TemplateHandler(webapp2.RequestHandler):
    def __init__(self, **kwargs):
        if 'template' in kwargs:
            self.template = kwargs.pop('template')
        super(TemplateHandler, self).__init__(**kwargs)

    def get_template(self):
        return self.template

    def get_jinja_environment(self):
        return Environment(
                loader=FileSystemLoader(self.app.config.get('jinja_templates',
                    join(dirname(__file__),'templates'))))

    def get_context_data(self, **kwargs):
        return kwargs

    def __call__(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.render(self.get_context_data())

    def render(self, context={}):
        template = \
            self.get_jinja_environment().get_template(self.get_template())
        self.response.out.write(template.render(context))

