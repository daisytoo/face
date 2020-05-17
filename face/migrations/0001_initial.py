# Generated by Django 2.2.12 on 2020-05-16 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clazz',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(default='一年级一班', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Face',
            fields=[
                ('fid', models.AutoField(primary_key=True, serialize=False)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('mid', models.IntegerField(default=-1)),
                ('mname', models.CharField(default='no matching', max_length=30)),
                ('fimg', models.ImageField(max_length=200, upload_to='upload')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('tname', models.CharField(default='李小明', max_length=30)),
                ('ttel', models.CharField(max_length=11)),
                ('timg', models.ImageField(max_length=200, upload_to='')),
                ('clazz', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='face.Clazz')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('sname', models.CharField(default='李小明', max_length=30)),
                ('simg', models.ImageField(max_length=200, upload_to='')),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face.Clazz')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('pname', models.CharField(default='李明', max_length=30)),
                ('ptel', models.CharField(max_length=11)),
                ('pimg', models.ImageField(max_length=200, upload_to='')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face.Student')),
            ],
        ),
    ]