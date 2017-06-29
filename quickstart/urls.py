from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from views import hello_world
from api import *

urlpatterns = [
    url(r'^signup/$', signup.as_view(),name="post"),
    url(r'^student/create/$', create_student_record.as_view(),name="post"),
    url(r'^department/create/$', create_department_record.as_view(),name="post"),
    url(r'^student/getall/$', get_all_student.as_view(),name="get"),
    url(r'^student/count/$', get_number_of_student.as_view(),name="get"),

    # url(r'^talent/uploadpassportid/$', talent_upload_passportid.as_view(),name="post"),
    # url(r'^talent/accepted/$', talent_check_accepted.as_view(),name="post"),
    # url(r'^talent/uploadvisaid/$', talent_upload_visaid.as_view(),name="post"),
    # url(r'^talent/record/$', record_exist_talent.as_view(),name="post"),
    # url(r'^talent/info/$', talent_information_upload.as_view(),name="get"),
    # url(r'^agency/record/$', record_exist_agency.as_view(),name="get"),
    url(r'^login/', obtain_jwt_token),
]