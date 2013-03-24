from datetime import datetime
from json import dumps
from logging import getLogger

from google.appengine.api import users
from google.appengine.ext import db

from handlers import TemplateHandler
from models import Goal



log = getLogger('goal_shame.goals')

class Dashboard(TemplateHandler):
    template = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['goals'] = Goal.all().filter('user =', users.get_current_user())
        log.info('Found %d goals' % (context['goals'].count(),))
        return context

class Create(TemplateHandler):
    def post(self, *args, **kwargs):
        log.info('Posting a goal: %s' % (unicode(self.request.POST),))
        try:
            name = self.request.get('name')
            latitude = float(self.request.get('latitude', None))
            longitude = float(self.request.get('longitude', None))
            center = db.GeoPt(latitude, longitude)
            radius = int(self.request.get('radius'))
            expires = datetime.utcfromtimestamp(int(self.request.get('expires')))
            count = int(self.request.get('count', 1))
            desired = self.request.get('desired', 'yes') in ['yes', '1', 'true'] and True or False

            goal = Goal(name=name, center=center, radius=radius, expires=expires,
                    count=count, desired=desired, user=users.get_current_user())
            goal.put()
            self.response.write(dumps({'created': goal.key().id()}))
        except Exception, e:
            log.exception('Error creating a goal')
            self.response.write(dumps({'error': unicode(e)}))

    def get(self):
        return self.post()




