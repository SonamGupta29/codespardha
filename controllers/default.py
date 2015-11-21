import os
import commands



def index():
    message='This is the landing form after login not the dashboard'
    session.userName = db(db.auth_user == auth.user_id).select(db.auth_user.first_name)[0].first_name

    session.handle = db(db.auth_user == auth.user_id).select(db.auth_user.handle)[0].handle
    #form = SQLFORM(db.ocj_user_login).process()
    return locals()


@auth.requires_login()
def showTimeline():
    activity = db(db.ocj_contests_log.userID == auth.user_id).select(orderby=~db.ocj_contests_log.submissionTime)
    return locals()


@auth.requires_login()
def home():
    message='Code Spardha'

    activity = db(db.ocj_contests_log.userID == auth.user_id).select(orderby=~db.ocj_contests_log.submissionTime)[:3]

    submissionCount = len(db(db.ocj_contests_log.userID == auth.user_id).select())

    successfulCount = len(db((db.ocj_contests_log.userID == auth.user_id) & (db.ocj_contests_log.submissionResult=="Accepted")).select())

    wrongAnswerCount = len(db((db.ocj_contests_log.userID == auth.user_id) & (db.ocj_contests_log.submissionResult=="Wrong Answer")).select())

    compileErrorCount = len(db((db.ocj_contests_log.userID == auth.user_id) & (db.ocj_contests_log.submissionResult=="Compile Time Error")).select())

    TLECount = len(db((db.ocj_contests_log.userID == auth.user_id) & (db.ocj_contests_log.submissionResult=="Time Limit Exceeded")).select())

    segmentationFaultCount = len(db((db.ocj_contests_log.userID == auth.user_id) & (db.ocj_contests_log.submissionResult=="Segmentation Fault")).select())

    runTimeErrorCount = len(db((db.ocj_contests_log.userID == auth.user_id) & (db.ocj_contests_log.submissionResult=="Run Time Error")).select())



    #form = SQLFORM(db.ocj_user_login).process()
    return locals()

def contests():
    # This page will shoes the current running contests
    runningContests = db((db.ocj_contests.startTime < request.now)& \
                         (db.ocj_contests.endTime > request.now)).select()

    upcomingContest = db(db.ocj_contests.startTime > request.now).select()

    return locals()


@auth.requires_login()
def contestpage():
    #This page will show the running contest problems

    #Get the contest name
    for f in db(db.ocj_contests.id == int(request.args[0])).select():
        cName = f.contestName

    # Get the current problems and show it to user
    rows = db(db.ocj_contests_questions.contestID == int(request.args[0])).select()

    # This will return the all the submission of the current contest
    logs = db(db.ocj_contests_log.contestID == int(request.args[0])).select(orderby=~db.ocj_contests_log.submissionTime)

    success = len(db((db.ocj_contests_log.contestID == int(request.args[0])) &\
                 (db.ocj_contests_log.submissionResult == "Accepted")).select())

    attempted = len(db((db.ocj_contests_log.contestID == int(request.args[0]))).select())

    if attempted == 0 :
        successPercentage = 0
    else :
        successPercentage = (success*100) / attempted
    
    return locals()



@auth.requires_login()
def challenges():

    session.isFromChallengesPage = 1
    #This function will display the question text
    for f in db(db.ocj_contests_questions.contestID == request.args[0]).select():
        QuestionText = f.questionText
        QuestionName = f.questionName

    #Set the current time stamp
    db.ocj_contests_log.submissionTime.default = request.now
    db.ocj_contests_log.submissionTime.writable = False
    db.ocj_contests_log.submissionTime.readable = False

    #Set the current logged in user
    db.ocj_contests_log.userID.default = auth.user_id
    db.ocj_contests_log.userID.writable = False
    db.ocj_contests_log.userID.readable = False

    #Set the current contest id
    db.ocj_contests_log.contestID.default = request.args[0]
    db.ocj_contests_log.contestID.writable = False
    db.ocj_contests_log.contestID.readable = False

    #Set the current question no
    db.ocj_contests_log.questionNumber.default = request.args[1]
    db.ocj_contests_log.questionNumber.writable = False
    db.ocj_contests_log.questionNumber.readable = False

    #Set the current Submission result as evaluating
    db.ocj_contests_log.submissionResult.default = 'Evaluating'
    db.ocj_contests_log.submissionResult.writable = False
    db.ocj_contests_log.submissionResult.readable = False

    #Set the current Submission result as evaluating
    db.ocj_contests_log.questionName.default = request.args[2]
    db.ocj_contests_log.questionName.writable = False
    db.ocj_contests_log.questionName.readable = False

    # This will show the question submission log
    form = SQLFORM(db.ocj_contests_log).process()
    logs = db((db.ocj_contests_log.contestID == int(request.args[0])) & \
                (db.ocj_contests_log.questionNumber == int(request.args[1]))).\
                select(orderby=~db.ocj_contests_log.submissionTime)

    contestID = request.args[0]
    questionNumber = request.args[1]
    if form.accepted:
        redirect(URL('processSubmission'))

    return locals()



