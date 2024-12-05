import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import models
import hashlib
from django.shortcuts import render

from .models import Member, Department, ApprovalRecord, UserApplication


@csrf_exempt
def process_frontend(request):
    print(request)
    print("yeah")
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        print(action)
        if action=='login':
            return login(request)
        elif action=='getUserInfo':
            return getUserInfo(request)
        elif action == 'modifyUserInfo':
            return modify_UserInfo(request)
        #------------以下为管理员功能-----------------------
        elif action == 'resetPassword':
            return reset_password(request)
            #modify_password(request)
        elif action=='modifyPhone':
            return modify_phone(request)
        elif action=='modifyEmail':
            return modify_email(request)
        elif action == 'adminModifyUserInfo':
            return adminModifyUserInfo(request)
        elif action == 'getAllUsersInfo':
            return getAllUsersInfo(request)
        elif action == 'addMember':
            return add_member(request)
        elif action == 'deleteUser':
            return delete_member(request)
        #------------以下为物流部门功能--------------
        elif action == 'addLeaseApply':
            return applyBySellers(request)
        elif action == 'getUserLeaseApplies':
            return getAppliesBySeller(request)
    else:
        print("noPost")

    return JsonResponse({'result': False})

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id') # id
        password = data.get('password') # password
        try:
            member = Member.objects.get(id=id)

            print(member.department_name)
            if member.check_password(password):
                # 密码正确
                return JsonResponse({
                    'result':'success',
                    'user':member.to_dict(),
                })
            else:
                # 密码不正确
                return JsonResponse({'result': 'wrong password'})
        except Member.DoesNotExist:
            return JsonResponse({'result': 'invalid account'})
    else :
        return JsonResponse({'result':'invalid request'})

def getUserInfo(request):
    data = json.loads(request.body)
    id = data.get('id')  # id
    print(id)
    try:
        member = Member.objects.get(id=id)

        print(member)
        department = Department.objects.get(name=member.department_name)

        return JsonResponse({
            'result': 'success',
            'id': member.id,
            'name': member.name,
            'password':member.password,
            'department_name': str(member.department_name),
            'phone': member.phone,
            'email': member.email,
            'identity': member.identity,
        })
    except Member.DoesNotExist:
        return JsonResponse({'result': 'invalid account'})

def modify_UserInfo(request):
    modify_password(request)
    modify_phone(request)
    modify_email(request)
    return JsonResponse({'result':'success'})

def reset_password(request):
    print('reset_password')
    data = json.loads(request.body)
    newPassword ='behappyeveryday'
    id = data.get('id')
    print(id)
    member = Member.objects.get(id=id)
    member.modify_password(newPassword)
    print("1111")
    return JsonResponse({'result':'success'})

def modify_password(request):
    data = json.loads(request.body)
    newPassword = data.get('newPassword')
    id = data.get('id')
    print(id)
    member = Member.objects.get(id = id)
    member.modify_password(newPassword)

def modify_phone(request):
    data = json.loads(request.body)
    newPhone = data.get('newPhone')
    print(newPhone)
    id = data.get('id')
    member = Member.objects.get(id = id)
    member.modify_phone(newPhone)

def modify_email(request):
    data = json.loads(request.body)
    newEmail = data.get('newEmail')
    id = data.get('id')
    member = Member.objects.get(id = id)
    member.modify_email(newEmail)

#---------------------------------以下为管理员功能--------------------------------

def getAllUsersInfo(request): # 返回所有用户信息, 用于管理员查看用户信息
    members = Member.objects.all()
    member_list = list(members.values())
    print(member_list)
    return JsonResponse({
        'result':'success',
        'usersList':member_list,
    })

def add_member(request): # 添加成员变量
    data = json.loads(request.body)
    data = data.get('user')
    print(data)
    # id是自增主键，所以不能设置，而是由系统自动返回
    name = data.get('name')
    print(name)
    password = 'iloveworking'
    department_name = data.get('department_name_id')
    print(department_name)
    phone = data.get('phone')
    email = data.get('email')
    identity_name = data.get('identity')
    # id
    # name
    # password
    # department_name
    # phone
    # email
    # identity
    try:
        department = Department.objects.get(name=department_name)
    except Department.DoesNotExist:
        department = None
    # 添加member时，由于department—_name是外键，所以需要转换一下
    member = Member(
        name = name,
        password = password,
        department_name = department,
        phone = phone,
        email = email,
        identity = identity_name,
    )
    member.saveNew() # 存储到数据库
    return JsonResponse({
        'result':'success',
        'user': member.to_dict(),
    })

