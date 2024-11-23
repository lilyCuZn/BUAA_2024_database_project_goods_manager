from django.db import models

# Create your models here.

from django.db import models

class Department(models.Model):
    # 部门
    id = models.AutoField(primary_key=True)  # 主键，自增
    name = models.CharField(max_length=30, null=False, blank=False)  # 名称
    manager = models.ForeignKey("Member", on_delete=models.CASCADE, null=False)  # 负责人编号，外键关联到Member表
    phone = models.CharField(max_length=11, null=False, blank=False)  # 联系电话，11位
    email = models.EmailField(max_length=50, null=True, blank=True)  # 联系邮箱
    address = models.CharField(max_length=200, null=False, blank=False)  # 部门地址

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'  # 指定数据库表名

class Member(models.Model):
    IDENTITY_CHOICES = [
        ('admin', '管理员'),
        ('member', '普通成员')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    password = models.CharField(max_length=30, null=False, blank=False)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_id')
    phone = models.BigIntegerField(null=False, blank=False)
    email = models.EmailField(max_length=50, null=True, blank=True)
    identity = models.CharField(max_length=7, choices=IDENTITY_CHOICES, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'member'

class Category(models.Model):
    # 物资类别
    id = models.AutoField(primary_key=True)  # 主键，自增
    name = models.CharField(max_length=30, null=False, blank=False)  # 分类名称
    threshold = models.IntegerField(null=False, blank=False)  # 警告阈值

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'  # 指定数据库表名

class ApprovalRecord(models.Model):
    # 审批记录
    OPERATION_TYPE_CHOICES = [
        ('PURCHASE_REQUEST', '物资采购申请'),
        ('INBOUND', '物资入库'),
        ('OUTBOUND', '物资出库'),
        ('DISPOSAL', '物资报废'),
        ('MAINTENANCE', '物资维修'),
        ('TRANSFER', '物资转移')
    ]

    STATUS_CHOICES = [
        ('PENDING_SUBMISSION', '待提交'),
        ('PENDING_APPROVAL', '待审批'),
        ('IN_APPROVAL', '审批中'),
        ('APPROVED', '已批准'),
        ('REJECTED', '已拒绝'),
        ('CANCELLED', '已取消'),
        ('COMPLETED', '已完成'),
        ('RETURNED_FOR_REVISION', '退回修改')
    ]

    id = models.AutoField(primary_key=True)  # 主键，自增
    operation_type = models.CharField(max_length=30, choices=OPERATION_TYPE_CHOICES, null=False, blank=False)  # 操作类型
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=False, blank=False)  # 审批状态
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间，自动添加当前时间
    updated_time = models.DateTimeField(auto_now=True)  # 更新时间，自动更新为当前时间
    applicant = models.ForeignKey(Member, related_name='applicant_records', on_delete=models.CASCADE, null=False)  # 申请人编号，外键关联到Memember表
    description = models.CharField(max_length=300, null=False, blank=False)  # 操作说明
    approver = models.ForeignKey(Member, related_name='approver_records', on_delete=models.CASCADE, null=False)  # 审批人编号，外键关联到Member表
    reply = models.CharField(max_length=300, null=False, blank=False)  # 答复

    def __str__(self):
        return f"审批记录 - {self.operation_type} - {self.status}"

    class Meta:
        db_table = 'approval_record'  # 指定数据库表名

class Material(models.Model):
    STATUS_CHOICES = [
        ('In', '库中'),
        ('BORROWING', '外借中'),
        ('OUT', '出库'),
        ('RETURNING', '归还中'),
        ('IN_MAINTENANCE', '维护中')
    ]

    DAMAGE_DEGREE_CHOICES = [
        ('INTACT', '完好'),
        ('SLIGHT', '轻微磨损'),
        ('MODERATE', '适度损坏，不影响使用'),
        ('SERIOUS', '严重损坏，无法使用')
    ]

    id = models.AutoField(primary_key=True)  # 主键，自增
    name = models.CharField(max_length=30, null=False, blank=False)  # 物资名称
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)  # 物资类别编号，外键关联到Category表
    # CASCADE: 当关联的对象被删除时，所有依赖于它的对象也将被自动删除
    price = models.FloatField(null=False, blank=False)  # 价格
    location = models.ForeignKey("Location", on_delete=models.CASCADE, null=False)  # 位置编号，外键关联到Location表
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False, blank=False)  # 物品状态
    damage_degree = models.CharField(max_length=20, choices=DAMAGE_DEGREE_CHOICES, null=False, blank=False)  # 损坏程度
    purchase_order = models.ForeignKey("PurchaseOrder", on_delete=models.CASCADE, null=False)  # 订购订单，外键关联到PurchaseOrder表

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'material'  # 指定数据库表名

class InventoryRecord(models.Model):
    # 出入库记录
    TYPE_CHOICES = [
        ('入库', '入库'),
        ('出库', '出库')
    ]

    id = models.AutoField(primary_key=True)  # 主键，自增
    item = models.ForeignKey(Material, on_delete=models.CASCADE, null=False)  # 物品编号，外键关联到Material表
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=False, blank=False)  # 出入库类型
    time = models.DateTimeField(auto_now_add=True)  # 出入库时间，自动添加当前时间
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)  # 操作员工编号，外键关联Member表
    remarks = models.CharField(max_length=300, null=True, blank=True)  # 备注信息
    approval = models.ForeignKey(ApprovalRecord, on_delete=models.CASCADE, null=True, blank=True)  # 审批记录编号，外键关联到ApprovalRecord表

    def __str__(self):
        return f"{self.type} - {self.item.name} - {self.time}"

    class Meta:
        db_table = 'inventory_record'  # 指定数据库表名

