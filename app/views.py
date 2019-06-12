#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template import RequestContext as RC
from django.template import Context, loader
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate,get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.db.models import Avg
from app.models import File, CSVs
from app.models import Organization, OrganizationHash, Coder
from app.models import Discuss, Stats
from app.forms import UploadFileForm, UserForm, NewUserForm, UrlForm
from app.forms import OrganizationForm, OrganizationHashForm
from app.forms import TeacherForm, LoginOrganizationForm
from app.forms import CoderForm, LoginCoderForm
from app.forms import DiscussForm
from app import org
from app import translation
from app import trans
from app import pyploma
from django.contrib.auth.models import User
from datetime import datetime,timedelta,date
from django.contrib.auth.decorators import login_required
from email.MIMEText import MIMEText
from django.utils.encoding import smart_str
from django.utils.translation import activate
from zipfile import ZipFile
import smtplib
import email.utils
import os
import ast
import json
import sys
import urllib2
import shutil
import unicodedata
import csv
import zipfile
from zipfile import ZipFile
from django.shortcuts import render
import analyzer
import spriteNaming
import backdropNaming
import duplicateScripts
import deadCode


###############################################################################
#                             MAIN PAGE                                       #
###############################################################################

#________________________________ MAIN _______________________________________#


def main(request):
    """Main page"""

    
    # The first time one user enters
    # Create the dashboards associated to users
    flagUser = 0
    if request.user.is_authenticated():
        username = request.user.username
        #Find which is authenticated (organization or coder or none)
        page = segmentation(request)
        if page == 'coder':
            user = Coder.objects.get(username=username)
        elif page == 'organization':
            user = Organization.objects.get(username=username)
        img = user.img
        dic={'username':username,
        "img":str(img)}
        return render(request, page + '/main.html', dic)

    else:
        username = None
        #Show main page of Dr. Scratch: www.drscratch.org/
        return render(request, 'main/main.html', {'username': username})



#______________________________ REDIRECT _____________________________________#

def redirect_main(request):
    """Page not found: redirect to main"""


    #Show main page of Dr. Scratch: www.drscratch.org/
    return HttpResponseRedirect('/')



#_______________________________ CONTEST _____________________________________#

def contest(request):
    """Shows pages for contests"""


    #Show pages for contestest of Dr. Scratch: www.drscratch.org/contest

    return render(request, 'contest.html', {})

#_______________________________ COLLABORATORS _______________________________#

def collaborators(request):
    """Shows collaborators page"""


    #Show collaborators page of Dr. Scratch: www.drscratch.org/collaborators
    #return render_to_response("main/collaborators.html",)
    return render(request, 'main/collaborators.html')


#____________________________ GENERAL STATISTICS _____________________________#

def date_range(start, end):
    """Initialization of ranges"""


    r = (end+timedelta(days=1)-start).days

    return [start+timedelta(days=i) for i in range(r)]

def statistics(request):
    """Initializing variables"""


    start = date(2019,1,1)
    end = datetime.today()
    y = end.year
    m = end.month
    d = end.day
    end = date(y,m,d)
    dateList = date_range(start, end)
    mydates=[]
    for n in dateList:
        mydates.append(n.strftime("%d/%m")) #used for x axis in

    #This final section stores all data for the template
    obj= Stats.objects.order_by("-id")[0]
    data = {"date":mydates,
             "dailyRate":obj.daily_score,
             "levels":{"basic":obj.basic,
                     "development":obj.development,
                     "master":obj.master},
             "totalProjects":obj.daily_projects,
             "skillRate":{"parallelism":obj.parallelism,
                          "abstraction":obj.abstraction,
                          "logic": obj.logic,
                          "synchronization":obj.synchronization,
                          "flowControl":obj.flowControl,
                          "userInteractivity":obj.userInteractivity,
                          "dataRepresentation":obj.dataRepresentation},
             "codeSmellRate":{"deadCode":obj.deadCode,
                              "duplicateScript":obj.duplicateScript,
                              "spriteNaming":obj.spriteNaming,
                              "initialization":obj.initialization }}

    #Show general statistics page of Dr. Scratch: www.drscratch.org/statistics
    #return render_to_response("main/statistics.html",
    #                                data, context_instance=RC(request))
    return render(request, 'main/statistics.html', data)



#_____________________________ SHOWS DASHBOARDS ______________________________#

def show_dashboard(request):
    """Shows the different dashboards"""


    if request.method == 'POST':
        error = False
        id_error = False
        no_exists = False

        #Analyze the project and looking for errors
        d = selector(request)
        #Find which is authenticated (organization or coder or none)
        user = str(segmentation(request))

        #Find if any error has occurred
        if d['Error'] == 'analyzing':
            return render(request, 'error/analyzing.html')

        elif d['Error'] == 'MultiValueDict':
            error = True
            return render(request, user + '/main.html', {'error':error})

        elif d['Error'] == 'id_error':
            id_error = True
            return render(request, user + '/main.html', {'id_error':id_error})

        elif d['Error'] == 'no_exists':
            no_exists = True
            return render(request, user + '/main.html', {'no_exists':no_exists})

        #Show the dashboard according the CT level
        else:
            if d["mastery"]["points"] >= 15:
                #Show master dashboard: www.drscratch.org/show_dashboard
                return render(request, user + '/dashboard-master.html', d)

            elif d["mastery"]["points"] > 7:
                #Show developing dashboard: www.drscratch.org/show_dashboard
                return render(request, user + '/dashboard-developing.html', d)

            else:
                #Show basic dashboard: www.drscratch.org/show_dashboard
                return render(request, user + '/dashboard-basic.html', d) 

    else:
        return HttpResponseRedirect('/')


def selector(request):
    """Choose between analysis by URL or project"""


    if "_upload" in request.POST:
        #Project uploaded from computer
        #Analyze by "upload" method
        d = _upload(request)
        if d['Error'] != 'None':
          return d
        filename = request.FILES['zipFile'].name.encode('utf-8')
        dic = {'url': "",'filename':filename}
        d.update(dic)

    elif '_url' in request.POST:
        #Project uploaded from Scratch's server
        #Analyze by "url" method
        d = _url(request)
        form = UrlForm(request.POST)
        url = request.POST['urlProject']
        filename = url
        dic = {'url': url, 'filename':filename}
        d.update(dic)

    return d

def segmentation(request):
    """Find which is authenticated (organization or coder or none)"""


    if request.user.is_authenticated():
        username = request.user.username
        if Organization.objects.filter(username = username.encode('utf-8')):
            user = 'organization'
        elif Coder.objects.filter(username = username.encode('utf-8')):
            user = 'coder'
    else:
        user = 'main'
    return user



###############################################################################
#                         PROJECT ANALYSIS                                    #
###############################################################################

#________________________________UPLOADED FILE________________________________#