def adminModifyUserInfo(request):
    data = json.loads(request.body)
    data = data.get('user')
    id = data.get('id')
    name = data.get('name')
    print(name)
    password = data.get('password')
    department_name = data.get('department_name_id')
    print(department_name)
    department = Department.objects.get(name=department_name)
    phone = data.get('phone')
    email = data.get('email')
    identity = data.get('identity')
    try:
        member = Member.objects.get(id = id)
        member.modifyInfo(name, password, department, phone, email, identity)
        return JsonResponse({'result':'success'})
    except Member.DoesNotExist:
        return JsonResponse({'result':'invalid account'})


def delete_member(request):
    data = json.loads(request.body)
    id = data.get('id')
    try:
        member = Member.objects.get(id=id)
        member.delete()
        return JsonResponse({'result':'success'})
    except Member.DoesNotExist:
        return JsonResponse({'result': 'invalid account'})

#------------------------------销售部门功能-------------------------------------------------------
def applyBySellers(request): #发起一个申请
    data = json.loads(request.body)
    data = data.get('leaseApply')
    #id = data.get('id')
    userId = None
    userId = Member.objects.get(id=data.get('userId'))
    print(userId)
    phone = data.get('phone')
    print(phone)
    message = data.get('goodsInfo') #物资信息
    usage = data.get('goodsUsage') #物资用途
    userApplication = UserApplication(
        #id = id,
        userId=userId,
        phone = phone,
        message = message,
        usage = usage,
        status = '待确认'
    )
    userApplication.save()
    return JsonResponse({
        'result':'success',
        'userApplication':userApplication.to_dict(),
        'id':userApplication.id,
    })

def getAppliesBySeller(request): #获取某个销售人员所写的申请
    data = json.loads(request.body)
    userId = data.get('userId') #申请人id
    print(userId)
    applications = UserApplication.objects.filter(userId = userId)
    application_list = [
        {
            'id': app.id,
            'userId': str(app.userId),
            'type':app.type,
            'phone': app.phone,
            'goodsInfo': app.message,
            'goodsUsage': app.usage,
            'state':app.status,
            # 添加其他需要返回的字段...
        }
        for app in applications
    ]
    print(application_list)
    return JsonResponse({'result':'success', 'applications': application_list})



#------------------------------物资管理部门功能----------------------------------------------------
def getAllApplications(request): # 看到所有的物资申请
    applications = UserApplication.objects
    applications_list = [
        {
            'id': app.id,
            'userId': app.userId,
            'type': app.type,
            'phone': app.phone,
            'message': app.message,
            'usage': app.usage,
            'state': app.status,
        }
        for app in applications
    ]
    return JsonResponse({
        'result':'success',
        'applications':applications_list,
    })

def applyMaintain(request): #发起维护审批
    return HttpResponse('yeah')
    data = json.loads(request.body)
    applier = data.get('applier') #申请人
    department = data.get('department')
    time = data.get('time')
    opType = data.get('opType')
    opInfo = data.get('opInfo')



#---------------------------审批部门功能--------------------------------------------------------
def approve(request): #审批，应该是得到一个审批id
    data = json.loads(request.body)
    id = data.get('id')
    # applier = data.get('applier')  # 申请人
    # department = data.get('department')
    # time = data.get('time')
    # opType = data.get('opType')
    # opInfo = data.get('opInfo')
    # approver = data.get('approver') #审批人
    # reply = data.get('reply')
    # approveBoolean = data.get('approveBoolean') #是否通过
    try:
        approveRecord = ApprovalRecord.objects.get(id=id)
        approver = data.get('approver')  # 审批人
        reply = data.get('reply')
        approveBoolean = data.get('approveBoolean') #是否通过
    except ApprovalRecord.DoesNotExist:
        return JsonResponse({"result":"invalid id"}
    )



