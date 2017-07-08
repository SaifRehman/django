from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
import datetime
import sys
import io
from django.core.files.storage import FileSystemStorage
from rest_framework import status
import datetime
import time
import base64
from models import Student
from models import Department
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

class signup(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        if not name:
            return Response({"error": "No name passed"})
        if not email:
            return Response({"error": "No email passed"})
        if not password:
            return Response({"error": "No passwords passed"})
        User.objects.create_user(username=name,
                                 email=email,
                                 password=password)
        return Response({"message": "Account has been sucessfully created"})

class create_student_record(APIView):
    permission_classes = (IsAuthenticated,)
    #queryset = Talentspersonal.objects.all()
    def post(self,request,format=None):
        try:
            readToken = request.META['HTTP_AUTHORIZATION']
            readToken = readToken.split(" ")
            readToken = readToken[1]
            payload = jwt.decode(readToken, 'practice', algorithms=['HS256'])
            pk_student = payload['user_id']
            check  = Student.objects.filter(pk_student_id=pk_student)
            if not check:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                base64data =  request.data.get("base64")
                base64data = base64.b64decode(base64data)
                filename = '/Users/saifrehman/Desktop/practice/media/quickstart/images/emiratesid/'+str(st)+".png"
                with open(filename, 'wb') as f:
                    f.write(base64data) 
                emiratesidimage = 'quickstart/images/emiratesid/'+str(st)+".png"
                phonenumber = request.data.get("phonenumber")
                age = request.data.get("age")
                database = Student(age=age,phonenumber=phonenumber,pk_student_id=pk_student,emiratesidimage=emiratesidimage)
                database.save() 
                return Response({"sucess":" true"}, status = 200)
            else:
                return Response({"sucess":" false"}, status = 400)
        except:
            return Response({"sucess":" false"}, status = 400)

class WatsonTest(APIView): 
    permission_classes = (IsAuthenticated,)
    def post(self, request, format = None):
        data = request.data.get("data")
        natural_language_understanding = NaturalLanguageUnderstandingV1(username="8528a131-21cc-49f2-9511-100f2e46c548",password="CubkctR6Xwhn",version="2017-02-27")
        response = natural_language_understanding.analyze(
        text=data,
        features=[
        Features.Entities(
        emotion=True,
        sentiment=True,
        limit=2
        ),
        Features.Keywords(
        emotion=True,
        sentiment=True,
        limit=2
        )
        ]
        )
        print response
        return Response({"Succes":response}, status=200)

class WatsonVision(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format = None):
        data = request.data.get("link")
        visual_recognition = VisualRecognitionV3('2016-05-20', api_key='dd25c6e9314862d037af87c6e5bad2c67fab1b81')
        response=visual_recognition.classify(images_url=data)
        return Response({"Succes":response}, status=200)# go to angular go to ang


#working good job
# now try to get data from api and show in ui
# make a new table and save some of the data in database
# this is hard i give up noooo. ok the scond one not imp, but do the first one. this is good the thing we did now. 
class create_department_record(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format = None):

        readToken = request.META['HTTP_AUTHORIZATION']
        readToken = readToken.split(" ")
        readToken = readToken[1]
        payload = jwt.decode(readToken, 'practice', algorithms=['HS256']) 
        pk_department_id = payload['user_id']
        department_name = request.data.get("departmentName")
        database = Department(departmentName=department_name, pk_department_id=pk_department_id)
        database.save()
        return Response({"Succes":"True"}, status=200)
    
class get_all_student(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        get = Student.objects.all().values('phonenumber', 'age','created_at','emiratesidimage')
        return Response({'students': list(get)})




# class talent_check_accepted(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = FileSerializer
#     #queryset = Talentspersonal.objects.all()
#     def get( self,request,format=None):
#         readToken = request.META['HTTP_AUTHORIZATION']

#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         print id
#         get =  Talentspersonal.objects.filter(talentid_id=id)
#         for info in get:
#             return Response({"accept":str(info.accepted)}, status = 200)

# class talent_upload_emiratesid(APIView):
#     permission_classes = (IsAuthenticated,)
#     # parser_classes = (MultiPartParser, FormParser,)
#     serializer_class = FileSerializer
#     queryset = Talentspersonal.objects.all()
#     def post( self,request,format=None):
#         ts = time.time()
#         st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#         base64data =  request.data.get("base64")
#         base64data = base64.b64decode(base64data)
#         filename = '/Users/saifrehman/Desktop/muse-backend/media/quickstart/images/emiratesid/'+str(st)+".png"
#         with open(filename, 'wb') as f:
#             f.write(base64data)
#         readToken = request.META['HTTP_AUTHORIZATION']
#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         print id
#         Talentspersonal.objects.filter(talentid_id=id).update(emiratesidimage='quickstart/images/emiratesid/'+str(st)+".png")
#         return Response({"sucess":" true"}, status = 200)

# class talent_upload_visaid(APIView):
#     permission_classes = (IsAuthenticated,)
#     # parser_classes = (MultiPartParser, FormParser,)
#     serializer_class = FileSerializer
#     queryset = Talentspersonal.objects.all()
#     def post( self,request,format=None):
#         ts = time.time()
#         st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#         base64data =  request.data.get("base64")
#         base64data = base64.b64decode(base64data)
#         filename = '/Users/saifrehman/Desktop/muse-backend/media/quickstart/images/visaid/'+str(st)+".png"
#         with open(filename, 'wb') as f:
#             f.write(base64data)
#         readToken = request.META['HTTP_AUTHORIZATION']
#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         print id
#         Talentspersonal.objects.filter(talentid_id=id).update(visaididimage='quickstart/images/visaid/'+str(st)+".png")
#         return Response({"sucess":" true"}, status = 200)

# class talent_upload_passportid(APIView):
#     permission_classes = (IsAuthenticated,)
#     # parser_classes = (MultiPartParser, FormParser,)
#     serializer_class = FileSerializer
#     queryset = Talentspersonal.objects.all()
#     def post( self,request,format=None):
#         ts = time.time()
#         st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#         base64data =  request.data.get("base64")
#         base64data = base64.b64decode(base64data)
#         filename = '/Users/saifrehman/Desktop/muse-backend/media/quickstart/images/passportid/'+str(st)+".png"
#         with open(filename, 'wb') as f:
#             f.write(base64data)
#         readToken = request.META['HTTP_AUTHORIZATION']
#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         print id
#         Talentspersonal.objects.filter(talentid_id=id).update(passportidimage='quickstart/images/passportid/'+str(st)+".png")
#         return Response({"sucess":" true"}, status = 200)
        
# class talent_information_upload(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Talentspersonal.objects.all()
#     def post( self,request,format=None):
#         emiratesid = request.data.get("emiratesid")
#         passportid = request.data.get("passportid")
#         visaid = request.data.get("visaid")
#         telephone = request.data.get("telephone")
#         readToken = request.META['HTTP_AUTHORIZATION']
#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         Talentspersonal.objects.filter(talentid_id=id).update(emiratesid=emiratesid,passportid=passportid,visaid=visaid,telephone=telephone)
#         return Response({"sucess":" true"}, status=200)

# class record_exist_talent(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         readToken = request.META['HTTP_AUTHORIZATION']
#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         get =  Talentspersonal.objects.filter(talentid_id=id)
#         print get
#         if not get:
#             return Response({"message": "0"})
#         else:
#             return Response({"message": "1"})

# class record_exist_agency(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         readToken = request.META['HTTP_AUTHORIZATION']
#         readToken = readToken.split(" ")
#         readToken = readToken[1]
#         payload = jwt.decode(readToken, 'muse', algorithms=['HS256'])
#         id = payload['user_id']
#         get =  Agencypersonal.objects.filter(agency_ID=id)
#         if not get:
#             return Response({"message": "0"})
#         else:
#             return Response({"message": "1"})