def _upload(request):
    """Upload file from form POST for unregistered users"""


    if request.method == 'POST':
        #Revise the form in main
        #If user doesn't complete all the fields,it'll show a warning
        try:
            file = request.FILES['zipFile']
        except:
            d = {'Error': 'MultiValueDict'}
            return  d

        
        # Create DB of files
        now = datetime.now()
        method = "project"
        filename = File (filename = file.name.encode('utf-8'),
                        organization = "",
                        method = method , time = now,
                        score = 0, abstraction = 0, parallelization = 0,
                        logic = 0, synchronization = 0, flowControl = 0,
                        userInteractivity = 0, dataRepresentation = 0,
                        spriteNaming = 0 ,initialization = 0,
                        deadCode = 0, duplicateScript = 0)
        filename.save()

        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"

        #Build the id
        now = datetime.now()
        date = now.strftime("%Y_%m_%d_%H_%M_%S_")
        ms = now.microsecond

        project_name = str(filename.filename).split(".sb")[0]
        project_name = project_name.replace(" ", "_")

        unique_id = project_name + "_" + date + str(ms)

        # Version of Scratch 1.4Vs2.0Vs3.0
        version = check_version(filename.filename)
        if version == "1.4":
            fileSaved = dir_zips + unique_id + ".sb"
        elif version == "2.0":
            fileSaved = dir_zips + unique_id + ".sb2"
        else:
            fileSaved = dir_zips + unique_id + ".sb3"

        # Create log
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(filename.filename) + "\t\t\t" + \
            "ID: " + str(filename.id) + "\t\t\t" + \
            "Method: " + str(filename.method) + \
            "\t\t\tTime: " + str(filename.time) + "\n")


       
        # Save file in server
        counter = 0
        file_name = handler_upload(fileSaved, counter)

        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)


        # Analyze the scratch project
        try:
            d = analyze_project(request, file_name, filename)
        except:
            #There ir an error with kutz or hairball
            #We save the project in folder called error_analyzing
            filename.method = 'project/error'
            filename.save()
            oldPathProject = fileSaved
            newPathProject = fileSaved.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             fileSaved.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}
            return d
        # Show the dashboard
        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'

        return d
    
    else:
        return HttpResponseRedirect('/')

#_______________________ANALYSIS BY PROJECT'S URL_____________________________#


def _url(request):
    """Process Request of form URL"""


    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            d = {}
            url = form.cleaned_data['urlProject']
            idProject = process_string_url(url)
            d = generator_dic(request,idProject)
            return d
        else:
            d = {'Error': 'MultiValueDict'}

            return  d
    else:

        return HttpResponseRedirect('/')


def process_string_url(url):
    """Process String of URL from Form"""


    idProject = ''
    auxString = url.split("/")[-1]
    if auxString == '':
        # we need to get the other argument
        possibleId = url.split("/")[-2]
        if possibleId == "editor":
            idProject = url.split("/")[-3]
        else:
            idProject = possibleId
    else:
        if auxString == "editor":
            idProject = url.split("/")[-2]
        else:
            # To get the id project
            idProject = auxString
    try:
        checkInt = int(idProject)
    except ValueError:
        idProject = "error"

    return idProject



def generator_dic(request, idProject):
    """Returns dictionary with analyzes and errors"""


    if idProject == "error":
        d = {'Error': 'id_error'}

        return d

    else:
        try:
            if request.user.is_authenticated():
                username = request.user.username
            else:
                username = None
            method = "url"
            (pathProject, file) = send_request_getSb3(idProject,
                                                      username, 
                                                      method)
        except:
            #When your project doesn't exist
            d = {'Error': 'no_exists'}

            return d


        try:
            d = analyze_project(request, pathProject, file)
        except:
            #There is an error with kutz or hairball
            #We save the project in folder called error_analyzing
            file.method = 'url/error'
            file.save()
            oldPathProject = pathProject
            newPathProject = pathProject.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             pathProject.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}

            return d

        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'

        return d



def new_getSb3(file_name, dir_zips,fileName):

    #Build the id
    now = datetime.now()
    date = now.strftime("%Y_%m_%d_%H_%M_%S_")
    ms = now.microsecond

    project_name = str(fileName.filename).split(".sb")[0]

    unique_id = project_name + "_" + date + str(ms)


    if zipfile.is_zipfile(file_name):
        os.rename(dir_zips + "project.json",dir_zips + unique_id + ".sb3")
    else:
        current = os.getcwd()
        os.chdir(dir_zips)
        with ZipFile(unique_id + ".sb3", 'w') as myzip:
            myzip.write("project.json")
        os.chdir(current)
        try:
            os.remove(dir_zips + "project.json")
        except:
            print "No existe"

    file_name = dir_zips + unique_id + ".sb3"
   
    return file_name




def send_request_getSb3(idProject, username, method):
    """First request to getSb3"""


    try:
        os.remove(dir_zips + "project.json")
    except:
        print "No existe"

    getRequestSb3 = "https://projects.scratch.mit.edu/" + idProject + "/get"
    fileURL = idProject + ".sb3"

    # Create DB of files
    now = datetime.now()

    if Organization.objects.filter(username=username):
        fileName = File (filename = fileURL,
                         organization = username,
                         method = method , time = now,
                         score = 0, abstraction = 0, parallelization = 0,
                         logic = 0, synchronization = 0, flowControl = 0,
                         userInteractivity = 0, dataRepresentation = 0,
                         spriteNaming = 0 ,initialization = 0,
                         deadCode = 0, duplicateScript = 0)
    elif Coder.objects.filter(username = username):
        fileName = File (filename = fileURL,
                         coder = username,
                         method = method , time = now,
                         score = 0, abstraction = 0, parallelization = 0,
                         logic = 0, synchronization = 0, flowControl = 0,
                         userInteractivity = 0, dataRepresentation = 0,
                         spriteNaming = 0 ,initialization = 0,
                         deadCode = 0, duplicateScript = 0)
    else:
        fileName = File (filename = fileURL,
                         method = method , time = now,
                         score = 0, abstraction = 0, parallelization = 0,
                         logic = 0, synchronization = 0, flowControl = 0,
                         userInteractivity = 0, dataRepresentation = 0,
                         spriteNaming = 0 ,initialization = 0,
                         deadCode = 0, duplicateScript = 0)
    
    fileName.save()
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    fileSaved = dir_zips + "project.json"

    #Write the activity in log
    pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    logFile = open (pathLog + "logFile.txt", "a")
    logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
        str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + \
        "\t\t\t" + "Time: " + str(fileName.time) + "\n")

    
    # Save file in server
    counter = 0

    file_name = handler_upload(fileSaved, counter)
    outputFile = open(file_name, 'wb')
    try:
        sb3File = urllib2.urlopen(getRequestSb3)
        outputFile.write(sb3File.read())
        outputFile.close()
    except:
        outputFile.write("ERROR downloading")
        outputFile.close()
    

    #New getSb3
    file_name = new_getSb3(file_name, dir_zips,fileName)
    

    return (file_name, fileName)



#____________________________HANDLER UPLOAD FILE______________________________#


def handler_upload(fileSaved, counter):
    """ Necessary to uploadUnregistered: rename projects"""


    # If file exists,it will save it with new name: name(x)
    if os.path.exists(fileSaved):
        counter = counter + 1
        #Check the version of Scratch 1.4Vs2.0Vs3.0
        version = check_version(fileSaved)
        if version == "3.0":
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb3"
            else:
                fileSaved = fileSaved.split('(')[0] + \
                    "(" + str(counter) + ").sb3"
        elif version == "2.0":
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb2"
            else:
                fileSaved = fileSaved.split('(')[0] + \
                    "(" + str(counter) + ").sb2"
        else:
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb"
            else:
                fileSaved = fileSaved.split('(')[0] + \
                    "(" + str(counter) + ").sb"

        file_name = handler_upload(fileSaved, counter)

        return file_name

    else:
        file_name = fileSaved


        return file_name



def check_version(filename):
    """Check the version of the project and return it"""

    extension = filename.split('.')[-1]
    if extension == 'sb2':
        version = '2.0'
    elif extension == 'sb3':
        version = '3.0'
    else:
        version = '1.4'

    return version



