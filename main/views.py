from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
def index(request):
    return redirect('creator_studio_login')
def creator_studio_login(request):
    return render(request, "creator_studio_login.html")
def view_admin(request):
    return render(request, "view_admin.html")
def add_admin(request):
    return render(request, "add_admin.html")
def edit_admin(request):
    return render(request, "edit_admin.html")
@api_view(['POST'])
def delete_user(request):
    print(request.data['email'])
    app_users.objects.filter(email=request.data['email']).delete()
    return Response({"success": True})
@api_view(['POST'])
def all_users(request):
    person=app_users.objects.get(email=request.data['email'])
    people=''
    status=''
    name=''
    edited=''
    if request.data['edit']==False:
        if person.parent==request.data['email']:
            status='Admin'
            name=person.fullname
            people=list(app_users.objects.filter(parent=request.data['email']).exclude(email=request.data['email']).values())
        else:
            admin=app_users.objects.get(email=person.parent)
            if admin.parent==admin.email:
                status='User'
                name=person.fullname
                people=list(app_users.objects.filter(parent=request.data['email']).exclude(email=request.data['email']).values())
            else:
                status='SubUser'
                admin=app_users.objects.get(email=person.parent)
                name=admin.fullname
                people=list(app_users.objects.filter(parent=admin.email).exclude(email=admin.email).values())
        return Response({"success": False,'status':status,'people':people,'name':name,'edited':edited})

    if request.data['edit']:
        name=person.fullname
        edited=list(app_users.objects.filter(email=request.data['edit']).values())
        return Response({"success": len(edited)>0 and edited[0]['parent']==request.data['email'],'status':status,'people':people,'name':name,'edited':edited})

@api_view(['POST'])
def add_user(request):
    if(request.data['edit']==False):
        if(len(list(app_users.objects.filter(email=request.data['email'])))>0):
            return Response({"success": False,"message":"User with this email exists already.Choose another!"})
        elif(len(list(app_users.objects.filter(fullname=request.data['fullname'])))>0):
            return Response({"success": False,"message":"User with this fullname exists already.Choose another!"})
        elif(request.data['password']!=request.data['confirmpassword']):
            return Response({"success": False,"message":"Password and Confirm Password should be same!"})
        elif(len(request.data['password'])>15 or len(request.data['fullname'])>15 ):
            return Response({"success": False,"message":"Password,Fullname cannot be more than 15 characters!"})
        try:
            validate_email(request.data["email"])
        except ValidationError:
            return Response({"success": False,"message":"Enter a valid email address!"})
        person=app_users.objects.create(email=request.data['email'],password=request.data['password'],subscription=request.data['subscription'],
                                            fullname=request.data['fullname'],residence=request.data['residence'],source=request.data['source'],parent=request.data['parent'],
                                            displayname=request.data['fullname'],account=request.data['account'])
        return Response({"success": True})
    else:
        if(request.data['password']!=request.data['confirmpassword']):
            return Response({"success": False,"message":"Password and Confirm Password should be same!"})
        elif(len(request.data['password'])>15):
            return Response({"success": False,"message":"Password cannot be more than 15 characters!"})
        else:
            person=app_users.objects.get(email=request.data['email'])
            person.subscription=request.data['subscription']
            person.residence=request.data['residence']
            person.source=request.data['source']
            person.account=request.data['account']
            person.password=request.data['password']
            person.save()
            return Response({"success": True})
@api_view(['POST'])
def register(request):
    if(request.data['logging_in']==True):
        try:
            person=app_users.objects.get(email=request.data['email'],password=request.data['password'],account='Active')
            person.last_login=request.data['last_login']
            person.save()
            return Response({"success": True,"email":person.email})
        except app_users.DoesNotExist:
            return Response({"success": False,"message":"Invalid Credentials/You are not an active user!"})

    elif (request.data['logging_in']==False):
        print(f"1{request.data['password']}")
        print(f"2{request.data['confirmpassword']}")
        if(len(list(app_users.objects.filter(email=request.data['email'])))>0):
            return Response({"success": False,"message":"User with this email exists already.Choose another!"})
        elif(len(list(app_users.objects.filter(fullname=request.data['fullname'])))>0):
            return Response({"success": False,"message":"User with this fullname exists already.Choose another!"})
        elif(len(list(app_users.objects.filter(displayname=request.data['displayname'])))>0):
            return Response({"success": False,"message":"User with this displayname exists already.Choose another!"})
        elif(request.data['password']!=request.data['confirmpassword']):
            return Response({"success": False,"message":"Password and Confirm Password should be same!"})
        elif(len(request.data['password'])>15 or len(request.data['fullname'])>15 or len(request.data['displayname'])>15 ):
            return Response({"success": False,"message":"Password,Fullname and Displayname cannot be more than 15 characters!"})
        else:
            try:
                validate_email(request.data['email'])
            except ValidationError:
                return Response({"success": False,"message":"Enter a valid email address!"})
            person=app_users.objects.create(email=request.data['email'],password=request.data['password'],fullname=request.data['fullname'],displayname=request.data['displayname'],residence=request.data['residence'],source=request.data['source'],parent=request.data['email'],account='Active',subscription='Active')
            return Response({"success": True,"email":person.email})
    else:
        try:
            person=app_users.objects.get(email=request.data['email'])
            return Response({"success": True,"message":f"Your Password is {person.password}"})
        except app_users.DoesNotExist:
            return Response({"success": False,"message":"User with this email does not exist!"})