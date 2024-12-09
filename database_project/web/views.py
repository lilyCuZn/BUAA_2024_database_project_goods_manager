import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from . import models
import hashlib
from django.shortcuts import render

from .models import Member, Department, ApprovalRecord, UserApplication, Category, Supplier, PurchaseOrder, Material, \
    LeaseReturn, MaintainRecord, Maintain_Material_Result


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
        #------------以下为外联部门功能------------------------
        elif action == 'addLeaseApply':
            return applyBySellers(request)
        elif action == 'getUserLeaseApplies':
            return getAppliesBySeller(request)
        #------------以下为物资管理部门功能----------------------
        elif action == 'getGoods':
            return getAllMaterials(request)
        elif action == 'getDamageGoods':
            return getAllDamageMaterials(request)
        elif action == 'createMaintainApplication':
            return addApprovalRecord_maintain(request)
        elif action == 'getMaintainApplications':
            return getApprovalRecord_maintain(request)
        elif action == 'createMaintainRecord':
            return addMaintainRecord(request)
        elif action == 'getMaintainRecords':
            return getMaintainRecords_all(request)
        elif action == 'getRecordGoods':
            return getMaterialsFromMaintainId(request)
        elif action == 'maintainGoods':
            return setMaintainResult(request)
        elif action == 'completeMaintainRecord':
            return setMainRecordStatusFinish(request)
        #-----------以下为采购部门功能------------------------------
        elif action == 'createPurchaseApplication':
            return addApprovalRecord_purchase(request)
        elif action == 'getPurchaseApplications':
            return getApprovalRecord_purchase(request)
        elif action == 'createPurchaseRecord':
            return addPurchaseOrder(request)
        elif action == 'getPurchaseRecords':
            return getAllPurchaseOrder(request)
        elif action == 'completePurchaseRecord':
            return completePurchaseOrder(request)
        #------------以下为审批部门功能-------------
        elif action == 'getPendingApproves':
            return getApprovalRecords_Status_approve(request)
        elif action == 'modifyApprove':
            return modifyApproveRecords_approve(request)
        elif action == 'getStorageApproves':
            return getApprovalRecord_maintain(request)
        elif action == 'getPurchaseApproves':
            return getApprovalRecord_purchase(request)
    else:
        print("noPost")

    return JsonResponse({'result': False})

