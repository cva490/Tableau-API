from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
import tableauserverclient as TSC
from tableauserverclient import ConnectionCredentials, ConnectionItem
from os import path
from django.contrib.staticfiles import finders
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from TableauAutomation import settings
import os
def Login(request):
    return render(request, 'login.html')


def home(request):
    global all_project_items
    global server
    tableau_auth = TSC.TableauAuth('leela.krishna8538@gmail.com', 'Covid@2020')
    server = TSC.Server('https://prod-apnortheast-a.online.tableau.com')
    if server.auth.sign_in(tableau_auth):
        all_project_items, pagination_item = server.projects.get()
        return render(request, 'home.html', {'username':server.users.get_by_id(server.user_id).fullname,  'role':server.users.get_by_id(server.user_id).site_role,  'lastlogin':server.users.get_by_id(server.user_id).last_login})


def logout(request):
    server.auth.sign_out()
    return render(request, 'login.html')


def publish(request):
    return render(request, 'publish.html', {'username':server.users.get_by_id(server.user_id).fullname,  'role':server.users.get_by_id(server.user_id).site_role,  'lastlogin':server.users.get_by_id(server.user_id).last_login,  'projects':all_project_items})

def users(request):
    return render(request, 'users.html', {'username':server.users.get_by_id(server.user_id).fullname,  'role':server.users.get_by_id(server.user_id).site_role,  'lastlogin':server.users.get_by_id(server.user_id).last_login,  'projects':all_project_items})


def submmitpublish(request):
    if request.method == 'POST':
        pass
    if request.FILES['txt_file']:
        myfile = request.FILES.getlist('txt_file')
        var_prj = request.POST['sel_prj']
        fs = FileSystemStorage()
        for tableaufile in myfile: 
            print(tableaufile.name)
            filename = fs.save(tableaufile.name, tableaufile)
            #uploaded_file_url = fs.url(filename)
            fs.url(filename)
            #uploaded_file_url=path.join(settings.MEDIA_ROOT,myfile)
            str_media=settings.MEDIA_ROOT
            uploaded_file_url=str_media+"\\"+tableaufile.name
            print(uploaded_file_url)
            #formattedpath = 'TableauAutomation\\Media\\' + myfile
            #print(formattedpath) 
            wb_item = TSC.WorkbookItem(name=tableaufile, project_id=var_prj)
            wb_item = server.workbooks.publish(wb_item, uploaded_file_url, 'Overwrite')
            os.remove(uploaded_file_url)
        return render(request, 'publish.html', {'username':server.users.get_by_id(server.user_id).fullname,  'role':server.users.get_by_id(server.user_id).site_role,  'lastlogin':server.users.get_by_id(server.user_id).last_login,  'projects':all_project_items})


def submmitusers(request):
    if request.method == 'POST':
        pass
    if  request.FILES.getlist('txt_file_users'):
        myfile = request.FILES.getlist('txt_file_users')
        fs = FileSystemStorage()
        for userfile in myfile:
            #print(userfile)
            filename = fs.save(userfile.name, userfile)
        fs.url(filename)
        str_media=settings.MEDIA_ROOT
        TableauUser_file_url=str_media+"\\"+userfile.name
        print(TableauUser_file_url)
        #newuser=TSC.UserItem('siva','Viewer')
        #server.users.add(newuser)
        os.remove(TableauUser_file_url)
    return render(request, 'users.html', {'username':server.users.get_by_id(server.user_id).fullname,  'role':server.users.get_by_id(server.user_id).site_role,  'lastlogin':server.users.get_by_id(server.user_id).last_login})