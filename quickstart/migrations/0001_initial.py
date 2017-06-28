# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 21:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agencypersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licenseid', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('licenseidimage', models.ImageField(upload_to='quickstart/')),
                ('accepted', models.BooleanField(default=0)),
                ('agency_ID', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Agencypersonal',
                'verbose_name': 'Signed up Agency',
                'verbose_name_plural': 'Signed up Agency',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentName', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'Department',
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenumber', models.CharField(max_length=15, null=True)),
                ('age', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('emiratesidimage', models.FileField(blank=True, default='images/emiratesid/non.png', null=True, upload_to='quickstart/images/emiratesid/')),
                ('pk_student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Student',
                'verbose_name': 'Students',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Talentspersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emiratesid', models.CharField(max_length=50, null=True)),
                ('telephone', models.CharField(max_length=50, null=True)),
                ('passportid', models.CharField(max_length=50, null=True)),
                ('visaid', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('emiratesidimage', models.FileField(blank=True, default='images/emiratesid/non.png', null=True, upload_to='quickstart/images/emiratesid/')),
                ('passportidimage', models.FileField(blank=True, default='images/passportid/non.png', null=True, upload_to='quickstart/images/passportid/')),
                ('visaididimage', models.FileField(blank=True, default='images/emiratesid/non.png', null=True, upload_to='quickstart/images/visaid/')),
                ('accepted', models.BooleanField(default=0)),
                ('talentid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Talentspersonal',
                'verbose_name': 'Signed up Talents',
                'verbose_name_plural': 'Signed up Talents',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='pk_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.Student'),
        ),
    ]