#________________________ AUTOMATIC ANALYSIS _________________________________#

def analyze_project(request, file_name, filename):


    dictionary = {}
    
    if os.path.exists(file_name):
        
        list_file = file_name.split('(')
       
        #if len(list_file) > 1:
        #    file_name = list_file[0] + '\(' + list_file[1]
        #    list_file = file_name.split(')')
        #    file_name = list_file[0] + '\)' + list_file[1]


        resultMastery = analyzer.main(file_name)
        resultSpriteNaming = spriteNaming.main(file_name)
        resultBackdropNaming = backdropNaming.main(file_name)
        resultDuplicateScript = duplicateScripts.main(file_name)
        resultDeadCode = deadCode.main(file_name)


        #Create a dictionary with necessary information
        dictionary.update(proc_mastery(request,resultMastery, filename))
        dictionary.update(proc_sprite_naming(resultSpriteNaming, filename))
        dictionary.update(proc_backdrop_naming(resultBackdropNaming, filename))
        dictionary.update(proc_duplicate_script(resultDuplicateScript, filename))
        dictionary.update(proc_dead_code(resultDeadCode, filename))
        #dictionary.update(proc_initialization(resultInitialization, filename))
        #code = {'dupCode':duplicate_script_scratch_block(resultDuplicateScript)}
        #dictionary.update(code)
        #code = {'dCode':dead_code_scratch_block(resultDeadCode)}
        #dictionary.update(code)

        return dictionary

    else:
        return HttpResponseRedirect('/')


# _______________________________ PROCESSORS _________________________________#

def proc_mastery(request,lines, filename):
    """Returns the information of Mastery"""

    dic = {}
    lLines = lines.split('\n')
    d = {}
    d = ast.literal_eval(lLines[1])
    lLines = lLines[2].split(':')[1]
    points = int(lLines.split('/')[0])
    maxi = int(lLines.split('/')[1])

    #Save in DB
    filename.score = points
    filename.abstraction = d["Abstraction"]
    filename.parallelization = d["Parallelization"]
    filename.logic = d["Logic"]
    filename.synchronization = d["Synchronization"]
    filename.flowControl = d["FlowControl"]
    filename.userInteractivity = d["UserInteractivity"]
    filename.dataRepresentation = d["DataRepresentation"]
    filename.save()

    #Translation
    d_translated = translate(request,d, filename)

    dic["mastery"] = d_translated
    dic["mastery"]["points"] = points
    dic["mastery"]["maxi"] = maxi

    return dic


def proc_duplicate_script(lines, filename):


    dic = {}
    number = 0
    lLines = lines.split('\n')
    #if len(lLines) > 2:
    number = lLines[0][0]
    dic["duplicateScript"] = dic
    dic["duplicateScript"]["number"] = number

    #Save in DB
    filename.duplicateScript = number
    filename.save()

    return dic


def proc_sprite_naming(lines, filename):

    dic = {}
    lLines = lines.split('\n')
    number = lLines[0].split(' ')[0]
    lObjects = lLines[1:]
    lfinal = lObjects[:-1]
    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = str(number)
    dic['spriteNaming']['sprite'] = lfinal

    #Save in DB
    filename.spriteNaming = str(number)
    filename.save()

    return dic


def proc_backdrop_naming(lines, filename):

    dic = {}
    lLines = lines.split('\n')
    number = lLines[0].split(' ')[0]
    lObjects = lLines[1:]
    lfinal = lObjects[:-1]
    dic['backdropNaming'] = dic
    dic['backdropNaming']['number'] = str(number)
    dic['backdropNaming']['backdrop'] = lfinal

    #Save in DB
    filename.backdropNaming = str(number)
    filename.save()

    return dic



def proc_dead_code(lines, filename):
    
    dic = {}
    dead_code = lines.split("\n")[1:]
    iterator = 0
    lcharacter = []
    lblocks = []
    if dead_code:
      d = ast.literal_eval(dead_code[0])
      keys = d.keys()
      values = d.values()
      items = d.items()

      for keys, values in items:
	lcharacter.append(keys)
	lblocks.append(values) 
	iterator += 1

    dic = {}
    dic["deadCode"] = dic
    dic["deadCode"]["number"] = iterator
    number = len(lcharacter)
    for i in range(number):
        dic["deadCode"][str(lcharacter[i])] = str(lblocks[i])

    #Save in DB
    filename.deadCode = iterator
    filename.save()

    return dic


"""
def proc_initialization(lines, filename):


    dic = {}
    lLines = lines.split('.sb2')
    d = ast.literal_eval(lLines[1])
    keys = d.keys()
    values = d.values()
    items = d.items()
    number = 0

    for keys, values in items:
        list = []
        attribute = ""
        internalkeys = values.keys()
        internalvalues = values.values()
        internalitems = values.items()
        flag = False
        counterFlag = False
        i = 0
        for internalkeys, internalvalues in internalitems:
            if internalvalues == 1:
                counterFlag = True
                for value in list:
                    if internalvalues == value:
                        flag = True
                if not flag:
                    list.append(internalkeys)
                    if len(list) < 2:
                        attribute = str(internalkeys)
                    else:
                        attribute = attribute + ", " + str(internalkeys)
        if counterFlag:
            number = number + 1
        d[keys] = attribute
    dic["initialization"] = d
    dic["initialization"]["number"] = number

    #Save in DB
    filename.initialization = number
    filename.save()

    return dic



#____________________  INFORMATION TO SCRATCH BLOCKS  ________________________#

def duplicate_script_scratch_block(code):


    try:
        code = code.split("\n")[2:][0]
        code = code[1:-1].split(",")
    except:
        code = ""

    return code

def dead_code_scratch_block(code):


    try:
        code = code.split("\n")[2:-1]
        for n in code:
            n = n[15:-2]
    except:
        code = ""
    return code

"""

# ______________________________ TRANSLATE MASTERY ___________________________#

