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
    response.flash = [T("Welcome to web2py!")]
    return dict(message=T('Hello World'))

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


def new_member():
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
    memID = None
    if request.args(0):
        memID = request.args(0)
        form = SQLFORM(db.payments, deletable=True, submit_button=T('تسجيل')).process(next=URL('update/db/members/' + str(memID)))
    else:
        form = SQLFORM(db.payments, deletable=True, submit_button=T('تسجيل')).process(next=URL('index'))
    return dict(form=form, memID=memID)

def new_event():
    form = SQLFORM(db.travels, deletable=True, submit_button=T('تسجيل')).process(next=URL('index'))
    return dict(form=form)

def search_member():
    results = []
    if request.vars.Name:
        value = str(request.vars.Name)
        results = db((db.members.Name.like('%'+ value +'%'))).select(db.members.id, db.members.Name, db.members.Date_of_birth, db.members.Cell_Phone)
    elif request.vars.Date_of_birth:
        value = request.vars.Date_of_birth
        results = db((db.members.Date_of_birth==value)).select(db.members.id, db.members.Name, db.members.Date_of_birth, db.members.Cell_Phone)
    elif request.vars.Membership_ID:
        value = request.vars.Membership_ID
        results = db((db.members.Membership_ID==value)).select(db.members.id, db.members.Name, db.members.Date_of_birth, db.members.Cell_Phone)
    elif request.vars.Home_Phone:
        value = str(request.vars.Home_Phone)
        results = db((db.members.Home_Phone==value)|(db.members.Work_Phone==value)|(db.members.Cell_Phone==value)).select(db.members.id, db.members.Name, db.members.Date_of_birth, db.members.Cell_Phone)
    elif request.vars.National_Id_or_passport:
        value = str(request.vars.National_Id_or_passport)
        results = db((db.members.National_Id_or_passport==value)).select(db.members.id, db.members.Name, db.members.Date_of_birth, db.members.Cell_Phone)
    return locals()
"""dict(results=results)"""



def update():
    memID = request.args(2)
    record = db.members(request.args(2))
    gRecord =(db.payments.member_name==request.args(2))
    form = SQLFORM(db.members, record,submit_button=T('تحديث')).process(next=URL('index'))
    grid = SQLFORM.grid(gRecord, fields=[db.payments.Code_id, db.payments.Payment_Date, db.payments.Payment_category, db.payments.ammout, db.payments.Notes], searchable=False, deletable=False, editable=False, details=False, create=False, csv=False, user_signature=False)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, grid=grid, memID=memID)

def mem_nopay():
    results = []
    firstPass_filt = []
    oplist = {}
    travels = db((db.travels.id>0)).select(db.travels.id, db.travels.name)
    for travel in travels:
        oplist[travel.id]=travel.name
    if request.vars.Payment_category:
        firstPass_filt = db((db.payments.Payment_category==request.vars.Payment_category)).select(db.payments.member_name)
        for row in firstPass_filt.render(): results.append(row.member_name)
        results = db(~db.members.Name.belongs(results)).select()
    return dict(results=results, oplist=oplist)


def AdminPanel():
    appName = str(request.application)
    return dict(appName=appName)
