from time import mktime

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
                'radius': self.radius,
                'expires': mktime(self.expires.timetuple()),
                'count': self.count,
                'desired': self.desired}

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