def translate(request,d, filename):
    """Translate the output of Hairball"""


    if request.LANGUAGE_CODE == "es":
        d_translate_es = {}
        d_translate_es['Abstracción'] = d['Abstraction']
        d_translate_es['Paralelismo'] = d['Parallelization']
        d_translate_es['Pensamiento lógico'] = d['Logic']
        d_translate_es['Sincronización'] = d['Synchronization']
        d_translate_es['Control de flujo'] = d['FlowControl']
        d_translate_es['Interactividad con el usuario'] = d['UserInteractivity']
        d_translate_es['Representación de la información'] = d['DataRepresentation']
        filename.language = "es"
        filename.save()
        return d_translate_es
    elif request.LANGUAGE_CODE == "en":
        d_translate_en = {}
        d_translate_en['Abstraction'] = d['Abstraction']
        d_translate_en['Parallelism'] = d['Parallelization']
        d_translate_en['Logic'] = d['Logic']
        d_translate_en['Synchronization'] = d['Synchronization']
        d_translate_en['Flow control'] = d['FlowControl']
        d_translate_en['User interactivity'] = d['UserInteractivity']
        d_translate_en['Data representation'] = d['DataRepresentation']
        filename.language = "en"
        filename.save()
        return d_translate_en
    elif request.LANGUAGE_CODE == "ca":
        d_translate_ca = {}
        d_translate_ca['Abstracció'] = d['Abstraction']
        d_translate_ca['Paral·lelisme'] = d['Parallelization']
        d_translate_ca['Lògica'] = d['Logic']
        d_translate_ca['Sincronització'] = d['Synchronization']
        d_translate_ca['Controls de flux'] = d['FlowControl']
        d_translate_ca["Interactivitat de l'usuari"] = d['UserInteractivity']
        d_translate_ca['Representació de dades'] = d['DataRepresentation']
        filename.language = "ca"
        filename.save()
        return d_translate_ca
    elif request.LANGUAGE_CODE == "gl":
        d_translate_gl = {}
        d_translate_gl['Abstracción'] = d['Abstraction']
        d_translate_gl['Paralelismo'] = d['Parallelization']
        d_translate_gl['Lóxica'] = d['Logic']
        d_translate_gl['Sincronización'] = d['Synchronization']
        d_translate_gl['Control de fluxo'] = d['FlowControl']
        d_translate_gl["Interactividade do susario"] = d['UserInteractivity']
        d_translate_gl['Representación dos datos'] = d['DataRepresentation']
        filename.language = "gl"
        filename.save()
        return d_translate_gl

    elif request.LANGUAGE_CODE == "pt":
        d_translate_pt = {}
        d_translate_pt['Abstração'] = d['Abstraction']
        d_translate_pt['Paralelismo'] = d['Parallelization']
        d_translate_pt['Lógica'] = d['Logic']
        d_translate_pt['Sincronização'] = d['Synchronization']
        d_translate_pt['Controle de fluxo'] = d['FlowControl']
        d_translate_pt["Interatividade com o usuário"] = d['UserInteractivity']
        d_translate_pt['Representação de dados'] = d['DataRepresentation']
        filename.language = "pt"
        filename.save()
        return d_translate_pt
    
    elif request.LANGUAGE_CODE == "el":
        d_translate_el = {}
        d_translate_el['Αφαίρεση'] = d['Abstraction']
        d_translate_el['Παραλληλισμός'] = d['Parallelization']
        d_translate_el['Λογική'] = d['Logic']
        d_translate_el['Συγχρονισμός'] = d['Synchronization']
        d_translate_el['Έλεγχος ροής'] = d['FlowControl']
        d_translate_el['Αλληλεπίδραση χρήστη'] = d['UserInteractivity']
        d_translate_el['Αναπαράσταση δεδομένων'] = d['DataRepresentation']
        filename.language = "el"
        filename.save()
        return d_translate_el

    elif request.LANGUAGE_CODE == "eu":           
        d_translate_eu = {}
        d_translate_eu['Abstrakzioa'] = d['Abstraction']
        d_translate_eu['Paralelismoa'] = d['Parallelization']
        d_translate_eu['Logika'] = d['Logic']
        d_translate_eu['Sinkronizatzea'] = d['Synchronization']
        d_translate_eu['Kontrol fluxua'] = d['FlowControl']
        d_translate_eu['Erabiltzailearen elkarreragiletasuna'] = d['UserInteractivity']
        d_translate_eu['Datu adierazlea'] = d['DataRepresentation']
        filename.language = "eu"
        filename.save()
        return d_translate_eu

    elif request.LANGUAGE_CODE == "it":           
        d_translate_it = {}
        d_translate_it['Astrazione'] = d['Abstraction']
        d_translate_it['Parallelismo'] = d['Parallelization']
        d_translate_it['Logica'] = d['Logic']
        d_translate_it['Sincronizzazione'] = d['Synchronization']
        d_translate_it['Controllo di flusso'] = d['FlowControl']
        d_translate_it['Interattività utente'] = d['UserInteractivity']
        d_translate_it['Rappresentazione dei dati'] = d['DataRepresentation']
        filename.language = "it"
        filename.save()
        return d_translate_it

    elif request.LANGUAGE_CODE == "ru":
        d_translate_ru = {}
        d_translate_ru['Абстракция'] = d['Abstraction']
        d_translate_ru['Параллельность действий'] = d['Parallelization']
        d_translate_ru['Логика'] = d['Logic']
        d_translate_ru['cинхронизация'] = d['Synchronization']
        d_translate_ru['Управление потоком'] = d['FlowControl']
        d_translate_ru['Интерактивность'] = d['UserInteractivity']
        d_translate_ru['Представление данных'] = d['DataRepresentation']
        filename.language = "ru"
        filename.save()
        return d_translate_ru


    else:
        d_translate_en = {}
        d_translate_en['Abstraction'] = d['Abstraction']
        d_translate_en['Parallelism'] = d['Parallelization']
        d_translate_en['Logic'] = d['Logic']
        d_translate_en['Synchronization'] = d['Synchronization']
        d_translate_en['Flow control'] = d['FlowControl']
        d_translate_en['User interactivity'] = d['UserInteractivity']
        d_translate_en['Data representation'] = d['DataRepresentation']
        filename.language = "any"
        filename.save()
        return d_translate_any

###############################################################################

###############################################################################

#_______________________________ LEARN MORE __________________________________#

def learn(request,page):
    """Shows pages to learn more about CT"""


    flagUser = 0
    #Unicode to string(page)


    if request.user.is_authenticated():
        user = request.user.username
        flagUser = 1

    if request.LANGUAGE_CODE == "en":
        dic = {u'Logic':'Logic',
               u'Parallelism':'Parallelism',
               u'Data':'Data',
               u'Synchronization':'Synchronization',
               u'User':'User',
               u'Flow':'Flow',
               u'Abstraction':'Abstraction'}


    elif request.LANGUAGE_CODE == "es":
        page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {'Pensamiento':'Logic',
               'Paralelismo':'Parallelism',
               'Representacion':'Data',
               'Sincronizacion':'Synchronization',
               'Interactividad':'User',
               'Control':'Flow',
               'Abstraccion':'Abstraction'}

    elif request.LANGUAGE_CODE == "ca":
        dic = {u'Logica':'Logic',
               u'Paral':'Parallelism',
               u'Representacio':'Data',
               u'Sincronitzacio':'Synchronization',
               u'Interactivitat':'User',
               u'Controls':'Flow',
               u'Abstraccio':'Abstraction'}

    elif request.LANGUAGE_CODE == "gl":
        page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {'Loxica':'Logic',
               'Paralelismo':'Parallelism',
               'Representacion':'Data',
               'Sincronizacion':'Synchronization',
               'Interactividade':'User',
               'Control':'Flow',
               'Abstraccion':'Abstraction'}

    elif request.LANGUAGE_CODE == "pt":
        page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {'Logica':'Logic',
               'Paralelismo':'Parallelism',
               'Representacao':'Data',
               'Sincronizacao':'Synchronization',
               'Interatividade':'User',
               'Controle':'Flow',
               'Abstracao':'Abstraction'}

    elif request.LANGUAGE_CODE == "el":
        dic = {u'Λογική':'Logic',
           u'Παραλληλισμός':'Parallelism',
           u'Αναπαράσταση':'Data',
           u'Συγχρονισμός':'Synchronization',
           u'Αλληλεπίδραση':'User',
           u'Έλεγχος':'Flow',
           u'Αφαίρεση':'Abstraction'}

    elif request.LANGUAGE_CODE == "eu":
        page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {u'Logika':'Logic',
           u'Paralelismoa':'Parallelism',
           u'Datu':'Data',
           u'Sinkronizatzea':'Synchronization',
           u'Erabiltzailearen':'User',
           u'Kontrol':'Flow',
           u'Abstrakzioa':'Abstraction'}

    elif request.LANGUAGE_CODE == "it":
        page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {u'Logica':'Logic',
           u'Parallelismo':'Parallelism',
           u'Rappresentazione':'Data',
           u'Sincronizzazione':'Synchronization',
           u'Interattivita':'User',
           u'Controllo':'Flow',
           u'Astrazione':'Abstraction'}

    elif request.LANGUAGE_CODE == "ru":
        dic = {u'Логика': 'Logic',
               u'Параллельность': 'Parallelism',
               u'Представление': 'Data',
               u'cинхронизация': 'Synchronization',
               u'Интерактивность': 'User',
               u'Управление': 'Flow',
               u'Абстракция': 'Abstraction'}

    else:
        dic = {u'Logica':'Logic',
               u'Paralelismo':'Parallelism',
               u'Representacao':'Data',
               u'Sincronizacao':'Synchronization',
               u'Interatividade':'User',
               u'Controle':'Flow',
               u'Abstracao':'Abstraction'}

    if page in dic:
        page = dic[page]
    

    page = "learn/" + page + ".html"

    if request.user.is_authenticated():
        #Find which is authenticated (organization or coder or none)
        user = segmentation(request)
        username = request.user.username
        #return render_to_response(page, {'flagUser':flagUser, 'user':user,
        #                                'username':username},
        #                        RC(request))
        return render(request, page, {'flagUser':flagUser, 'user':user, 'username':username})
    else:

        #return render_to_response(page,
        #                        RC(request))
        return render(request, page)



