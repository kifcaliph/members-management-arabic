# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from gluon.contrib.user_agent_parser import mobilize
from datetime import date

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = [T("Welcome to web2py!")]
    return dict(message=T('Hello World'))

def search_membername():
    partialstr = request.vars.values()[0]
    query = db.members.Name.like('%'+partialstr+'%')
    members_name = db(query).select(db.members.Name)
    items = []
    for (i,member) in enumerate(members_name):
        items.append(DIV(A(member.Name, _id="res%s"%i, _href="#", _onclick="copyToBox($('#res%s').html())"%i), _id="resultLiveSearch"))

    return TAG[''](*items)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def new_user():
    """
    creating the custom form in the website
    """
    form = SQLFORM(db.members, deletable=True, submit_button=T('تسجيل')).process(next=URL('index'))
    """form.add_button('إلغاء', URL('index'))"""
    return dict(form=form)

def reporting():
    form, results = crud.search(db.members)
    return dict(form=form, results=results)

def new_payment():
    form = SQLFORM(db.payments, deletable=True, submit_button=T('تسجيل')).process(next=URL('index'))
    return dict(form=form)

def new_event():
    form = SQLFORM(db.travels, deletable=True, submit_button=T('تسجيل')).process(next=URL('index'))
    return dict(form=form)
