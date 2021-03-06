# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################
if auth.is_logged_in():
    refstring = "http://127.0.0.1:8000/OCJ/default/home"
else:
    refstring = "http://127.0.0.1:8000/OCJ/default/index"

response.logo = A(B('Code Spardha'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href=refstring,
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'home'), []),
    (T('Running Contests'), False, URL('default', 'contests')),
]

if auth.user:
    groups = db((db.auth_membership.user_id==auth.user.id)&(db.auth_membership.group_id==db.auth_group.id)).select(db.auth_group.role)
    for group in groups:
        if group.role =='host_admin':
            response.menu.append(('Host/Manage Contests', False, URL('hostcontest')))


if "auth" in locals(): auth.wikimenu()