#_________________________DOWNLOAD CERTIFICATE________________________________#
def download_certificate(request):
    """Function to download your project's certificate"""


    if request.method == "POST":
        data = request.POST["certificate"]
        data = unicodedata.normalize('NFKD',data).encode('ascii','ignore')
        filename = data.split(",")[0]
        level = data.split(",")[1]
        if (request.LANGUAGE_CODE == 'es' or request.LANGUAGE_CODE == 'ca' or request.LANGUAGE_CODE == 'gl' or request.LANGUAGE_CODE == 'pt'):
            language = request.LANGUAGE_CODE
        else:
            language = 'en'
        pyploma.generate(filename,level,language)
        path_to_file = os.path.dirname(os.path.dirname(__file__)) + "/app/certificate/output.pdf"
        pdf_data = open(path_to_file, 'r')
        response = HttpResponse(pdf_data, content_type='application/pdf')
        try:
            file_pdf = filename.split("/")[-2] + ".pdf"
        except:
            file_pdf = filename.split(".")[0] + ".pdf"
        response['Content-Disposition'] = 'attachment; filename=%s' % file_pdf
        return response
    else:
        return HttpResponseRedirect('/')


#___________________________ ASYNCHRONOUS FORMS ______________________________#

def search_email(request):
    """Comfirm email"""


    if request.is_ajax():
        user = Organization.objects.filter(email=request.GET['email'])
        if user:
            return HttpResponse(json.dumps({"exist":"yes"}), 
                                content_type ='application/json')

def search_username(request):
    """Comfirm username"""


    if request.is_ajax():
        user = Organization.objects.filter(username=request.GET['username'])
        if user:
            return HttpResponse(json.dumps({"exist":"yes"}), 
                                content_type ='application/json')

def search_hashkey(request):
    """Comfirm hashkey"""


    if request.is_ajax():
        user = OrganizationHash.objects.filter(hashkey=request.GET['hashkey'])
        if not user:
            return HttpResponse(json.dumps({"exist":"yes"}), 
                                content_type ='application/json')

#____________________________ PLUG-INS _______________________________________#

def plugin(request,urlProject):
    """Analysis by plugin"""


    idProject = process_string_url(urlProject)
    d = generator_dic(request,idProject)
    #Find if any error has occurred
    if d['Error'] == 'analyzing':
        return render(request, user + '/error_analyzing.html')

    elif d['Error'] == 'MultiValueDict':
        error = True
        return render(request, user + '/main.html', {'error':error})

    elif d['Error'] == 'id_error':
        id_error = True
        return render(request, user + '/main.html', {'id_error':id_error})

    elif d['Error'] == 'no_exists':
        no_exists = True
        return render(request, user + '/main.html', {'no_exists':no_exists})

    #Show the dashboard according the CT level
    else:
        user = "main"
        base_dir = os.getcwd()
        if d["mastery"]["points"] >= 15:
            return render(request, user + '/dashboard-master.html', d)

        elif d["mastery"]["points"] > 7:
            return render(request, user + '/dashboard-developing.html', d)

        else:
            return render(request, user + '/dashboard-basic.html', d) 


#_____________________ TRANSLATION SCRATCHBLOCKS______________________________#

def blocks(request):
    """Translate blocks of Scratch shown in learn pages"""


    callback = request.GET.get('callback')
    headers = {}
    headers['Accept-Language'] = str(request.LANGUAGE_CODE)

    headers = json.dumps(headers)
    if callback:
        headers = '%s(%s)' % (callback, headers)
        return HttpResponse(headers, content_type="application/json")



#_____________________________ TO REGISTER ORGANIZATION ______________________#

def organization_hash(request):
    """Method for to sign up in the platform"""


    if request.method == "POST":
        form = OrganizationHashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/organization_hash')
    elif request.method == 'GET':
        return render(request, 'organization/organization-hash.html') 

    else:
        return HttpResponseRedirect('/')


def sign_up_organization(request):
    """Method which allow to sign up organizations"""


    flagOrganization = 1
    flagHash = 0
    flagName = 0
    flagEmail = 0
    flagForm = 0
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashkey = form.cleaned_data['hashkey']

            #Checking the validity into the database contents.
            #They will be refused if they already exist.
            #If they exist an error message will be shown.
            if User.objects.filter(username = username):
                #This name already exists
                flagName = 1
                return render(request, 'error/sign-up.html',
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm,
                                           'flagOrganization':flagOrganization})

            elif User.objects.filter(email = email):
                #This email already exists
                flagEmail = 1
                return render(request, 'error/sign-up.html',
                                        {'flagName':flagName,
                                        'flagEmail':flagEmail,
                                        'flagHash':flagHash,
                                        'flagForm':flagForm,
                                        'flagOrganization':flagOrganization})

            if (OrganizationHash.objects.filter(hashkey = hashkey)):
                organizationHashkey = OrganizationHash.objects.get(hashkey=hashkey)
                organization = Organization.objects.create_user(username = username, 
                                                            email=email, 
                                                            password=password, 
                                                            hashkey=hashkey)
                organizationHashkey.delete()
                organization = authenticate(username=username, password=password)
                user=Organization.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token=default_token_generator.make_token(user)
                c = {
                        'email':email,
                        'uid':uid,
                        'token':token}

                body = render_to_string("organization/email-sign-up.html",c)
                subject = "Welcome to Dr. Scratch for organizations"
                sender ="no-reply@drscratch.org"
                to = [email]
                email = EmailMessage(subject,body,sender,to)
                #email.attach_file("static/app/images/logo_main.png")
                email.send()
                login(request, organization)
                return HttpResponseRedirect('/organization/' + organization.username)

            else:
                #Doesn't exist this hash
                flagHash = 1

                return render(request, 'error/sign-up.html',
                                  {'flagName':flagName,
                                   'flagEmail':flagEmail,
                                   'flagHash':flagHash,
                                   'flagForm':flagForm,
                                   'flagOrganization':flagOrganization})


        else:
            flagForm = 1
            return render(request, 'error/sign-up.html',
                  {'flagName':flagName,
                   'flagEmail':flagEmail,
                   'flagHash':flagHash,
                   'flagForm':flagForm,
                   'flagOrganization':flagOrganization})

    elif request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/organization/' + request.user.username)
        else:
            return render(request, 'organization/organization.html')


