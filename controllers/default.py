import os


def index():
    message='Code Spardha'
    #form = SQLFORM(db.ocj_user_login).process()
    return locals()


def contests():
    # This page will shoes the current running contests
    rows = db(db.ocj_contests).select()
    return locals()


@auth.requires_login()
def contestpage():
    #This page will show the running contest problems

    #Get the contest name
    for f in db(db.ocj_contests.id == int(request.args[0])).select():
        contestName = f.ContestName

    # Get the current problems and show it to user
    rows = db(db.ocj_contests_questions_1.ContestID == int(request.args[0])).select()

    # This will return the all the submission of the current contest
    logs = db(db.ocj_contests_log).select()
    return locals()



@auth.requires_login()
def challenges():
    #This function will display the question text
    for f in db(db.ocj_contests_questions_1.id == request.args[0]).select():
        QuestionText = f.QuestionText
        QuestionName = f.QuestionName

    #Set the current time stamp
    db.ocj_contests_log.UploadTime.default = request.now
    db.ocj_contests_log.UploadTime.writable = False
    db.ocj_contests_log.UploadTime.readable = False

    #Set the current logged in user
    db.ocj_contests_log.UserID.default = auth.user_id
    db.ocj_contests_log.UserID.writable = False
    db.ocj_contests_log.UserID.readable = False

    #Set the current question number
    db.ocj_contests_log.QueNo.default = request.args[0]
    db.ocj_contests_log.QueNo.writable = False
    db.ocj_contests_log.QueNo.readable = False

    form = SQLFORM(db.ocj_contests_log).process()
    logs = db(db.ocj_contests_log).select()
    return locals()




@auth.requires_membership('host_admin')
def manage():
    grid = SQLFORM.grid(db.ocj_contests)
    return locals()



#This view will be used for hosting the contest
def hostcontest():
    session.wasOnAddContestForm = 1
    #Set the current logged in user id as the hosted by user id
    return dict(form=SQLFORM(db.ocj_contests).process())

#This will be intermediate function for hosting the contest
def addcontest():
    
    """
    This session variable will check if any user directly landed on this page or not
    if he didnt come from last page then redirect him on the last page and ask to name the
    contest first
    """
    if session.wasOnAddContestForm != 1:
       redirect(URL('hostcontest'))    

    session.wasOnAddContestForm = 0
    """
    Get the varilable from the last page and inser it into the database and get the id in return
    """
    CName = request.vars['ContestName']
    ETime = request.vars['EndTime']
    STime = request.vars['StartTime']
    id = db.ocj_contests.insert(ContestName=CName, EndTime=ETime, StartTime=STime, HostedBy=auth.user_id)

    return locals()


def getFilePath():    
    record = db(db.ocj_contests_log.UserID == auth.user_id).select(orderby=~db.ocj_contests_log.UploadTime)[0]
    k = str(record['Code'])
    filePath = os.path.join(request.folder,'uploads',k)
    runStatus = os.system("g++ "+str(filePath))
    if runStatus == 0 :
        compilationStat = "Success"
    else:
        compilationStat = "Failure"
    return locals()


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
    http://..../[app]/default/user/bulk_register
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