def login(request):
    leaseReturns = LeaseReturn.objects.all()
    for leaseReturn in leaseReturns:
        leaseReturn.checkOverdue()

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
    type = data.get('type')
    print(type)
    userApplication = UserApplication(
        #id = id,
        userId=userId,
        phone = phone,
        message = message,
        usage = usage,
        status = '待确认',
        type = type
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
def getAllApplications_goods_from_seller(request): # 看到所有的物资申请（来自外联部门）
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

def getApprovalRecord_maintain(request): #得到物资管理部门的所有审批记录
    records = ApprovalRecord.objects.filter(operation_type='物资维护申请')
    records_list = [
        {
            'id': record.id,
            'operation_type': record.operation_type,
            'status': record.status,
            'created_time': record.created_time.strftime('%Y-%m-%d %H:%M'),
            'updated_time': record.updated_time.strftime('%Y-%m-%d %H:%M'),
            'applicant': record.applicant.to_dict(),
            'description': record.description,
            'approver': record.approver.to_dict() if record.approver is not None else None,
            'reply': record.reply
        }
        for record in records
    ]
    records_list.sort(
        key=lambda record: (record['status'] != '待确认', record['created_time'])
    )
    applications = records_list
    print(applications)
    return JsonResponse({'result': 'success', 'applications': applications})

def addApprovalRecord_maintain(request): #物资管理部门新增审批（物资维护申请）
    data = json.loads(request.body)
    data = data.get('application')
    applicant_id = data.get('userId')  # 申请人编号
    applicant = Member.objects.get(id=applicant_id)  # 申请人编号，外键关联到Memember表
    operation_type = '物资维护申请'  # 操作类型
    status = '待确认'  # 审批状态
    description = data.get('description')  # 操作说明
    approvalRecord = ApprovalRecord(
        operation_type=operation_type,
        status=status,
        applicant=applicant,
        description=description,
    )
    approvalRecord.save()
    return JsonResponse({'result': 'success'})

def getAllMaterials(request):
    # 得到所有的物资列表
    materials = Material.objects.all()
    material_list = [
        {
            'id':material.id,
            'category': str(material.category) ,# 物资类别编号，外键关联到Category表
            'status':material.status, # 物品状态
            'purchaseId':str(material.purchase_order.id)  # 订购订单，外键关联到PurchaseOrder表
        }
        for material in materials
    ]
    return JsonResponse({'result':'success', 'goods':material_list})

def getAllDamageMaterials(request): #得到所有状态为损坏的material
    materials = Material.objects.filter(status='损坏')
    material_list = [
        {
            'id': material.id,
            'category': str(material.category),  # 物资类别编号，外键关联到Category表
            'status': material.status,  # 物品状态
            'purchaseId': str(material.purchase_order.id)  # 订购订单，外键关联到PurchaseOrder表
        }
        for material in materials
    ]
    return JsonResponse({'result': 'success', 'goods': material_list})


def addMaintainRecord(request): #添加物资维护记录
    data = json.loads(request.body)
    data = data.get('record')
    materialIds = data.get('goods') #物资编号们
    print(materialIds)
    memberId = data.get('userId')  # 维护人员编号，外键关联到Member表
    member = Member.objects.get(id=memberId)
    approvalId = data.get('approveId')  # 审批记录编号，外键关联到ApprovalRecord表
    approval = ApprovalRecord.objects.get(id=approvalId)

    maintainRecord = MaintainRecord(
        member=member,
        approval=approval,
        status='未完成'
    )
    maintainRecord.save()

    for materialId in materialIds:
        material = Material.objects.get(id=materialId)
        material.setStatus('维护中')

        maintain_material_result = Maintain_Material_Result(
            maintainId = maintainRecord,
            materialId= material,
            # result = null
        )
        maintain_material_result.save()

    return JsonResponse({'result':'success'})


def getMaintainRecords_all(request): # 得到所有的维护记录
    maintainRecords = MaintainRecord.objects.all()
    record_list = [
        {
            'id': record.id,  # 主键，自增
            'createdTime': record.createdTime.strftime('%Y-%m-%d %H:%M'),
            'completedTime':record.finishTime.strftime('%Y-%m-%d %H:%M') if record.finishTime != None else '',
            'applicant': record.member.to_dict(),
            'applicationId': str(record.approval),
            'status': record.status,
        }
        for record in maintainRecords
    ]
    print(record_list)
    record_list.sort(key=lambda record:(record['status'] != '未完成', record['createdTime']))
    print(record_list)
    print('success')
    return JsonResponse({'result':'success', 'record_list':record_list})


def getMaterialsFromMaintainId(request): #根据维护记录的id，返回这次维护的目标material
    data = json.loads(request.body)
    maintainId = data.get('recordId')
    maintainRecord = MaintainRecord.objects.get(id=maintainId)
    maintain_material_results = Maintain_Material_Result.objects.filter(maintainId = maintainRecord)
    materialList = []
    for maintain_material_result in maintain_material_results:
        material = maintain_material_result.materialId
        materialList.append(material.to_dict())

    print(materialList)
    materialList.sort(key=lambda material:(material['status']!='维护中', int(material['id'])))
    print(materialList)
    print('success')
    return JsonResponse({'result':'success', 'goods':materialList})

def setMaintainResult(request): # 维护后，对单个物资设置维护结果（修缮or报废）
    data = json.loads(request.body)
    maintainId = data.get('maintainId')
    print(maintainId)
    maintain = MaintainRecord.objects.get(id=maintainId)
    materialId = data.get('goodsId')
    print(materialId)
    material = Material.objects.get(id=materialId)
    result = data.get('result')

    maintain_material_result = Maintain_Material_Result.objects.get(maintainId=maintain, materialId=material)
    maintain_material_result.setResult(result)

    materialStatus = ''
    if result == '修缮':
        materialStatus = '库中'
    elif result == '报废':
        materialStatus = '已报废'
    material.setStatus(materialStatus)
    return JsonResponse({'result':'success'})

def setMainRecordStatusFinish(request): #维护完一整个维护清单后，设置已完成
    data = json.loads(request.body)
    maintainId = data.get('maintainId')
    maintain = MaintainRecord.objects.get(id=maintainId)
    maintain.setFinish()


#--------------------------采购部门功能------------------------------------------------------
def addApprovalRecord_purchase(request): #新增采购审批
    data  = json.loads(request.body)
    data = data.get('application')
    applicant_id = data.get('applicant').get('id') #申请人编号
    operation_type = '物资采购申请' # 操作类型
    status = '待确认'  # 审批状态
    applicant = Member.objects.get(id=applicant_id)  # 申请人编号，外键关联到Member表
    description = data.get('description')  # 操作说明
    # approver = models.ForeignKey(Member, related_name='approver_records', on_delete=models.CASCADE,
    #                              null=False)  # 审批人编号，外键关联到Member表
    # reply = models.CharField(max_length=300, null=False, blank=False)  # 答复
    approvalRecord = ApprovalRecord(
        operation_type = operation_type,
        status = status,
        applicant = applicant,
        description = description,
    )
    approvalRecord.save()
    return JsonResponse({'result':'success'})

def getApprovalRecord_purchase(request): #查看所有的采购审批
    print('purchase_approve')
    records = ApprovalRecord.objects.filter(operation_type='物资采购申请')
    records_list = [
        {
            'id': record.id,
            'operation_type': record.operation_type,
            'status': record.status,
            'created_time': record.created_time.strftime('%Y-%m-%d %H:%M'),
            'updated_time': record.updated_time.strftime('%Y-%m-%d %H:%M'),
            'applicant': record.applicant.to_dict(),
            'description': record.description,
            'approver': record.approver.to_dict() if record.approver is not None else None,
            'reply': record.reply
        }
        for record in records
    ]
    records_list.sort(
        key=lambda record: (record['status'] != '待确认', record['created_time'])
    )
    applications = records_list
    print(applications)
    return JsonResponse({'result': 'success', 'applications': applications})

def addPurchaseOrder(request): #发起采购订单
    data = json.loads(request.body)
    data = data.get('record')
    memberId = data.get('userId')
    categoryName = data.get('goods_type')
    supplierName = data.get('provider')
    print(supplierName)
    quantity = data.get('goods_num')
    status = '采购中'  # 订单状态
    approvalId = data.get('approve_id')  # 审批记录编号，外键关联到ApprovalRecord表
    category = None
    try:
        category = Category.objects.get(name=categoryName)
    except Category.DoesNotExist:
        category = Category(
            name = categoryName
        )
        category.save()

    supplier = None
    try:
        supplier = Supplier.objects.get(name=supplierName)
    except Supplier.DoesNotExist:
        supplier = Supplier(
            name = supplierName
        )
        supplier.save()

    member = Member.objects.get(id=memberId)
    approval = ApprovalRecord.objects.get(id=approvalId)

    purchaseOrder = PurchaseOrder(
        member = member,
        category = category,  # 物资类别编号，外键关联到Category表
        supplier = supplier,  # 供应商编号，外键关联到Supplier表
        quantity = quantity,  # 实际数量
        status = status,  # 订单状态
        approval = approval  # 审批记录编号，外键关联到ApprovalRecord表
    )
    purchaseOrder.save()
    return JsonResponse({"result":"success"})


def getAllPurchaseOrder(request):
    # 获取所有的采购订单，优先放采购中的，status相同按照时间先后排序
    orders = PurchaseOrder.objects.all()
    sorted_orders = sorted(
        orders,
        key=lambda order: (order.status != '采购中', order.create_time)
    )
    orders_list = [
        {
            'id' :order.id,  # 主键，自增
            'applicant':order.member.to_dict(),
            'goods_type' :str(order.category),  # 物资类别编号，外键关联到Category表
            'provider' :str(order.supplier),  # 供应商编号，外键关联到Supplier表
            'created_time' : order.create_time.strftime('%Y-%m-%d %H:%M'),  # 创建时间，自动添加当前时间
            'completed_time' : order.finish_time.strftime('%Y-%m-%d %H:%M') if order.finish_time != None else None,  # 完成时间
            'goods_num' : order.quantity,  # 实际数量
            'status' : order.status,  # 订单状态
            'approver' : str(order.approval) if order.approval != None else None # 审批记录编号，外键关联到ApprovalRecord表
        }
        for order in sorted_orders
    ]
    print(orders_list)
    return JsonResponse({'result':'success', 'orders':orders_list})

def completePurchaseOrder(request): #完成一个采购订单
    data = json.loads(request.body)
    orderId = data.get('recordId')
    order = PurchaseOrder.objects.get(id=orderId)
    order.setFinish()
    # 需要将采购的东西放进物资库里
    num = order.quantity
    for i in range(1, num):
        material = Material(
            category = order.category,  # 物资类别编号，外键关联到Category表
            status = '库中',  # 物品状态
            purchase_order = order  # 订购订单，外键关联到PurchaseOrder表
        )
        material.save()
    return JsonResponse({'result':'success'})

#---------------------------审批部门功能--------------------------------------------------------
def getApprovalRecords_Status_approve(request): #得到所有某种status的审批记录
    data = json.loads(request.body)
    status = data.get('status')
    records = ApprovalRecord.objects.filter(status = status)
    records_list = [
        {
            'id': record.id,
            'operation_type':record.operation_type,
            'status':record.status,
            'created_time':record.created_time.strftime('%Y-%m-%d %H:%M'),
            'updated_time':record.updated_time.strftime('%Y-%m-%d %H:%M'),
            'applicant':record.applicant.to_dict(),
            'description':record.description,
            'approver':record.approver.to_dict() if record.approver is not None else None,
            'reply':record.reply
        }
        for record in records
    ]
    records_list.sort(key=lambda record: record['created_time'])
    print(records_list)
    print("success")
    return JsonResponse({'result': 'success', 'applications': records_list})


def getApprovalRecords_Department(request): #得到某个部门所有的审批记录
    data = json.loads(request.body)
    department = data.get('department')
    if department == '采购部门':
        return getApprovalRecord_purchase(request)
    elif department == '物资管理部门':
        return getApprovalRecord_maintain(request)
    else:
        return JsonResponse({"result":"invalid department"})


def modifyApproveRecords_approve(request): #审批，应该是得到一个审批id
    data = json.loads(request.body)
    data = data.get('approve')

    recordId = data.get('id')
    print(recordId)
    approver = data.get('approver')
    print(approver)
    approverId = approver.get('id')
    print(approverId)
    reply = data.get('reply')
    status = data.get('status')
    try:
        approver = Member.objects.get(id=approverId)
        record = ApprovalRecord.objects.get(id=recordId)
        record.update(approver, reply, status)
        return JsonResponse({'result':'success'})
    except ApprovalRecord.DoesNotExist:
        return JsonResponse({"result":"invalid id"}
    )