#_________________________ TO SHOW ORGANIZATION'S DASHBOARD ___________#

def login_organization(request):
    """Log in app to user"""


    if request.method == 'POST':
        flag = False
        flagOrganization = 0
        form = LoginOrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            organization = authenticate(username=username, password=password)
            if organization is not None:
                if organization.is_active:
                    login(request, organization)
                    return HttpResponseRedirect('/organization/' + organization.username)

            else:
                flag = True
                flagOrganization = 1
                return render(request, 'sign-password/user-doesnt-exist.html',
                                         {'flag': flag,
                                         'flagOrganization': flagOrganization})

    else:
        return HttpResponseRedirect("/")


def logout_organization(request):
    """Method for logging out"""


    logout(request)
    return HttpResponseRedirect('/')

def organization(request, name):
    """Show page of Organizations to sign up"""


    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.user.username
            if username == name:
                if Organization.objects.filter(username = username):
                    user = Organization.objects.get(username=username)
                    img = user.img
                    dic={'username':username,
                    "img":str(img)}

                    return render(request, 'organization/main.html', dic)

                else:
                    logout(request)
                    return HttpResponseRedirect("/organization")

            else:
                #logout(request)
                return render(request, 'sign-password/organization.html')

        return render(request, 'sign-password/organization.html') 

    else:
        return HttpResponseRedirect("/")

def stats(request,username):
    """Generator of the stats from Coders and Organizations"""


    flagOrganization = 0
    flagCoder = 0
    if Organization.objects.filter(username=username):
        flagOrganization = 1
        page = 'organization'
        user = Organization.objects.get(username=username)
    elif Coder.objects.filter(username=username):
        flagCoder = 1
        page = 'coder'
        user = Coder.objects.get(username=username)

    date_joined= user.date_joined
    end = datetime.today()
    end = date(end.year, end.month,end.day)
    start = date(date_joined.year,date_joined.month,date_joined.day)
    dateList = date_range(start, end)
    daily_score = []
    mydates = []
    for n in dateList:
        mydates.append(n.strftime("%d/%m"))
        if flagOrganization:
            points = File.objects.filter(organization=username).filter(time=n)
        elif flagCoder:
            points = File.objects.filter(coder=username).filter(time=n)
        points = points.aggregate(Avg("score"))["score__avg"]
        daily_score.append(points)

    for n in daily_score:
        if n==None:
            daily_score[daily_score.index(n)]=0

    if flagOrganization:
        f = File.objects.filter(organization=username)
    elif flagCoder:
        f = File.objects.filter(coder=username)
    if f:

        #If the org has analyzed projects
        parallelism = f.aggregate(Avg("parallelization"))
        parallelism = int(parallelism["parallelization__avg"])
        abstraction = f.aggregate(Avg("abstraction"))
        abstraction = int(abstraction["abstraction__avg"])
        logic = f.aggregate(Avg("logic"))
        logic = int(logic["logic__avg"])
        synchronization = f.aggregate(Avg("synchronization"))
        synchronization = int(synchronization["synchronization__avg"])
        flowControl = f.aggregate(Avg("flowControl"))
        flowControl = int(flowControl["flowControl__avg"])
        userInteractivity = f.aggregate(Avg("userInteractivity"))
        userInteractivity = int(userInteractivity["userInteractivity__avg"])
        dataRepresentation = f.aggregate(Avg("dataRepresentation"))
        dataRepresentation = int(dataRepresentation["dataRepresentation__avg"])

        deadCode = File.objects.all().aggregate(Avg("deadCode"))
        deadCode = int(deadCode["deadCode__avg"])
        duplicateScript = File.objects.all().aggregate(Avg("duplicateScript"))
        duplicateScript = int(duplicateScript["duplicateScript__avg"])
        spriteNaming = File.objects.all().aggregate(Avg("spriteNaming"))
        spriteNaming = int(spriteNaming["spriteNaming__avg"])
        initialization = File.objects.all().aggregate(Avg("initialization"))
        initialization = int(initialization["initialization__avg"])
    else:

        #If the org hasn't analyzed projects yet
        parallelism,abstraction,logic=[0],[0],[0]
        synchronization,flowControl,userInteractivity=[0],[0],[0]
        dataRepresentation,deadCode,duplicateScript=[0],[0],[0]
        spriteNaming,initialization =[0],[0]

    #Saving data in the dictionary
    dic = {
        "date":mydates,
        "username": username,
        "img": user.img,
        "daily_score":daily_score,
        "skillRate":{"parallelism":parallelism,
                 "abstraction":abstraction,
                 "logic": logic,
                 "synchronization":synchronization,
                 "flowControl":flowControl,
                 "userInteractivity":userInteractivity,
                 "dataRepresentation":dataRepresentation},
                 "codeSmellRate":{"deadCode":deadCode,
        "duplicateScript":duplicateScript,
        "spriteNaming":spriteNaming,
        "initialization":initialization }}

    return render(request, page + '/stats.html', dic)



def settings(request,username):
    """Allow to Coders and Organizations change the image and password"""


    base_dir = os.getcwd()
    flagOrganization = 0
    flagCoder = 0
    if Organization.objects.filter(username=username):
        page = 'organization'
        user = Organization.objects.get(username=username)
    elif Coder.objects.filter(username=username):
        page = 'coder'
        user = Coder.objects.get(username=username)

    if request.method == "POST":

        #Saving image in DB
        user.img = request.FILES["img"]
        os.chdir(base_dir+"/static/img")
        user.img.name = str(username)+ "."+ str(request.FILES["img"]).split(".")[1]

        if os.path.exists(user.img.name):
            os.remove(user.img.name)

        os.chdir(base_dir)
        user.save()

    dic = {
    "username": username,
    "img": user.img
    }


    return render(request, page + '/settings.html', dic)



def downloads(request,username, filename=""):
    """Allow to Coders and Organizations download the files.CSV already analyzed"""


    flagOrganization = 0
    flagCoder = 0
    #segmentation
    if Organization.objects.filter(username=username):
        flagOrganization = 1
        user = Organization.objects.get(username=username)
    elif Coder.objects.filter(username=username):
        flagCoder = 1
        user = Coder.objects.get(username=username)

    if flagOrganization:
        csv = CSVs.objects.all().filter(organization=username)
        page = 'organization'
    elif flagCoder:
        csv = CSVs.objects.all().filter(coder=username)
        page = 'coder'
    #LIFO to show the files.CSV

    csv_len = len(csv)
    lower = 0
    upper = 10
    list_csv = {}


    if csv_len > 10:
        for n in range((csv_len/10)+1):
            list_csv[str(n)]= csv[lower:upper-1]
            lower = upper
            upper = upper + 10


        dic = {
        "username": username,
        "img": user.img,
        "csv": list_csv,
        "flag": 1
        }
    else:
        dic = {
        "username": username,
        "img": user.img,
        "csv": csv,
        "flag": 0
        }


    if request.method == "POST":
        #Downloading CSV
        filename = request.POST["csv"]
        path_to_file = os.path.dirname(os.path.dirname(__file__)) + \
                        "/csvs/Dr.Scratch/" + filename
        csv_data = open(path_to_file, 'r')
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
        return response

    
    return render(request, page + '/downloads.html', dic)



#________________________ ANALYZE CSV FOR ORGANIZATIONS ____________#

