#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from os.path import dirname, join
import webapp2



config = {'jinja_templates': join(dirname(__file__),'templates')}

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', 'handlers.TemplateHandler', name='home'),
    webapp2.Route(r'/dashboard/', 'goals.Dashboard', name='dashboard'),

    webapp2.Route(r'/goals/create/', 'goals.Create', name='goals-create'),
], debug=True, config=config)
