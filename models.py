from time import mktime

from json import dumps

from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel
from google.appengine.api import users



class Goal(db.Model):
    user = db.UserProperty(required=True)
    name = db.StringProperty(required=True)
    center = db.GeoPtProperty(required=True)
    radius = db.IntegerProperty(required=True, default=50)
    expires = db.DateTimeProperty(required=True)
    count = db.IntegerProperty(required=True, default=1, indexed=False)
    desired = db.BooleanProperty(required=True, default=True)

    def get_as_dict(self):
        return {'user': self.user.email(),
                'name': self.name,
                'center': unicode(self.center),
                'latitude': unicode(self.center.lat),
                'longitude': unicode(self.center.lon),
                'radius': self.radius,
                'expires': mktime(self.expires.timetuple()),
                'count': self.count,
                'desired': self.desired,
                'description': self.get_description(),
                'id': str(self.key().id())}

    def get_as_json(self):
        return dumps(self.get_as_dict())

    def get_description(self):
        if self.desired:
            if self.count > 1:
                return 'Go to %s at least %d times before %s' % (self.name,
                        self.count, unicode(self.expires))
            return 'Go to %s before %s' % (self.name, unicode(self.expires),)
        else:
            if self.count > 1:
                return 'Do not go to %s more than %d times before %s' % (self.name,
                        self.count - 1, unicode(self.expires))
        return 'Do not go to %s before %s' % (self.name,
                unicode(self.expires),)


    @property
    def map_color(self):
        if self.desired:
            return '#00FF00'
        else:
            return '#FF0000'

class GoalTriggered(db.Model):
    goal = db.ReferenceProperty(Goal, required=True)
    when = db.DateTimeProperty(required=True)

class Action(PolyModel):
    goal = db.ReferenceProperty(Goal, required=True)
    triggered = db.BooleanProperty(required=True, default=False)

class SMSAction(Action):
    phone = db.PhoneNumberProperty(required=True, indexed=False)

class FacebookAction(Action):
    pass

class TwitterAction(Action):
    pass

class EmailAction(Action):
    recipient = db.EmailProperty(required=True, indexed=False)

class DonateAction(Action):
    charity = db.StringProperty(required=True, indexed=False)