def analyze_CSV(request):
    """Analyze files.CSV with a list of projects to analyze them at a time"""


    if request.method =='POST':
        if "_upload" in request.POST:
            #Analize CSV file
            csv_data = 0
            flag_csv = False
            file = request.FILES['csvFile']
            file_name = request.user.username + "_" + str(datetime.now()) + \
                        ".csv"# file.name.encode('utf-8')
            dir_csvs = os.path.dirname(os.path.dirname(__file__)) + \
                        "/csvs/" + file_name
            #Save file .csv
            with open(dir_csvs, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            dictionary = {}
            for line in open(dir_csvs, 'r'):
                row = len(line.split(","))
                type_csv = ""
                username = request.user.username

                #Check doesn't exist any old project.json
                try:
                    os.remove(dir_zips + "project.json")
                except:
                    print "No existe"
                
                if row == 2:
                    type_csv = "2_row"
                    code = line.split(",")[0]
                    url = line.split(",")[1]
                    url = url.split("\n")[0]
                    method = "csv"
                    if url.isdigit():
                        idProject = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            idProject = url.split("/")[-1]
                        elif slashNum == 5:
                            idProject = url.split('/')[-2]
                    try:

                        (pathProject, file) = send_request_getSb3(idProject, 
                                                                    username,
                                                                    method)
                        d = analyze_project(request, pathProject, file)
                    except:
                        d = ["Error analyzing project", url]

                    try:
                        os.remove(dir_zips + "project.json")
                    except:
                        print "No existe"

                    dic = {}
                    dic[line] = d
                    dictionary.update(dic)
                elif row == 1:
                    type_csv = "1_row"
                    url = line.split("\n")[0]
                    method = "csv"
                    if url.isdigit():
                        idProject = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            idProject = url.split("/")[-1]
                        elif slashNum == 5:
                            idProject = url.split('/')[-2]
                    try:
                        (pathProject, file) = send_request_getSb3(idProject, 
                                                                    username,
                                                                     method)
                        d = analyze_project(request, pathProject, file)
                    except:
                        d = ["Error analyzing project", url]

                    try:
                        os.remove(dir_zips + "project.json")
                    except:
                        print "No existe"


                    dic = {}
                    dic[url] = d
                    dictionary.update(dic)

            csv_data = generator_CSV(request, dictionary, file_name, type_csv)

            #segmentation
            if Organization.objects.filter(username = username):
                csv_save = CSVs(filename = file_name, 
                                    directory = csv_data, 
                                    organization = username)
                
                page = 'organization'
            elif Coder.objects.filter(username = username):
                csv_save = CSVs(filename = file_name, 
                                    directory = csv_data, 
                                    coder = username)
                page = 'coder'
            csv_save.save()

            return HttpResponseRedirect('/' + page + "/downloads/" + username)

        elif "_download" in request.POST:
            #Export a CSV File

            if request.user.is_authenticated():
                username = request.user.username
            csv = CSVs.objects.latest('date')

            path_to_file = os.path.dirname(os.path.dirname(__file__)) + \
                            "/csvs/Dr.Scratch/" + csv.filename
            csv_data = open(path_to_file, 'r')
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(csv.filename)
            return response

    else:
        return HttpResponseRedirect("/organization")


#_________________________GENERATOR CSV FOR ORGANIZATION____________________________#

def generator_CSV(request, dictionary, filename, type_csv):
    """Generator of a csv file"""


    csv_directory = os.path.dirname(os.path.dirname(__file__)) + \
                                        "/csvs/Dr.Scratch/"
    csv_data = csv_directory + filename
    writer = csv.writer(open(csv_data, "wb"))
    dic = org.translate_CT(request.LANGUAGE_CODE)

    if type_csv == "2_row":
        writer.writerow([dic["code"], dic["url"], dic["mastery"],
                        dic["abstraction"], dic["parallelism"],
                        dic["logic"], dic["sync"],
                        dic["flow_control"], dic["user_inter"], dic["data_rep"],
                        dic["dup_scripts"],dic["sprite_naming"],
                        dic["dead_code"], dic["attr_init"]])

    elif type_csv == "1_row":
        writer.writerow([dic["url"], dic["mastery"],
                        dic["abstraction"], dic["parallelism"],
                        dic["logic"], dic["sync"],
                        dic["flow_control"], dic["user_inter"], dic["data_rep"],
                        dic["dup_scripts"],dic["sprite_naming"],
                        dic["dead_code"], dic["attr_init"]])

    for key, value in dictionary.items():
        total = 0
        flag = False
        try:
            if value[0] == "Error analyzing project":
                if type_csv == "2_row":
                    row1 = key.split(",")[0]
                    row2 = key.split(",")[1]
                    row2 = row2.split("\n")[0]
                    writer.writerow([row1, row2, dic["error"]])
                elif type_csv == "1_row":
                    row1 = key.split(",")[0]
                    writer.writerow([row1,dic["error"]])
        except:
            total = 0
            row1 = key.split(",")[0]
            if type_csv == "2_row":
                row2 = key.split(",")[1]
                row2 = row2.split("\n")[0]

            for key, subvalue in value.items():
                if key == "duplicateScript":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row11 = sub2value
                if key == "spriteNaming":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row12 = sub2value
                if key == "deadCode":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row13 = sub2value
                if key == "initialization":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row14 = sub2value

            for key, value in value.items():
                if key == "mastery":
                    for key, subvalue in value.items():
                        if key!="maxi" and key!="points":
                            if key == dic["parallelism"]:
                                row5 = subvalue
                            elif key == dic["abstraction"]:
                                row4 = subvalue
                            elif key == dic["logic"]:
                                row6 = subvalue
                            elif key == dic["sync"]:
                                row7 = subvalue
                            elif key == dic["flow_control"]:
                                row8 = subvalue
                            elif key == dic["user_inter"]:
                                row9 = subvalue
                            elif key == dic["data_rep"]:
                                row10 = subvalue
                            total = total + subvalue
                    row3 = total
            if type_csv == "2_row":
                writer.writerow([row1,row2,row3,row4,row5,row6,row7,row8,
                            row9,row10,row11,row12,row13,row14])
            elif type_csv == "1_row":
                writer.writerow([row1,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
    return csv_data



#__________________________ TO REGISTER USER _________________________________#

def coder_hash(request):
    """Method for to sign up users in the platform"""


    if request.method == "POST":
        form = CoderHashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/coder_hash')
    elif request.method == 'GET':
        return render(request, 'coder/coder-hash.html')


def sign_up_coder(request):
    """Method which allow to sign up coders"""


    flagCoder = 1
    flagHash = 0
    flagName = 0
    flagEmail = 0
    flagForm = 0
    flagWrongEmail = 0
    flagWrongPassword = 0
    if request.method == 'POST':
        form = CoderForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            email = form.cleaned_data['email']
            email_confirm = form.cleaned_data['email_confirm']
            birthmonth = form.cleaned_data['birthmonth']
            birthyear = form.cleaned_data['birthyear']
            gender = form.cleaned_data['gender']
            #gender_other = form.cleaned_data['gender_other']
            country = form.cleaned_data['country']
            
            #Checking the validity into the database contents.
            #They will be refused if they already exist.
            #If they exist an error message will be shown.
            if User.objects.filter(username = username):
                #This name already exists
                flagName = 1
                #return render_to_response("error/sign-up.html",
                #                          {'flagName':flagName,
                #                           'flagEmail':flagEmail,
                #                           'flagHash':flagHash,
                #                           'flagForm':flagForm,
                #                           'flagCoder':flagCoder},
                #                          context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder})

            elif User.objects.filter(email = email):
                #This email already exists
                flagEmail = 1
                #return render_to_response("error/sign-up.html",
                #                        {'flagName':flagName,
                #                        'flagEmail':flagEmail,
                #                        'flagHash':flagHash,
                #                        'flagForm':flagForm,
                #                        'flagCoder':flagCoder},
                #                        context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder})
            elif (email != email_confirm):
                flagWrongEmail = 1
                #return render_to_response("error/sign-up.html",
                #        {'flagName':flagName,
                #        'flagEmail':flagEmail,
                #        'flagHash':flagHash,
                #        'flagForm':flagForm,
                #        'flagCoder':flagCoder,
                #        'flagWrongEmail': flagWrongEmail},
                #        context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder,
                                                              'flagWrongEmail': flagWrongEmail})

            elif (password != password_confirm):
                flagWrongPassword = 1
                #return render_to_response("error/sign-up.html",
                #        {'flagName':flagName,
                #        'flagEmail':flagEmail,
                #        'flagHash':flagHash,
                #        'flagForm':flagForm,
                #        'flagCoder':flagCoder,
                #        'flagWrongPassword':flagWrongPassword},
                #        context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder,
                                                              'flagWrongPassword': flagWrongPassword})

            else:
                coder = Coder.objects.create_user(username = username,
                                    email=email, password=password,
                                    birthmonth = birthmonth, 
                                    birthyear = birthyear,
                                    gender = gender,
                                    #gender_other = gender_other,
                                    country = country)

                coder = authenticate(username=username, password=password)
                user = Coder.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token=default_token_generator.make_token(user)
                c = {
                        'email':email,
                        'uid':uid,
                        'token':token}

                body = render_to_string("coder/email-sign-up.html",c)
                subject = "Welcome to Dr. Scratch!"
                sender ="no-reply@drscratch.org"
                to = [email]
                email = EmailMessage(subject,body,sender,to)
                email.send()
                login(request, coder)
                return HttpResponseRedirect('/coder/' + coder.username)

        else:
            flagForm = 1
            #return render_to_response("error/sign-up.html",
            #      {'flagName':flagName,
            #       'flagEmail':flagEmail,
            #       'flagHash':flagHash,
            #       'flagForm':flagForm},
            #      context_instance = RC(request))
            return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                          'flagEmail':flagEmail,
                                                          'flagHash':flagHash,
                                                          'flagForm':flagForm})

    elif request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/coder/' + request.user.username)
        else:
            #return render_to_response("main/main.html", 
            #        context_instance = RC(request))
            return render(request, 'main/main.html')