class MaintenanceRecord(models.Model):
    # 物资维护记录
    id = models.AutoField(primary_key=True)  # 主键，自增
    item = models.ForeignKey(Material, on_delete=models.CASCADE, null=False)  # 物资编号，外键关联到Material表
    time = models.DateTimeField(null=False, blank=False)  # 维护日期
    content = models.CharField(max_length=200, null=False, blank=False)  # 维护内容
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)  # 维护人员编号，外键关联到Member表
    approval = models.ForeignKey(ApprovalRecord, on_delete=models.CASCADE, null=True, blank=True)  # 审批记录编号，外键关联到ApprovalRecord表

    def __str__(self):
        return f"维护记录 - {self.item.name} - {self.time}"

    class Meta:
        db_table = 'maintenance_record'  # 指定数据库表名


class Supplier(models.Model):
    # 供应商
    id = models.AutoField(primary_key=True)  # 主键，自增
    name = models.CharField(max_length=50, null=False, blank=False)  # 供应商名称
    phone = models.CharField(max_length=20, null=False, blank=False)  # 联系电话
    email = models.CharField(max_length=50, null=True, blank=True)  # 联系邮箱
    address = models.CharField(max_length=200, null=False, blank=False)  # 地址

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'supplier'  # 指定数据库表名

class Supplier_Product(models.Model):
    # 供应商-商品
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)  # 供应商编号，外键关联到Supplier表
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)  # 物资类别编号，外键关联到Category表
    price = models.FloatField(null=False, blank=False)  # 价格
    quantity = models.IntegerField(null=False, blank=False)  # 可供应量

    def __str__(self):
        return f"{self.supplier.name} - {self.category.name}"

    class Meta:
        db_table = 'supplier_product'  # 指定数据库表名

class PurchaseOrder(models.Model):
    # 采购订单
    STATUS_CHOICES = [
        ('PROCURING', '采购中'),
        ('PROCURED', '已采购'),
        ('OVERDUE', '逾期'),
        ('UNQUALIFIED', '未满足要求的，与审批记录不相符')
    ]

    id = models.AutoField(primary_key=True)  # 主键，自增
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)  # 物资类别编号，外键关联到Category表
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)  # 供应商编号，外键关联到Supplier表
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间，自动添加当前时间
    finish_time = models.DateTimeField(null=True, blank=True)  # 完成时间
    quantity = models.IntegerField(null=False, blank=False)  # 实际数量
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False, blank=False)  # 订单状态
    approval = models.ForeignKey(ApprovalRecord, on_delete=models.CASCADE, null=False)  # 审批记录编号，外键关联到ApprovalRecord表

    def __str__(self):
        return f"采购订单 - {self.category.name} - {self.supplier.name} - {self.status}"

    class Meta:
        db_table = 'purchase_order'  # 指定数据库表名

class Warehouse(models.Model): # 仓库
    id = models.AutoField(primary_key=True)  # 主键，自增
    name = models.CharField(max_length=10, null=False, blank=False)  # 仓库名称

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'warehouse'  # 指定数据库表名
        indexes = [models.Index(fields=['name'], name='idx_warehouse_name')]  # B+树索引

class Zone(models.Model): # 区域
    id = models.AutoField(primary_key=True)  # 主键，自增
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=False)  # 仓库编号，外键关联到Warehouse表

    def __str__(self):
        return f"Zone {self.id} in {self.warehouse.name}"

    class Meta:
        db_table = 'zone'  # 指定数据库表名
        indexes = [models.Index(fields=['warehouse'], name='idx_zone_warehouse')]  # B+树索引

class Shelf(models.Model):  # 货架
    id = models.AutoField(primary_key=True)  # 主键，自增
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=False)  # 区域编号，外键关联到Zone表

    def __str__(self):
        return f"Shelf {self.id} in Zone {self.zone.id}"

    class Meta:
        db_table = 'shelf'  # 指定数据库表名
        indexes = [models.Index(fields=['zone'], name='idx_shelf_zone')]  # B+树索引

class Level(models.Model):  # 层级
    id = models.AutoField(primary_key=True)  # 主键，自增
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, null=False)  # 货架编号，外键关联到Shelf表

    def __str__(self):
        return f"Level {self.id} on Shelf {self.shelf.id}"

    class Meta:
        db_table = 'level'  # 指定数据库表名
        indexes = [models.Index(fields=['shelf'], name='idx_level_shelf')]  # B+树索引

class Location(models.Model):   # 位置
    id = models.AutoField(primary_key=True)  # 主键，自增
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False)  # 层级编号，外键关联到Level表
    available = models.BooleanField(default=True)  # 是否空闲，默认为真

    def __str__(self):
        return f"Location {self.id} on Level {self.level.id}"

    class Meta:
        db_table = 'location'  # 指定数据库表名
        indexes = [models.Index(fields=['level'], name='idx_location_level')]  # B+树索引

class StockWarning(models.Model):
    TYPE_CHOICES = [
        ('LOW_STOCK', '库存低于阈值'),
        ('EXPIRED', '过期'),
        ('DAMAGE', '损坏'),
        ('OTHER', '其他')
    ]

    id = models.AutoField(primary_key=True)  # 主键，自增
    item = models.ForeignKey(Material, on_delete=models.CASCADE, null=False)  # 物资编号，外键关联到Material表
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=False, blank=False)  # 警告类型

    def __str__(self):
        return f"库存警告 - {self.item.name} - {self.type}"

    class Meta:
        db_table = 'stock_warning'  # 指定数据库表名