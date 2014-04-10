# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://member.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('travels',
                Field('name', 'string'),
                Field('event_date', 'date', default = request.now, requires=[IS_NOT_EMPTY(),IS_DATE(format=('%Y-%m-%d'))]),
                format = '%(name)s')

db.define_table('members',
                 Field('Name', 'string',unique=True, requires=IS_NOT_EMPTY(), notnull=True),
                 Field('Job', 'string', requires=IS_NOT_EMPTY(), notnull=True, default="غير محدد"),
                 Field('Sex_type', 'string', requires=IS_IN_SET(["ذكر" , "أنثي", "غير محدد"])),
                 Field('Date_of_birth', 'date', requires=IS_NOT_EMPTY(), notnull=True),
				 Field('Membership_ID', 'string', requires=IS_NOT_EMPTY(), notnull=True),
                 Field('Membership_type', 'string', requires=IS_IN_SET(["عامل" , "منتسب", "فخري","غير محدد"])),
				 Field('Membership_category', 'string', requires=IS_IN_SET(["عائلي", "فردي", "غير محدد"])),
				 Field('Start_Date', 'date', default = request.now, requires=[IS_NOT_EMPTY(),IS_DATE(format=('%Y-%m-%d'))]),
				 Field('Home_Phone', 'integer'),
				 Field('Work_Phone', 'integer'),
				 Field('Cell_Phone', 'integer'),
				 Field('Email', 'string'),
				 Field('Home_Address', 'string'),
				 Field('Work_address', 'string'),
                 Field('ID_type', 'string', requires=IS_IN_SET(["رقم قومي", "باسبور", "غير محدد"])),
				 Field('National_Id_or_passport', 'integer'),
				 Field('Issued_from', 'string'),
				 Field('Notes','text'),
				 format = '%(Name)s')

db.define_table('payments',
                Field('Code_id', 'integer'),
                Field('Payment_Date', 'date', default = request.now, requires=[IS_NOT_EMPTY(),IS_DATE(format=('%Y-%m-%d'))]),
                Field('Payment_category', db.travels),
                Field('ammout', 'integer'),
                Field('Name', db.members),
                Field('Notes','text'),
                format = '%(Payment_category)s')
