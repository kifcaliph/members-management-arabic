# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(IMG(_src=URL('static', 'images/mylogo.jpg'), _class="customlogo"))
response.title = "برنامج الأعضاء"
response.subtitle = ''



## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('الرئيسية'), False, URL('default', 'index'), []),
    (T('عضو جديد'), False, URL('default', 'new_member'), []),
    (T('تسجيل إشتراك'), False, URL('default', 'new_payment'), []),
    (T('نوع إشتراك'), False, URL('default', 'new_event'), []),
    (T('بحث'), False, URL('default', 'search_member'), []),
    (T('أعضاء بلا إشتراك'), False, URL('default', 'mem_nopay'), []),
    (T('تقارير'), False, URL('default', 'reporting'), []),
    (T('المشرف العام'), False, URL('default', 'AdminPanel'), [])
    ]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
  
    
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
