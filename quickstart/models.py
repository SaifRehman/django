from __future__ import unicode_literals
from django.db import models
from django.utils.safestring import mark_safe
import os
from django.contrib.auth.models import User
from time import time
from django.forms import ModelForm
from django.contrib import admin

class Student(models.Model):
    phonenumber  = models.CharField(null=True,max_length = 15)
    age  = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    emiratesidimage = models.FileField(blank=True, null=True,upload_to=os.path.basename(os.path.dirname(os.path.realpath(__file__)))+"/images/emiratesid/",default="images/emiratesid/non.png")
    pk_student = models.OneToOneField(User)
    def image_tag(self):
        return mark_safe('<img src="%s"  />' % (self.passportidimage.path))
    class Meta:
        db_table = "Student"
        verbose_name = "Students"
        verbose_name_plural = "Students"
    def __unicode__(self):
        return self.phonenumber
class Department(models.Model):
    pk_department = models.ForeignKey(Student)
    departmentName = models.CharField(null=True,max_length = 50)
    class Meta:
        db_table = "Department"
        verbose_name = "Department"
        verbose_name_plural = "Departments"
    def __unicode__(self):
        return self.departmentName