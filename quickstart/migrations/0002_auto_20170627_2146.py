# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 21:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencypersonal',
            name='agency_ID',
        ),
        migrations.RemoveField(
            model_name='talentspersonal',
            name='talentid',
        ),
        migrations.DeleteModel(
            name='Agencypersonal',
        ),
        migrations.DeleteModel(
            name='Talentspersonal',
        ),
    ]
