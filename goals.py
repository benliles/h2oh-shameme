from datetime import datetime
from json import dumps
from logging import getLogger

from google.appengine.api import users
from google.appengine.ext import db

from handlers import ApiHandler, TemplateHandler
from models import Goal



log = getLogger('goal_shame.goals')

class Dashboard(TemplateHandler):
    template = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['goals'] = Goal.all().filter('user =', users.get_current_user())
        log.info('Found %d goals' % (context['goals'].count(),))
        return context

class List(ApiHandler):
    def get(self):
        self.response.write(dumps([goal.get_as_dict() for goal in
                Goal.all().filter('user =', self.get_current_user())]))

class Create(ApiHandler):
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
            log.info('Created a new goal: %s' % (goal.key().id(),))
            self.response.write(dumps({'created': str(goal.key().id())}))
        except Exception, e:
            log.exception('Error creating a goal')
            self.response.write(dumps({'error': unicode(e)}))

class GoalHandler(ApiHandler):
    def get(self, id, *args, **kwargs):
        log.info('Getting a goal: %s' % (id,))
        goal = Goal.get_by_id(int(id))
        if goal is None:
            self.response.write(dumps({'error': 'invalid id: %s' % (id,)}));
            return
        self.response.write(dumps(goal.get_as_dict()))


    def post(self, id, *args, **kwargs):
        log.info('Posting a goal update for %s of %s' % (id,
            unicode(self.request.POST),))
        goal = Goal.get_by_id(int(id))
        if goal is None:
            self.response.write(dumps({'error': 'invalid id: %s' % (id,)}))
            return

        try:
            if 'name' in self.request.POST:
                goal.name = self.request.get('name')
            if 'latitude' in self.request.POST:
                goal.center.lat = float(self.request.get('latitude'))
            if 'longitude' in self.request.POST:
                goal.center.lon = float(self.request.get('longitude'))
            if 'radius' in self.request.POST:
                goal.radius = int(self.request.get('radius'))
            if 'expires' in self.request.POST:
                goal.expires = \
                    datetime.utcfromtimestamp(int(self.request.get('expires')))
            if 'count' in self.request.POST:
                goal.count = int(self.request.get('count'))
            if 'desired' in self.request.POST:
                goal.desired = self.request.get('desired') in \
                    ['yes','1','true'] and True or False
            goal.put()
            self.response.write(dumps({'updated': goal.key().id()}))
        except Exception, e:
            log.exception('Error updating a goal')
            self.response.write(dumps({'error': unicode(e)}))