#_________________________ TO SHOW USER'S DASHBOARD ___________#

def coder(request, name):
    """Shows the main page of coders"""


    if (request.method == 'GET') or (request.method == 'POST'):
        if request.user.is_authenticated():
            username = request.user.username
            if username == name:
                if Coder.objects.filter(username = username):
                    user = Coder.objects.get(username=username)
                    img = user.img
                    dic={'username':username,
                    "img":str(img)}

                    #return render_to_response("coder/main.html",
                    #                            dic,
                    #                            context_instance = RC(request))
                    return render(request, 'coder/main.html', dic)
                else:
                    logout(request)
                    return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/")


def login_coder(request):
    """Log in app to user"""


    if request.method == 'POST':
        flagCoder = 0
        flag = False
        form = LoginOrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            coder = authenticate(username=username, password=password)
            if coder is not None:
                if coder.is_active:
                    login(request, coder)
                    return HttpResponseRedirect('/coder/' + coder.username)

            else:
                flag = True
                flagCoder = 1
                #return render_to_response("sign-password/user-doesnt-exist.html",
                #                            {'flag': flag,
                #                             'flagCoder': flagCoder},
                #                            context_instance=RC(request))
                return render(request, 'sign-password/user-doesnt-exist.html', {'flag': flag, 'flagCoder': flagCoder})
    else:
        return HttpResponseRedirect("/")


def logout_coder(request):
    """Method for logging out"""


    logout(request)
    return HttpResponseRedirect('/')

#_________________________ CHANGE PASSWORD __________________________________#

def change_pwd(request):
    """Change user's password"""


    if request.method == 'POST':
        recipient = request.POST['email']

        #segmentation
        page = segmentation(request)
        try:
            if Organization.objects.filter(email=recipient):
                user = Organization.objects.get(email=recipient)
            elif Coder.objects.filter(email=recipient):
                user = Coder.objects.get(email=recipient)
        except:
            #return render_to_response("sign-password/user-doesnt-exist.html",
            #                               context_instance=RC(request))
            return render(request, 'sign-password/user-doesnt-exist.html')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)

        
        c = {
                'email':recipient,
                'uid':uid,
                'token':token,
                'id':user.username}


        body = render_to_string("sign-password/email-reset-pwd.html",c)
        subject = "Dr. Scratch: Did you forget your password?"
        sender ="no-reply@drscratch.org"
        to = [recipient]
        email = EmailMessage(subject,body,sender,to)
        email.send()
        #return render_to_response("sign-password/email-sended.html",
        #                        context_instance=RC(request))
        return render(request, 'sign-password/email-sended.html')

    else:

        page = segmentation(request)
        #return render_to_response("sign-password/password.html", 
        #                        context_instance=RC(request))
        return render(request, 'sign-password/password.html')



def reset_password_confirm(request,uidb64=None,token=None,*arg,**kwargs):
    """Confirm change password"""


    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        if Organization.objects.filter(pk=uid):
            user = Organization._default_manager.get(pk=uid)
            page = 'organization'
        elif Coder.objects.filter(pk=uid):
            user = Coder._default_manager.get(pk=uid)
            page = 'coder'
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if request.method == "POST":
        flag_error = False
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST['password']
            new_confirm = request.POST['confirm']
            if new_password == "":
                return render(request, 'sign-password/new-password.html')

            elif new_password == new_confirm:
                user.set_password(new_password)
                user.save()
                logout(request)
                user = authenticate(username=user.username, 
                                    password=new_password)
                login(request, user)
                return HttpResponseRedirect('/' + page + '/' + user.username)
                return render(request, page + '/main.html')

            else:
                flag_error = True
                return render(request, 'sign-password/new-password.html',
                                    {'flag_error':flag_error})

    else:
         if user is not None and default_token_generator.check_token(user, token):
             return render(request, 'sign-password/new-password.html')
         else:
             return render(request, page + '/main.html')



#_________________________________ DISCUSS ___________________________________#
def discuss(request):
    """Forum to get feedback"""


    comments = dict()
    form = DiscussForm()
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = ""
    if request.method == "POST":

        form = DiscussForm(request.POST)
        if form.is_valid():
            nick = user
            date = timezone.now()
            comment = form.cleaned_data["comment"]
            new_comment = Discuss(nick = nick,
                                date = date,
                                comment=comment)
            new_comment.save()
        else:
            comments["form"] = form

    data = Discuss.objects.all().order_by("-date")
    lower = 0
    upper = 10
    list_comments = {}
   
    if len(data) > 10:
        for n in range((len(data)/10)+1):
            list_comments[str(n)]= data[lower:upper-1]
            lower = upper
            upper = upper + 10
    else:
        list_comments[0] = data


    comments["comments"] = list_comments

    return render(request, 'discuss.html', comments)



########################## UNDERDEVELOPMENT ###################################

#_________________________________ ERROR _____________________________________#

def error404(request):
    """Return own 404 page"""


    response = render(request, '404.html', {})
    response.status_code = 404
    return response

def error500(request):
    """Return own 500 page"""


    response = render(request, '500.html', {})
    return response

