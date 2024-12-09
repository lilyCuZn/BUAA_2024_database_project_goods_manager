# Generated by Django 3.2.25 on 2024-12-10 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('operation_type', models.CharField(blank=True, choices=[('PURCHASE_REQUEST', '物资采购申请'), ('MAINTENANCE', '物资维护申请')], max_length=30)),
                ('status', models.CharField(blank=True, choices=[('WAITING', '待确认'), ('REFUSE', '拒绝'), ('APPROVAL', '同意')], max_length=30)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('reply', models.CharField(blank=True, max_length=300)),
            ],
            options={
                'db_table': 'approval_record',
            },
        ),
        migrations.CreateModel(
            name='AutoMemberId',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('threshold', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='LeaseApply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='电话号码')),
                ('message', models.CharField(max_length=300, null=True, verbose_name='物资信息')),
                ('usage', models.CharField(max_length=300, null=True, verbose_name='物资用途')),
                ('status', models.CharField(choices=[('待确认', 'Waiting'), ('租赁中', 'Leasing'), ('拒绝', 'Refuse'), ('归还中', 'Returning'), ('已结束', 'Return')], max_length=4, null=True)),
                ('returnMessage', models.CharField(max_length=300, null=True)),
                ('createdTime', models.DateTimeField(auto_now_add=True)),
                ('finishTime', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': '用户申请',
                'verbose_name_plural': '用户申请',
                'db_table': 'UserApplication',
            },
        ),
        migrations.CreateModel(
            name='LeaseReturn',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('LEASING', '租赁中'), ('RETURNED', '已归还'), ('LOST', '已丢失'), ('OVERDUE', '已逾期')], max_length=20)),
                ('leaseTime', models.DateTimeField(auto_now_add=True)),
                ('returnTime', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'LeaseReturn',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'level',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Maintain_Material_Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.CharField(choices=[('REPAIRED', '修缮'), ('THROWN', '报废')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintainRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createdTime', models.DateTimeField(auto_now_add=True)),
                ('finishTime', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('FINISH', '已完成'), ('UNFINISH', '未完成')], max_length=20, null=True)),
            ],
            options={
                'db_table': 'maintain_record',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('In', '库中'), ('BORROWING', '租赁中'), ('IN_MAINTENANCE', '维护中'), ('DAMAGE', '损坏'), ('LOST', '已丢失'), ('THROWN', '已报废')], max_length=20)),
            ],
            options={
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('identity', models.CharField(choices=[('admin', '管理员'), ('member', '普通成员')], max_length=7)),
            ],
            options={
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('PROCURING', '采购中'), ('PROCURED', '已采购')], max_length=20)),
            ],
            options={
                'db_table': 'purchase_order',
            },
        ),
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'shelf',
            },
        ),
        migrations.CreateModel(
            name='StockWarning',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'stock_warning',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='Supplier_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
            ],
            options={
                'db_table': 'supplier_product',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'warehouse',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.warehouse')),
            ],
            options={
                'db_table': 'zone',
            },
        ),
        migrations.AddIndex(
            model_name='warehouse',
            index=models.Index(fields=['name'], name='idx_warehouse_name'),
        ),
        migrations.AddField(
            model_name='supplier_product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category'),
        ),
        migrations.AddField(
            model_name='supplier_product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.supplier'),
        ),
        migrations.AddField(
            model_name='stockwarning',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category'),
        ),
        migrations.AddField(
            model_name='shelf',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.zone'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='approval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.approvalrecord'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.member'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.supplier'),
        ),
        migrations.AddField(
            model_name='member',
            name='department_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.department'),
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category'),
        ),
        migrations.AddField(
            model_name='material',
            name='purchase_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.purchaseorder'),
        ),
        migrations.AddField(
            model_name='maintainrecord',
            name='approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.approvalrecord'),
        ),
        migrations.AddField(
            model_name='maintainrecord',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.member'),
        ),
        migrations.AddField(
            model_name='maintain_material_result',
            name='maintainId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.maintainrecord'),
        ),
        migrations.AddField(
            model_name='maintain_material_result',
            name='materialId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.material'),
        ),
        migrations.AddField(
            model_name='location',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.level'),
        ),
        migrations.AddField(
            model_name='level',
            name='shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.shelf'),
        ),
        migrations.AddField(
            model_name='leasereturn',
            name='materialId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.material'),
        ),
        migrations.AddField(
            model_name='leasereturn',
            name='userApplyId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.leaseapply'),
        ),
        migrations.AddField(
            model_name='leaseapply',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.member'),
        ),
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.member'),
        ),
        migrations.AddField(
            model_name='approvalrecord',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_records', to='web.member'),
        ),
        migrations.AddField(
            model_name='approvalrecord',
            name='approver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver_records', to='web.member'),
        ),
        migrations.AddIndex(
            model_name='zone',
            index=models.Index(fields=['warehouse'], name='idx_zone_warehouse'),
        ),
        migrations.AddIndex(
            model_name='shelf',
            index=models.Index(fields=['zone'], name='idx_shelf_zone'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['level'], name='idx_location_level'),
        ),
        migrations.AddIndex(
            model_name='level',
            index=models.Index(fields=['shelf'], name='idx_level_shelf'),
        ),
    ]