#This function will be used to process the submission from here we can compile and run function
@auth.requires_login()
def processSubmission():

    qNumber = request.vars['questionNumber']
    cID = request.vars['contestID']
    cFile = request.vars['submissionFile']
    qName = request.vars['questionName']

    """
    Insert record in the log table and make the submission status as evaluating
    """
    """ 
    And this will only happen if the page is came from last page not refreshed, 
    coz page refresh will insert duplicate page
    """
    id = db.ocj_contests_log.insert(questionNumber = qNumber, contestID = cID, \
                                    code = cFile, questionName = qName, \
                                    userID = auth.user_id, submissionTime = request.now, \
                                    submissionResult = "Evaluating")

    CurrStatus = getFilePath()
    if session.isFromChallengesPage == 1:
        id = db.ocj_contests_log.insert(questionNumber = qNumber, contestID = cID, \
                                    code = cFile, questionName = qName, \
                                    userID = auth.user_id, submissionTime = request.now, \
                                    submissionResult = CurrStatus)
        session.isFromChallengesPage = 0



    rows = db((db.ocj_contests_log.contestID == cID) & \
                (db.ocj_contests_log.questionNumber == qNumber) &
                (db.ocj_contests_log.userID == auth.user_id)).\
                select(orderby=~db.ocj_contests_log.submissionTime)



    return locals()



@auth.requires_login()
@auth.requires_membership('host_admin')
def manage():
    grid = SQLFORM.grid(db.ocj_contests)
    return locals()


@auth.requires_login()
@auth.requires_membership('host_admin')
#This view will be used for hosting the contest
def hostcontest():
    session.wasOnAddContestForm = 1
    #Set the current logged in user id as the hosted by user id
    #return dict(form=SQLFORM(db.ocj_contests).process())

    logs = db(db.ocj_contests.hostedBy == int(auth.user_id)).select(orderby=~db.ocj_contests.startTime)





    return locals()


@auth.requires_login()
@auth.requires_membership('host_admin')
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
    CName = request.vars['contestName']
    ETime = request.vars['endTime']
    STime = request.vars['startTime']
    id = db.ocj_contests.insert(contestName=CName, endTime=ETime, startTime=STime, hostedBy=auth.user_id)

    return locals()


def addContestDetails():

    contestID = request.vars['contestID']
    questionNumber = request.vars['questionNumber']
    questionName = request.vars['questionName'] 
    questionText_1 = request.vars['questionText_1']
    noOfTestCases_1 = request.vars['noOfTestCases_1']
    testCase_1_1 = request.vars['testCase_1_1']
    testCaseAns_1_1 = request.vars['testCaseAns_1_1']

    id = db.ocj_contests_questions.insert(  contestID = contestID,   \
                                            questionNumber = questionNumber, \
                                            questionName = questionName, \
                                            questionText = questionText_1, \
                                            noOfTestCases = noOfTestCases_1, \
                                            testCase1 = testCase_1_1, \
                                            output1 = testCaseAns_1_1 )

    return locals()




def getFilePath():
    record = db(db.ocj_contests_log.userID == auth.user_id).select(orderby=~db.ocj_contests_log.submissionTime).first()
    questionId = record['questionNumber']
    contestId = record['contestID']
    recordfromques = db( (db.ocj_contests_questions.questionNumber == questionId)\
                                        & (db.ocj_contests_questions.contestID==contestId) ).select().first()
    testpathtemp = recordfromques['testCase1']
    testop = recordfromques['output1']
    k = record['code']
    filePath = os.path.join(request.folder,'uploads',k)
    testpath = os.path.join(request.folder,'uploads',testpathtemp)
    outputPath=os.path.join(request.folder,'uploads',testop)
    scriptPath = os.path.join(request.folder,'static/CodeJudge.sh')
    listRunStatus = list(commands.getstatusoutput("bash "+str(scriptPath)+" "+ str(filePath) +" "+ str(testpath) +" "+ str(outputPath) ))
    os.system("bash "+str(scriptPath)+" "+ str(filePath) +" "+ str(testpath) +" "+ str(outputPath) )
    runStatus = listRunStatus[1]

    if "CTE" in runStatus:
        CurrStatus = "Compile Time Error"
    elif "Segmentation" in runStatus :
        CurrStatus = "Segmentation Fault"
    elif "RTE" in runStatus :
        CurrStatus = "Run Time Error"
    elif "Wrong" in runStatus :
        CurrStatus = "Wrong Answer"
    elif "Accepted" in runStatus :
        CurrStatus = "Accepted"
    else:
        CurrStatus = "Time Limit Exceeded"
    #Update the Submission STatus of the submitted code
    #0-Success 1-CTE 2-RTE 3-TLE
    #row = db(db.ocj_contests_log.userID==auth.user_id).select(orderby=~db.ocj_contests_log.submissionTime).first()
    #row.update_record(submissionResult=CurrStatus)
    #return locals()
    return CurrStatus






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
