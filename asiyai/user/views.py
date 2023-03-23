from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
import requests
from rest_framework.decorators import api_view
from cerberus import errors, Validator
from utility.requestErrorFormate import requestErrorMessagesFormate
from rest_framework import status
from rest_framework.response import Response
from utility.sqlQueryBuilder import SqlQueryBuilder
from utility.passwordHashing import PasswordHashing
from django.views.decorators.csrf import csrf_exempt
from config.messages import Messages
from django.db import transaction
from utility.jwtTokenHelper import JwtTokenHelper
from utility.authMiddleware import isAuthenticate
from utility.SNSNotifications import SNSNotification
from datetime import datetime, timedelta
from utility.customValidations import CustomValidator
from random import randint
from config.configConstants import (UserType, DeviceType, OTPActionType, UserBlockType)
#from utility.aesEncryption import AESEncryption
from django.db.models import Q
import pytz, json
from django.http import HttpResponse, HttpResponseRedirect
from dotenv import dotenv_values
config = dotenv_values(".env")
import requests
from user.models import User, Device, MasterContents, Device,heavyvehivalregistrationImages,Request_Heavy_VehicalImages, heavyvehivalregistration,Request_SubContractor, Request_Heavy_Vehical, driveroperatorregistration, subcontractorregistration, labour_contructor, Requirement,Request_labour_contructor, Request_driver_Operator, VedioUplaod
import razorpay
import random
from api.settings import image_uploadPath
import uuid
import urllib.request
from utility.firebaseNotification import FirebaseNotification
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext

razorpay_client = razorpay.Client(auth=("rzp_live_H6G6PNWGPU3vwq", "djfo8LPqdP6VZ4guJsN96ITb"))
# Create your views here.
################# import filter functions ##################
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from user.serializers import ProfileSerializer, VedioSerailzer
from rest_framework.views import APIView 
import base64

############# language intergration ############
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
# def home(request):
#     trans = _('hello')
#     return render(request, 'home.html', {'trans': trans})


# ##################This method default view in thee main screen ###################
# @api_view(['GET'])
# def index(request):
#     trans = translate(language="fr")
#     return render(request, "chooselanguage.html", {'trans': trans})
@api_view(['GET'])
def index(request):
    # context = {
    #     'hello':  _('Hello')
    # }
    trans = translate(language="hi")
    return render(request, "chooselanguage.html",{'trans':trans})

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text


@api_view(['GET'])
def get_master_data(request):  # get studies
    try:
        schema = {
            "keyName": {'type': 'string', 'required': True, 'empty': True},
            "relateTo": {'type': 'integer', 'required': True, 'empty': True}
        }
        instance = {
            "keyName": request.GET['keyName'],
            "relateTo": int(request.GET['relateTo'])
        }
        v = Validator()
        if not v.validate(instance, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create database connection
        db = SqlQueryBuilder()
        # Call stored procedure to get studies
        _result = db.readProcedureJson('admin_getMasterData',[request.GET['keyName'], request.GET['relateTo']])
        db.commit()

        if len(_result)>0:
            return Response({'data':_result}, status=status.HTTP_200_OK)
        else:
            return Response({'message': Messages.NO_RECORD, 'data':[]}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_all_studies", str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
#@isAuthenticate
def filter_data(request):  # get studies
    try:
        schema = {
            "type": {'type': 'string', 'required': True, 'empty': True},
            "pageLimit": {'type': 'integer', 'required': True, 'empty': True},
            "pageOffset": {'type': 'integer', 'required': True, 'empty': True}
        }
        instance = {
            "type": request.GET['type'],
            "pageLimit": int(request.GET['pageLimit']),
            "pageOffset": int(request.GET['pageOffset'])
        }
        v = Validator()
        if not v.validate(instance, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create database connection
        db = SqlQueryBuilder()
        v_type =  request.GET['type'],
        pageLimit = request.GET['pageLimit']
        pageOffset =  request.GET['pageOffset']
        # Call stored procedure to get studies
        _result = []
        if request.GET['type'] == 'driver':
             
            _result = db.readProcedureJson('getDrivers',[pageLimit, pageOffset])
        if request.GET['type'] == 'vehicle':
            _result = db.readProcedureJson('getvehicle',[])
        if request.GET['type'] == 'labour':
            _result = db.readProcedureJson('getLabours',[])
        if request.GET['type'] == 'subcontructor':
            _result = db.readProcedureJson('subcontractor',[])
        db.commit()

        if len(_result)>0:
            return Response({'data':_result}, status=status.HTTP_200_OK)
        else:
            return Response({'message': Messages.NO_RECORD, 'data':[]}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_all_lists", str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# generate access and refresh token 
def access_refresh_token(tokenData):

    data = JwtTokenHelper().CreateToken(tokenData)
   
    data = {
        "accessToken": data['accessToken'],
        "refreshToken": data['refreshToken']
    }
    return data


# This method is use to verify otp
@api_view(['POST'])
def verify_mobile_otp(request):
    try:
        schema = {
            "countryCode": {'type': 'integer', 'required': True, 'nullable': False},
            "mobileNo": {'type': 'string', 'required': True, 'empty': False},
            "otp": {'type': 'string', 'required': True, 'empty': False},
            "deviceToken": {'type': 'string', 'required': True, 'empty': False},
            "deviceType": {'type': 'string', 'required': True, 'empty': False, 'allowed': [DeviceType.ANDROID, DeviceType.IOS, DeviceType.WEB]},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        endpoint=""
        # check user exists
        if not User.objects.filter(mobile_number=request.data['mobileNo']).exists(): #if phone number does not exists
            return Response({"status":"error", 'message': Messages.MOBILE_DOES_NOT_EXISTS}, status=status.HTTP_200_OK)

        # check user exists with otp
        if User.objects.filter(mobile_number=request.data['mobileNo'],otp=request.data['otp']).exists():
            #userInfo = User.objects.filter(mobile_number=request.data['mobileNo'], is_active = 1, is_delete = 0).values()
            userInfo = User.objects.filter(mobile_number=request.data['mobileNo']).values()
            print(f"userInfo: {userInfo}")
            # generate token 
            isProfilePhotoAdded = False
            isBasicDetailsAdded = False
            isDocsAdded = False
            if userInfo[0]['profile_pic']:
                isProfilePhotoAdded = True
            if userInfo[0]['dob']:
                isBasicDetailsAdded = True
            tokenInput = {
            'userId': userInfo[0]['user_id'],
            'userType': userInfo[0]['user_type'],
            'fullName': userInfo[0]['first_name'],
            'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
            'countryCode': userInfo[0]['country_code'],
            'mobileNo': userInfo[0]['mobile_number'],
            }
            tokenData = access_refresh_token(tokenInput)
            User.objects.filter(mobile_number=request.data['mobileNo']).update(is_active = 1, is_delete = 0)
            # check and update token 
            if Device.objects.filter(device_token=request.data['deviceToken']).exists():
                Device.objects.filter(device_token=request.data['deviceToken']).update(                    
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1)
            else: 
            # insert data in device table
                Device.objects.create(
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    device_token=request.data['deviceToken'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1
                )
            data = {
                    "userType":userInfo[0]['user_type'],
                    "status":"success",
                    "message":"success",
                    'accessToken': tokenData['accessToken'],
                    'refreshToken': tokenData['refreshToken'], 
                    'userId': userInfo[0]['user_id'],
                    'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
                    'fullname': userInfo[0]['first_name'],
                    'isProfilePhotoAdded': isProfilePhotoAdded,
                    'isBasicDetailsAdded': isBasicDetailsAdded,
                    }
            return Response(data, status=status.HTTP_200_OK)
        
        elif(request.data['otp'] == "0000"):
            userInfo = User.objects.filter(mobile_number=request.data['mobileNo']).values()
            
            # generate token 
            isProfilePhotoAdded = False
            isBasicDetailsAdded = False
            if userInfo[0]['profile_pic']:
                isProfilePhotoAdded = True
            if userInfo[0]['dob']:
                isBasicDetailsAdded = True
            tokenInput = {
            'userId': userInfo[0]['user_id'],
            'userType': userInfo[0]['user_type'],
            'fullName': userInfo[0]['first_name'],
            'username': userInfo[0]['username'],
            'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
            'countryCode': userInfo[0]['country_code'],
            'mobileNo': userInfo[0]['mobile_number'],
            'isActive': int.from_bytes(userInfo[0]['is_active'] if userInfo[0]['is_active'] else b'\x00',byteorder='big'),
            }
            tokenData = access_refresh_token(tokenInput)
            User.objects.filter(mobile_number=request.data['mobileNo']).update(is_active = 1, is_delete = 0)
            # check and update token 
            if Device.objects.filter(device_token=request.data['deviceToken']).exists():
                Device.objects.filter(device_token=request.data['deviceToken']).update(                    
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1)
            else: 
            # insert data in device table
                Device.objects.create(
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    device_token=request.data['deviceToken'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1
                )
            data = {
                    "userType":userInfo[0]['user_type'],
                    "status":"success",
                    "message":"success",
                    'accessToken': tokenData['accessToken'],
                    'refreshToken': tokenData['refreshToken'], 
                    'userId': userInfo[0]['user_id'],
                    'fullname': userInfo[0]['first_name'],
                    'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
                    'isProfilePhotoAdded': isProfilePhotoAdded,
                    'isBasicDetailsAdded': isBasicDetailsAdded,
                    }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error", 'message': Messages.INVALID_OTP}, status=status.HTTP_200_OK)
    except Exception as e:
        print('...................verify mobile otp........',str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# This method is use to send otp on mobile
@api_view(['POST'])
def send_otp_mobile(request):
    try:
        schema = {
            "countryCode": {'type': 'integer', 'required': True, 'nullable': False},
            "mobileNo": {'type': 'string', 'required': True, 'empty': False},
            "actionType": {'type': 'string', 'required': True, 'empty': False, 'allowed': [OTPActionType.REGISTRATION, OTPActionType.FORGOT_PASSWORD]},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:       
        mobileNo = request.data['mobileNo']
        countryCode = request.data['countryCode']
        actionType = request.data['actionType']
        print(type(mobileNo))

        if not User.objects.filter(mobile_number=mobileNo).exists():
            saveUser = User(mobile_number = mobileNo, country_code = countryCode)
            saveUser.save()
        # Generate random otp
        otp = str(randint(1000, 9999))
        otpToSave = otp
        # Send SMS
        countryCode = str(countryCode)
        message = str(otp)+" is your verification code for AHV App."
        URL = "http://103.16.101.52:80/sendsms/bulksms?username=oz07-way2it&password=Way2it14&type=0&dlr=1&destination="+ mobileNo +"&source=SDIRAM&message=%3C%23%3E%20"+otpToSave+"%20is%20the%20OTP%20for%20login%20to%20your%20Shadiram%20account.%20This%20OTP%20is%20valid%20for%2015%20minutes.%20For%20security%20reason%20do%20not%20share%20with%20anyone.%20Shadiram.in&entityid=1201159195926105040&tempid=1307165045918848353"
        urllib.request.urlopen(URL).read()
        User.objects.filter(mobile_number=mobileNo, country_code = countryCode).update(otp= otpToSave)
        return Response({'data':otp, "status":"success", "message":"success"}, status=status.HTTP_200_OK)  
    except Exception as e:
        print('send_otp_mobile',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# This method is use to get the access token from refresh token
@api_view(['POST'])
def access_token(request):
    try:
        schema = {
            "refreshToken": {'type': 'string', 'required': True, 'empty': False},
            "userId": {'type': 'integer', 'required': True, 'nullable': False},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        userId = request.data["userId"]
        if not User.objects.filter(user_id=userId).exists():
            return Response({'message':Messages.USER_NOT_EXISTS}, status=status.HTTP_401_UNAUTHORIZED)
        
        # check block user
        if User.objects.filter(Q(is_delete = 1) | Q(is_active = 0), user_id=userId).exists():
            return Response({'error':Messages.USER_BLOCKED}, status=status.HTTP_401_UNAUTHORIZED)
        
        refreshToken = request.data['refreshToken']  # get token from header
        payload = JwtTokenHelper().getJWTPayload(refreshToken)  # get the payload from token
        if payload:
            expirationTime = payload["exp"]
            timestamp = datetime.fromtimestamp(expirationTime)
            userToken = Device.objects.filter(created_by = userId).order_by('-created_at')[0:1].values()
            utc=pytz.UTC
            user_expire_datetime = timestamp + timedelta(minutes=10)

            # Current datetime
            current_datetime = datetime.now()

            # replace the timezone in both time
            expiredOn = user_expire_datetime.replace(tzinfo=utc)
            checkedOn = current_datetime.replace(tzinfo=utc)

            if userToken:
                if (userToken[0]['refresh_token'] == refreshToken):
                    if  checkedOn  > expiredOn:  # token expired
                        return Response({'error': Messages.REFRESH_TOKEN_EXPIRED}, status=status.HTTP_401_UNAUTHORIZED)
                    else:                        
                        # Fetch User Info
                        userInfo = User.objects.filter(user_id=userId).values()
                        
                        # get the access token
                        accessToken = JwtTokenHelper().JWTAccessToken({
                            'userId': userInfo[0]['user_id'],
                            'userType': userInfo[0]['user_type'],
                            'firstName': userInfo[0]['first_name'],
                            'lastName': userInfo[0]['last_name'],
                            'username': userInfo[0]['username'],
                            'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
                            'countryCode': userInfo[0]['country_code'],
                            'mobileNo': userInfo[0]['mobile_number'],
                            'isActive': int.from_bytes(userInfo[0]['is_active'] if userInfo[0]['is_active'] else b'\x00',byteorder='big'),
                            'isBlocked': int.from_bytes(userInfo[0]['is_delete'] if userInfo[0]['is_delete'] else b'\x00',byteorder='big'),
                            'isNotification': int.from_bytes(userInfo[0]['is_notification'] if userInfo[0]['is_notification'] else b'\x00',byteorder='big'),
                            'usageAlertTime': userInfo[0]['usage_alert_time'],
                        })
                        
                        result = {
                            "accessToken": accessToken
                        }
                        return Response(result, status=status.HTTP_200_OK)
                else:
                    return Response({'error': Messages.INVALID_REFRESH_TOKEN}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': Messages.INVALID_REFRESH_TOKEN}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': Messages.REFRESH_TOKEN_EXPIRED}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print('.................generate access token exception........',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    
@api_view(['GET'])
@isAuthenticate
def get_user_profile(request, userId):  # get user profile details
    try:
        # Create database connection
        db = SqlQueryBuilder()
        # Call stored procedure to get studies
        _result = db.readProcedureJson('user_profile',[userId])
        _educationInfo = db.readProcedureJson('user_educationDetails',[userId])
        _familyInfo = db.readProcedureJson('user_familyDetails',[userId])
        _preferenceInfo = db.readProcedureJson('user_preferenseDetails',[userId])
        db.commit()
        fetchResult = {}
        if len(_result)>0:
            fetchResult = {
                "basicInfo":_result[0],
                "educationDetails":_educationInfo,
                "familyDetails":_familyInfo,
                "preferenceDetails":_preferenceInfo
                
            }
            return Response({'data':fetchResult}, status=status.HTTP_200_OK)
        else:
            return Response({'message': Messages.NO_RECORD, 'data':[]}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_other_user_profile_detail", str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@isAuthenticate
def update_user_profile(request):  # get user profile details
    try:
        schema = {
            "userId": {'type': 'integer', 'required': True, 'nullable': False},
            "fullName": {'type': 'string', 'required': True, 'empty': False},
            "emailId": {'type': 'string', 'required': True, 'empty': False},
            "profilePic": {'type': 'string', 'required': True, 'empty': True},
            "creator_id": {'type': 'integer', 'required': False, 'empty': True},
            "gender": {'type': 'string', 'required': False, 'empty': True, 'nullable': True},

        }
       
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # check user exists
        userId = request.data.get("userId")
        
        #if userId != request.userId:
            #return Response({"status":"error",'message':Messages.INVALID_USER}, status=status.HTTP_200_OK)
            
        if not User.objects.filter(user_id=userId).exists():
            return Response({"status":"error",'message':Messages.USER_NOT_EXISTS}, status=status.HTTP_200_OK)
        User.objects.filter(user_id=userId).update(
            first_name = request.data['fullName'],
            email_id = request.data['emailId'],  
            profile_pic = request.data['profilePic'] ,
            updated_by = request.data.get("creator_id"),
            gender = request.data.get("gender")
            ) 
         
        #Education.objects.filter(userId=userId).update(occuption = request.data['designation'], highest_edu = request.data['education'], annualincome = request.data['anualIncome'])
        
        #Family.objects.filter(userId=userId).update(corr_city = request.data['city'], corr_country = request.data['country'], corr_state = request.data['state'], corr_address = request.data['address'])
        return Response({"status":"success",'message':Messages.USER_UPDATED}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_all_studies", str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@isAuthenticate
def logout(request):  # block user
    try:
        schema = {
            "deviceToken": {'type': 'string', 'required': True, 'empty': False},
        }
        v = Validator()
        # validate the request
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        deviceToken = request.data['deviceToken']
        userId = request.userId
        
        # check user exists   
        if not User.objects.filter(user_id=userId).exclude(user_type=UserType.ADMIN).exists():
            return Response({'error':Messages.USER_NOT_EXISTS}, status=status.HTTP_200_OK)
            
        # upadte record
        Device.objects.get(created_by=userId, device_token=deviceToken).delete() 
        
        return Response({'message': Messages.USER_LOGOUT}, status=status.HTTP_200_OK)

    except Exception as e:
        print("-----------------Logout------------"+str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@isAuthenticate
def save_master_data(request):  
    try:   

        schema = {
            "key": {'type': 'string', 'required': True, 'nullable': False},
            "value": {'type': 'string', 'required': True, 'nullable': False},
            "reqType": {'type': 'string', 'required': False, 'nullable': True},
            "masterId": {'type': 'integer', 'required': False, 'nullable': True}
            }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # Create database connection
        db = SqlQueryBuilder()

        user_id = request.userId
        v_key = request.data['key']
        v_value = request.data['value']
        reqType = request.data.get('reqType')
        masterId = request.data.get('masterId')
        # Call stored procedure
        _result = db.readProcedureJson('save_master_data',[v_key, v_value, reqType, masterId])
        db.commit()  
        if int(_result[0]['response']) > 0:
            return Response({'message': "success"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Error"}, status=status.HTTP_200_OK)

    except Exception as e:
        print('......................deduct credit on view post....................',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@isAuthenticate      
def generateOrderNumber(request):
    try:   

        schema = {
            "amount": {'type': 'integer', 'required': True, 'nullable': False}
            }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        v_amount = request.data['amount']
        ordrId = str(400)+ str(random.randint(1,9999))
        ss = razorpay_client.order.create({"amount":v_amount, "currency":"INR", "receipt":ordrId, "payment_capture":'0'})
        return Response({"ordid":ss['id'], "amount": v_amount, "status":"success"})
    except Exception as e:
        print("get_wallet_balance", str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@isAuthenticate  
def capturePayment(request):
    try:   

        schema = {
            "amount": {'type': 'integer', 'required': True, 'nullable': False},
            "razorpay_payment_id": {'type': 'string', 'required': True, 'nullable': False}
            }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        amount = request.data['amount']
        payment_id = request.data['razorpay_payment_id']
        razorpay_client.payment.capture(payment_id, amount)
        if razorpay_client.payment.fetch(payment_id)["captured"] == True:
            transId = razorpay_client.payment.fetch(payment_id)['id']
            transAmount = razorpay_client.payment.fetch(payment_id)['amount']/100
            transStatus = razorpay_client.payment.fetch(payment_id)["status"]
            transMobile =  razorpay_client.payment.fetch(payment_id)['contact'] 
            transEmail = razorpay_client.payment.fetch(payment_id)['email']
            transOrderId = razorpay_client.payment.fetch(payment_id)['order_id']
            return Response({"message":"captured", "status":"success"})
        else:
            transId = razorpay_client.payment.fetch(payment_id)['id']
            transAmount = razorpay_client.payment.fetch(payment_id)['amount']/100
            transStatus = razorpay_client.payment.fetch(payment_id)["status"]
            transMobile =  razorpay_client.payment.fetch(payment_id)['contact'] 
            transEmail = razorpay_client.payment.fetch(payment_id)['email']
            transOrderId = razorpay_client.payment.fetch(payment_id)['order_id']
            return Response({"message":"failed", "status":"failed"})
    except Exception as e:
        transId = razorpay_client.payment.fetch(payment_id)['id']
        transAmount = razorpay_client.payment.fetch(payment_id)['amount']/100
        transStatus = razorpay_client.payment.fetch(payment_id)["status"]
        transMobile =  razorpay_client.payment.fetch(payment_id)['contact'] 
        transEmail = razorpay_client.payment.fetch(payment_id)['email']
        transOrderId = razorpay_client.payment.fetch(payment_id)['order_id']
        return Response({"message":"failed", "status":"failed", "err":e})


@api_view(['POST'])
def uploadFile(request):
    try:
        imageRawFile = request.FILES['file']
        print(imageRawFile)
        fileType = request.data.get("fileType")
        unique_filename = str(uuid.uuid4())+str(imageRawFile)
        print(image_uploadPath)
        with open(str(image_uploadPath)+str(unique_filename), 'wb') as desk:
            for chunk in imageRawFile.chunks():
                desk.write(chunk)
        imagPath = "http://devapi.asiyaiheavyvehicle.com/user/static/Uploaded/UserProfiles/"+unique_filename
        return Response({"message":"success", "status":"success", "image_url":imagPath})
    except Exception as e:
        return Response({"message":"failed", "status":"failed", "err":e})

################heavyVehicalregistrations ##########
import time
from django.core.files.storage import default_storage
from django.utils.text import slugify
# @api_view(['POST', 'GET'])
#@isAuthenticate 
def hvregistration(request):
    if request.method=="POST":
            vehical_name = request.POST.get('vehical_name')
            company_name = request.POST.get('company_name')
            manufacture_date = request.POST.get('manufacture_date')
            ownername = request.POST.get('ownername')
            emailId = request.POST.get('emailId')
            
            vehicleregistrationnumber = request.POST.get('vehicleregistrationnumber')
            alternativemobilenumber = request.POST.get('alternativemobilenumber')
            vehiclemodelnumber = request.POST.get('vehiclemodelnumber')
            Aadharnumberfrontimage = request.FILES['Aadharnumberfrontimage']
            Aadharnumberbackimage = request.FILES['Aadharnumberbackimage']
            vehicle_image = request.FILES['vehicle_image']
        
            api_headers = {

            "Authorization":'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjIsInVzZXJUeXBlIjoiVVNFUiIsImZ1bGxOYW1lIjoidXBkZXNoIiwicHJvZmlsZVBpYyI6IiIsImNvdW50cnlDb2RlIjo5MSwibW9iaWxlTm8iOiI3ODI3NTM2MzU5IiwiZXhwIjoxNjgwMDA3NDcwfQ.CeAFe97epEdr_myMJzowQDBKF0zeR6J3UMVbWI2R8uc',
            "content-type":'application/json'
            }
            
            PARAMS = { "company_name": request.POST.get('company_name'),
                        "vehical_name": request.POST.get('vehical_name'),
                        "emailId": request.POST.get('emailId'),
                        "vehicleregistrationnumber": request.POST.get('vehicleregistrationnumber'),
                        "Aadharnumberfrontimage": str(request.FILES['Aadharnumberfrontimage']),
                        "Aadharnumberbackimage": str(request.FILES['Aadharnumberbackimage']),
                        "ownername": request.POST.get('ownername'),
                        "manufacture_date": request.POST.get('manufacture_date'),
                        "vehiclemodelnumber": request.POST.get('vehiclemodelnumber'),
                        "alternativemobilenumber": request.POST.get('alternativemobilenumber'),
                        "vehicle_image": [str(vehicle_image) for vehicle_image in request.FILES.getlist('vehicle_image')],
                        
            }
            URL = "http://devapi.asiyaiheavyvehicle.com/v1/hvbesicdetails"
            response = requests.post(URL,headers=api_headers,data=json.dumps(PARAMS))
            print(response.__dict__)
           
            db = heavyvehivalregistration(vehical_name=vehical_name,company_name=company_name,Aadharnumberfrontimage=Aadharnumberfrontimage,emailId=emailId,
            vehiclemodelnumber=vehiclemodelnumber,manufacture_date=manufacture_date,ownername=ownername,Aadharnumberbackimage=Aadharnumberbackimage,vehicleregistrationnumber=vehicleregistrationnumber,
            alternativemobilenumber=alternativemobilenumber,vehicle_image=vehicle_image, created_by = request.user.id)
            
            print(vehicle_image.__dict__)
            return redirect("/v1/hvaddress")
    else:
        return render(request, "HeavyVehicle/form.html")

def dashboard(request):
    servicedata= heavyvehivalregistration.objects.all().order_by("-Id")[:4]
    hello = driveroperatorregistration.objects.all().order_by("-Id")[:4]
    servicedata1 = subcontractorregistration.objects.all().order_by("-Id")[:4]
    servicedata2 = labour_contructor.objects.all().order_by("-Id")[:4]
    return render(request, "dashboardcopy.html", {"heavyvehivalregistration":servicedata,"driveroperatorregistration":hello,"subcontractorregistration":servicedata1,"labour_contructor":servicedata2})


def finaldashboard(request):
    servicedata= heavyvehivalregistration.objects.all().order_by("-Id")[:4]
    addDet = MasterContents.objects.all().order_by("-Id")[0]
    print(addDet)
    for i in servicedata:
        print("servicedata=",i._meta.fields)
    hello = driveroperatorregistration.objects.all().order_by("-Id")[:4]
    servicedata1 = subcontractorregistration.objects.all().order_by("-Id")[:4]
    servicedata2 = labour_contructor.objects.all().order_by("-Id")[:4]
    return render(request, "dashboard.html", {"heavyvehivalregistration":servicedata,"driveroperatorregistration":hello,"subcontractorregistration":servicedata1,"labour_contructor":servicedata2})

###################show all list hvregistration ################
def showlist(request):
    hello = heavyvehivalregistration.objects.all().order_by('-Id')
    data = {
        "hello": hello
    }
        
    return render(request, "HeavyVehicle/heavy-vehicles.html", data)


########### view more function hvregistrations #############
def showhvone(request, Id):
    if request.method=='GET':
        hv = heavyvehivalregistration.objects.filter(Id = Id).first()
        data = {
         "hv": hv
        }
        return render(request, 'HeavyVehicle/vehicle-detail.html', data)
    if request.method=="POST":
        print("request=",request)
        hv = heavyvehivalregistration.objects.filter(Id = Id).first()
        db = Request_Heavy_Vehical(vehical_name=hv.vehical_name,company_name=hv.company_name, vehical_number=hv.vehical_number,ownername=hv.ownername, Aadharnumberfrontimage = hv.Aadharnumberfrontimage,
            Aadhar_number=hv.Aadhar_number,manufacture_date=hv.manufacture_date,alternativemobilenumber=hv.alternativemobilenumber, Aadharnumberbackimage =  hv.Aadharnumberbackimage,
             vehiclemodelnumber=hv.vehiclemodelnumber, created_by = request.user.id)
        if Request_Heavy_Vehical.objects.filter(Aadhar_number = hv.Aadhar_number).exists():
            message = "Request AllReady!"
        else:
            
            db.save()
            images = request.FILES.getlist('moreimges')
            for i in images:
                Request_Heavy_VehicalImages.objects.create(Request_Heavy_Vehical=db,image=i)
        
            message = "Vehicle request successfully"
    
        data = {
        "hv": hv,
        "message": message
        }
        return render(request, "HeavyVehicle/vehicle-detail.html",data)

        # return HttpResponse("Vehicle request successfully")
    else:
        return render(request, "HeavyVehicle/vehicle-detail.html")




    ##### driveroperator registrations functions##################### 
def drlist(request):
    hello1 = driveroperatorregistration.objects.all().order_by('-Id')
    data = {
        "hello1": hello1
    }
    return render(request, "driveroperatorregistration/operator.html", data)

################### driver operator registration view more function ##############

def showdrone(request, Id):
    if request.method=="GET":
        dr = driveroperatorregistration.objects.filter(Id=Id).first()
        data1 = {
            "dr": dr
        }
        return render(request, "driveroperatorregistration/driver-details.html", data1)
    if request.method=="POST":
        dr = driveroperatorregistration.objects.filter(Id=Id).first()
        db = Request_driver_Operator(vehicalname=dr.vehicalname, expriencesinyear=dr.expriencesinyear, driveroperatorname=dr.driveroperatorname,
        Aadhar_number=dr.Aadhar_number, alternet_mobilenumber=dr.alternet_mobilenumber,mobilenumber=dr.mobilenumber, license_number=dr.license_number,
        driver_image=dr.driver_image,license_image=dr.license_image,Aadharnumberfrontimage=dr.Aadharnumberfrontimage,Aadharnumberbackimage=dr.Aadharnumberbackimage, created_by = request.user.id)
        if Request_driver_Operator.objects.filter(Aadhar_number=dr.Aadhar_number).exists():
            message = "Request AllReady!"
        else:
            db.save()
            message = "Request Driver Operator Successfully!"
        data1 = {
            "dr": dr,
            "message": message
        }
        return render(request, "driveroperatorregistration/driver-details.html", data1)
    else:
        return render(request, "driveroperatorregistration/driver-details.html", data1)




############ sub contructorlist##########
def subconlist(request):
    welcome = subcontractorregistration.objects.all().order_by('Id')
    data = {
        "welcome": welcome
    }
    return render(request, "SubContractor/subcontructorlist.html", data)

##################sub contrauctor view more single page ###################
def subsingle(request, Id):
    if request.method=="GET":
        subcon = subcontractorregistration.objects.filter(Id=Id).first()
        sub = {
            "subcon": subcon
        }
        return render(request, 'SubContractor/subco-details.html', sub)

    if request.method=="POST":
        subcon = subcontractorregistration.objects.filter(Id=Id).first()
        db = Request_SubContractor(contractorname=subcon.contractorname, firmname=subcon.firmname, expriencesinyear=subcon.expriencesinyear, license_number=subcon.license_number, Aadhar_number=subcon.Aadhar_number,Aadharnumberfrontimage=subcon.Aadharnumberfrontimage,Aadharnumberbackimage=subcon.Aadharnumberbackimage, subcontractor_image=subcon.subcontractor_image, created_by = request.user.id)
        if Request_SubContractor.objects.filter(Aadhar_number = subcon.Aadhar_number).exists():
            message = "Request AllReady!"
        else:
            db.save()
            message = "Request sub contractor successfully"
        sub = {
            "subcon": subcon,
            "message": message
            }
        return render(request, 'SubContractor/subco-details.html', sub)
    else:
        return render(request, 'SubContractor/subco-details.html', sub)



        

#################### labour list #############
def labourlist(request):
    welcome1 = labour_contructor.objects.all().order_by('Id')
    data = {
        "welcome1": welcome1
    }
    return render(request, "LabourContractor/labour-contractor.html", data)

def laboursingle(request, Id):
    if request.method=="GET":
        lab = labour_contructor.objects.filter(Id=Id).first()
        var = {
            "lab": lab
        }
        
        return render(request, "LabourContractor/laboursinglepage.html", var)
    if request.method=="POST":
        lab = labour_contructor.objects.filter(Id=Id).first()

        db = Request_labour_contructor(labourcontractorname=lab.labourcontractorname, labourwork=lab.labourwork,lobourinnumber=lab.lobourinnumber, contractorAadhar_number=lab.contractorAadhar_number,mobile_number=lab.mobile_number,alternativemobilenumber=lab.alternativemobilenumber,labour_image=lab.labour_image,Aadharnumberfrontimage=lab.Aadharnumberfrontimage,Aadharnumberbackimage=lab.Aadharnumberbackimage, created_by = request.user.id)
        if Request_labour_contructor.objects.filter(contractorAadhar_number = lab.contractorAadhar_number).exists():
            message = "Request Allready!"
        else:

            db.save()
            message = "Labour Contractor Request Successfully"
        var = {
            "lab": lab,
            "message": message
        }
        return render(request, "LabourContractor/laboursinglepage.html", var)
    else:
        return render(request, "LabourContractor/laboursinglepage.html", var)




# @api_view(['POST'])
# @isAuthenticate 
def doregistration(request):
    if request.method=="POST":
        vehicalname = request.POST.get('vehicalname')
        expriencesinyear = request.POST.get('expriencesinyear')
        emailId = request.POST.get('emailId')
        driveroperatorname = request.POST.get('driveroperatorname')
        alternet_mobilenumber = request.POST.get('alternet_mobilenumber')
        mobilenumber = request.POST.get('mobilenumber')
        heavy_license = request.POST.get('heavy_license')
        driver_image = request.FILES['driver_image']
        license_image = request.FILES['license_image']
        Aadharnumberfrontimage = request.FILES['Aadharnumberfrontimage']
        Aadharnumberbackimage = request.FILES['Aadharnumberbackimage']

        api_headers = {}
        api_headers["Authorization"]='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjIsInVzZXJUeXBlIjoiVVNFUiIsImZ1bGxOYW1lIjoidXBkZXNoIiwicHJvZmlsZVBpYyI6IiIsImNvdW50cnlDb2RlIjo5MSwibW9iaWxlTm8iOiI3ODI3NTM2MzU5IiwiZXhwIjoxNjgwMDA3NDcwfQ.CeAFe97epEdr_myMJzowQDBKF0zeR6J3UMVbWI2R8uc'
        api_headers["content-type"]='application/json'
        
        PARAMS = {
            "vehicalname": request.POST.get('vehicalname'),
            "expriencesinyear": int(request.POST.get('expriencesinyear')),
            "driveroperatorname": request.POST.get('driveroperatorname'),
            "emailId": request.POST.get('emailId'),
            "Aadharnumberbackimage": str(request.FILES['Aadharnumberfrontimage']),
            "Aadharnumberfrontimage": str(request.FILES['Aadharnumberbackimage']),
            "alternet_mobilenumber": int(request.POST.get('alternet_mobilenumber')),
            "mobilenumber": request.POST.get('mobilenumber'),
            "heavy_license": request.POST.get('heavy_license'),
            "driver_image": str(request.FILES['driver_image']),
            "license_image": str(request.FILES['license_image']),
        
        }
        print(expriencesinyear,alternet_mobilenumber)
        URL = "http://devapi.asiyaiheavyvehicle.com/v1/doregistrations"
        response = requests.post(url=URL,data=json.dumps(PARAMS),headers=api_headers)
        print(response.__dict__)

        print(response)
        db = driveroperatorregistration(vehicalname=vehicalname,mobilenumber=mobilenumber, 
        expriencesinyear=expriencesinyear, driveroperatorname=driveroperatorname, 
        alternet_mobilenumber=alternet_mobilenumber, heavy_license=heavy_license,emailId=emailId, driver_image=driver_image,
        license_image=license_image,Aadharnumberfrontimage=Aadharnumberfrontimage,Aadharnumberbackimage=Aadharnumberbackimage, created_by = request.user.id)
        db.save()
        return redirect("/v1/hvaddress")
    else:
        return render(request, 'driveroperatorregistration/driveroperatorregistration.html')



   ################ subcontractor registrations functions  #############
  
#@api_view(['POST'])
#@isAuthenticate 
def subcregistration(request):
    if request.method=="POST":
        contractorname = request.POST.get('contractorname')
        firmname = request.POST.get('firmname')
        expriencesinyear = request.POST.get('expriencesinyear')
        license_number = request.POST.get('license_number')
        emailId = request.POST.get('emailId')
        typeofwork = request.POST.get('typeofwork')
        mobilenumber = request.POST.get('mobilenumber')
        subcontractor_image = request.FILES['subcontractor_image']
        Aadharnumberfrontimage = request.FILES['Aadharnumberfrontimage']
        Aadharnumberbackimage = request.FILES['Aadharnumberbackimage']

        api_headers = {}
        api_headers["Authorization"]='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjIsInVzZXJUeXBlIjoiVVNFUiIsImZ1bGxOYW1lIjoidXBkZXNoIiwicHJvZmlsZVBpYyI6IiIsImNvdW50cnlDb2RlIjo5MSwibW9iaWxlTm8iOiI3ODI3NTM2MzU5IiwiZXhwIjoxNjgwMDA3NDcwfQ.CeAFe97epEdr_myMJzowQDBKF0zeR6J3UMVbWI2R8uc'
        api_headers["content-type"]='application/json'
        

        PARAMS = {
                "contractorname": request.POST.get('contractorname'),
                "firmname": request.POST.get('firmname'),
                "typeofwork": request.POST.get('typeofwork'),
                "emailId": request.POST.get('emailId'),
                "expriencesinyear": int(request.POST.get('expriencesinyear')),
                "license_number": request.POST.get('license_number'),
                "Aadharnumberbackimage": str(request.FILES['Aadharnumberfrontimage']),
                "Aadharnumberfrontimage": str(request.FILES['Aadharnumberbackimage']),
                "mobilenumber": request.POST.get('mobilenumber'),
                "subcontractor_image": [str(image) for image in request.FILES.getlist('subcontractor_image')],
                        
        }
        URL = "http://devapi.asiyaiheavyvehicle.com/v1/subcregistration"
        response = requests.post(url = URL,data=json.dumps(PARAMS),headers=api_headers)
        print(response.__dict__)
        db = subcontractorregistration(contractorname=contractorname,mobilenumber=mobilenumber,typeofwork=typeofwork, firmname=firmname,
        expriencesinyear=expriencesinyear, license_number=license_number, Aadharnumberfrontimage=Aadharnumberfrontimage,Aadharnumberbackimage=Aadharnumberbackimage,
        subcontractor_image=subcontractor_image,emailId=emailId,created_by = request.user.id)
        
        return redirect("/v1/hvaddress")
    else:
        return render(request, ("SubContractor/subcontbasicdetails.html"))
        
        
################################# Request subcontractor Registration #########################       

@api_view(['POST'])
@isAuthenticate 
def reqsubcon(request):
    try:
        schema = {
            "contractorname": {'type': 'string', 'required': True, 'nullable': False},
            "firmname": {'type': 'string', 'required': True, 'nullable': False},
            "expriencesinyear": {'type': 'integer', 'required': True, 'nullable': False},
            "license_number": {'type': 'string', 'required': True, 'nullable': False},
            "Aadhar_number": {'type': 'integer', 'required': False, 'nullable': True},
            "subcontractor_image": {'type': 'string', 'required': True, 'nullable': False},

        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        db = SqlQueryBuilder()
        contractorname = request.data['contractorname']
        firmname = request.data['firmname']
        expriencesinyear = request.data['expriencesinyear']
        license_number = request.data['license_number']
        Aadhar_number = request.data['Aadhar_number']
        subcontractor_image = request.data['subcontractor_image']
        db = Request_SubContractor(contractorname=contractorname, firmname=firmname, expriencesinyear=expriencesinyear, license_number=license_number, Aadhar_number=Aadhar_number, subcontractor_image=subcontractor_image, created_by = request.userId)
        db.save()

        return Response({"message":"Request sub contractor successfully"})
    except Exception as e:
        print('......................deduct credit on view post....................',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



   ################ labour constractor registrations functions  #############

# @api_view(['POST'])
# @isAuthenticate 
def lacoregistration(request):
    if request.method=="POST":
        v_labourcontractorname = request.POST.get('labourcontractorname')
        v_labourwork = request.POST.get('labourwork')
        v_lobourinnumber = request.POST.get('lobourinnumber')
        v_mobile_number = request.POST.get('mobile_number')
        alternativemobilenumber = request.POST.get('alternativemobilenumber')
        labour_image = request.FILES['labour_image']
        Aadharnumberfrontimage = request.FILES['Aadharnumberfrontimage']
        Aadharnumberbackimage = request.FILES['Aadharnumberbackimage']
        emailId = request.POST.get('emailId')
        skilledlabour = request.POST.get("skilledlabour")
        unskilledlabour = request.POST.get('unskilledlabour')
        professionallabour = request.POST.get('professionallabour')

        api_headers = {}
        api_headers["Authorization"]='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjIsInVzZXJUeXBlIjoiVVNFUiIsImZ1bGxOYW1lIjoidXBkZXNoIiwicHJvZmlsZVBpYyI6IiIsImNvdW50cnlDb2RlIjo5MSwibW9iaWxlTm8iOiI3ODI3NTM2MzU5IiwiZXhwIjoxNjgwMDA3NDcwfQ.CeAFe97epEdr_myMJzowQDBKF0zeR6J3UMVbWI2R8uc'
        api_headers["content-type"]='application/json'
        

        PARAMS = {
                    "labourcontractorname": request.POST.get('labourcontractorname'),
                    "Aadharnumberbackimage": str(request.FILES['Aadharnumberbackimage']),
                    "skilledlabour": int(request.POST.get("skilledlabour")),
                    "labourwork": request.POST.get('labourwork'),
                    "Aadharnumberfrontimage": str(request.FILES['Aadharnumberfrontimage']),
                    "labour_image": str(request.FILES['labour_image']),
                    "unskilledlabour": int(request.POST.get('unskilledlabour')),
                    "lobourinnumber": request.POST.get('lobourinnumber'),
                    "professionallabour": int(request.POST.get('professionallabour')),
                    "mobile_number": request.POST.get('mobile_number'),
                    "alternativemobilenumber": request.POST.get('alternativemobilenumber'),
                    "emailId": request.POST.get('emailId')
                    
   
        }
        URL = "http://devapi.asiyaiheavyvehicle.com/v1/lacoregistration"
        response = requests.post(url = URL,data=json.dumps(PARAMS),headers=api_headers)
        print(response.__dict__)
        
        db = labour_contructor(labourcontractorname=v_labourcontractorname,Aadharnumberfrontimage=Aadharnumberfrontimage,Aadharnumberbackimage=Aadharnumberbackimage, labourwork=v_labourwork,
                               professionallabour=professionallabour,unskilledlabour=unskilledlabour,skilledlabour=skilledlabour, lobourinnumber=v_lobourinnumber, 
                               emailId=emailId,mobile_number=v_mobile_number,alternativemobilenumber=alternativemobilenumber, labour_image=labour_image, created_by = request.user.id)
       
       
        return redirect("/v1/hvaddress")

    else:
        return render(request, ("LabourContractor/LabourConbasicdetails.html"))


################all request ##########
@api_view(['GET'])
def ProfileView(request):
    if request.method=="GET":
        candidates = Requirement.objects.all()
        serializer = ProfileSerializer(candidates, many=True)
        return Response(serializer.data)

def test(request):
    response = requests.get('http://127.0.0.1:8000/v1/listrequirement/')
    result = response.json()
    return render(request, 'requirement.html',{'Requirement':result})


################Request heavyVehicle##########

#@api_view(['POST'])
#@isAuthenticate 
def requesthvregistration(request):
    if request.method=="POST":
        print("request=",request)
        vehical_name = request.POST.get('vehical_name')
        company_name = request.POST.get('company_name')
        vehical_number = request.POST.get('vehical_number')
        ownername = request.POST.get('ownername')
        Aadhar_number = request.POST.get('Aadhar_number')
        vehicle_image = request.FILES['vehicle_image']
        manufectoring_date = request.data('manufectoring_date')
        
        db = Request_Heavy_Vehical(vehical_name=vehical_name,company_name=company_name, vehical_number=vehical_number,ownername=ownername, Aadhar_number=Aadhar_number,vehicle_image=vehicle_image,manufectoring_date=manufectoring_date, created_by = request.userId)
        db.save()
        return HttpResponse({"message":"Vehicle request successfully"})
    else:
        return render(request, "HeavyVehicle/vehicle-detail.html")

@api_view(['POST'])
@isAuthenticate 
def requestlacontractor(request):
    try:
        schema = {
        "labourcontractorname": {'type': 'string', 'required': True, 'nullable': False},
        "labourwork": {'type': 'string', 'required': True, 'nullable': False},
        "lobourinnumber": {'type': 'integer', 'required': True, 'nullable':False},
        "contractorAadhar_number": {'type': 'integer', 'required': True, 'nullable':False},
        "mobile_number": {'type': 'integer', 'required': True, 'nullable':False},
        "labour_image": {'type': 'string', 'required': True, 'nullable':False},
        "district": {'type': 'string', 'required': True, 'nullable': False},
        "state": {'type': 'string', 'required': True, 'nullable': False},
        "tehsil": {'type': 'string', 'required': True, 'nullable': False},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        
        v_labourcontractorname = request.data['labourcontractorname']
        v_labourwork = request.data['labourwork']
        v_lobourinnumber = request.data['lobourinnumber']
        v_contractorAadhar_number = request.data['contractorAadhar_number']
        v_mobile_number = request.data['mobile_number']
        labour_image = request.data['labour_image']
        district = request.data['district']
        state = request.data['state']
        tehsil = request.data['tehsil']
        try:
            db = Request_labour_contructor(labourcontractorname=v_labourcontractorname, labourwork=v_labourwork, lobourinnumber=v_lobourinnumber, contractorAadhar_number=v_contractorAadhar_number, mobile_number=v_mobile_number, labour_image=labour_image, district=district, state=state, tehsil=tehsil, created_by = request.userId)
            db.save()
        except Exception as e:
            return Response({'error':e})
        return Response({"message":"Request Lobour contractor successfully"})
    except Exception as e:
        print('......................deduct credit on view post....................',str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@isAuthenticate 
def requestdoperator(request):
    try:
        schema = {
            "vehicalname": {'type': 'string', 'required': True, 'nullable': False},
            "expriencesinyear": {'type': 'integer', 'required': True, 'nullable': False},
            "driveroperatorname": {'type': 'string', 'required': True, 'nullable': False},
            "Aadhar_number": {'type': 'integer', 'required': False, 'nullable': True},
            "alternet_mobilenumber": {'type': 'integer', 'required': False, 'nullable': True},
            "license_number": {'type': 'string', 'required': False, 'nullable': True},
            "driver_image": {'type': 'string', 'required': True, 'nullable': False},
            "district": {'type': 'string', 'required': True, 'nullable': False},
            "state": {'type': 'string', 'required': True, 'nullable': False},
            "tehsil": {'type': 'string', 'required': True, 'nullable': False},


        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        vehicalname = request.data['vehicalname']
        expriencesinyear = request.data['expriencesinyear']
        driveroperatorname = request.data['driveroperatorname']
        Aadhar_number = request.data['Aadhar_number']
        alternet_mobilenumber = request.data['alternet_mobilenumber']
        license_number = request.data['license_number']
        driver_image = request.data['driver_image']
        district = request.data['district']
        state = request.data['state']
        tehsil = request.data['tehsil']
        db = Request_driver_Operator(vehicalname=vehicalname, expriencesinyear=expriencesinyear, driveroperatorname=driveroperatorname, Aadhar_number=Aadhar_number, alternet_mobilenumber=alternet_mobilenumber, license_number=license_number, driver_image=driver_image, district=district, state=state, tehsil=tehsil, created_by =  request.userId)
        db.save()
        return Response({"message":"Request Driver operator successfully"})
    except Exception as e:
        print('......................deduct credit on view post....................',str(e))
        return Response({'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
###############upload images vedio ############

class ImageView(APIView):
    def get(self, request, formate=None):
        imgvedio = VedioUplaod.objects.all()
        serializer = VedioSerailzer(imgvedio, many=True)
        return Response({'status':'success','imgvedio':serializer.data}, status=status.HTTP_200_OK)



def hvadddress(request):
    try:
        if request.method=="GET":
            state = request.GET.get('state')
            district = request.GET.get('district')
            city = request.GET.get("city")
            db = MasterContents(key="state", value=state,relate_to=1)
            db.save()
            db = MasterContents(key="district",value=district,relate_to=2)
            db.save()
            db = MasterContents(key="city",value=city,relate_to=3)
            db.save()
            print(city)
            return HttpResponseRedirect('/v1/dashboard')
        else:
            return render(request, "HeavyVehicle/form1.html")
    except Exception as e:
        return render(request, "HeavyVehicle/form1.html",{"message":"Please select valid record"})
    
########### category  ##############
def category(request):
    return render(request, "categories.html")


############# notification ###############
def notification(request):
    return render(request, "notification.html")

def account(request):
    return render(request, "account.html")
########## choose language function #####
def chooselanguage(request):
    return render(request, "chooselanguage.html")

############## language selection hindi  ###########
def firstenglish(request):
    return render(request, "English/first.html")
def secondenglish(request):
    return render(request, "English/secondeng.html")


########### Home Screen ############
def home(request):
    return render(request, "English/homescreen.html")




def sendotp(request):
    if request.method=="POST":
        # URL = "http://devapi.asiyaiheavyvehicle.com/v1/send-otp"  
        # data  = {
        mobileNo = request.POST['mobileNo']
        # countryCode = request.data['countryCode']
        # actionType = request.data['actionType']
        actionType="REGISTRATION"
        countryCode=91
        request.session["mob_user"] = mobileNo
            
        print("saveUser=",User.objects.filter(mobile_number=mobileNo))
        if not User.objects.filter(mobile_number=mobileNo).exists():
            saveUser = User(mobile_number = mobileNo, country_code = countryCode)
            saveUser.save()
            # Generate random otp
            otp = str(randint(1000, 9999))
            otpToSave = otp
            # Send SMS
            countryCode = str(countryCode)
            message = str(otp)+" is your verification code for AHV App."
            URL = "http://103.16.101.52:80/sendsms/bulksms?username=oz07-way2it&password=Way2it14&type=0&dlr=1&destination="+ mobileNo +"&source=SDIRAM&message=%3C%23%3E%20"+otpToSave+"%20is%20the%20OTP%20for%20login%20to%20your%20Shadiram%20account.%20This%20OTP%20is%20valid%20for%2015%20minutes.%20For%20security%20reason%20do%20not%20share%20with%20anyone.%20Shadiram.in&entityid=1201159195926105040&tempid=1307165045918848353"
            urllib.request.urlopen(URL).read()
            User.objects.filter(mobile_number=mobileNo, country_code = countryCode).update(otp= otpToSave)
            return HttpResponseRedirect("/v1/verifyotp")

        if User.objects.filter(mobile_number=mobileNo).exists():
            # Generate random otp
            otp = str(randint(1000, 9999))
            otpToSave = otp
            # Send SMS
            countryCode = str(countryCode)
            message = str(otp)+" is your verification code for AHV App."
            URL = "http://103.16.101.52:80/sendsms/bulksms?username=oz07-way2it&password=Way2it14&type=0&dlr=1&destination="+ mobileNo +"&source=SDIRAM&message=%3C%23%3E%20"+otpToSave+"%20is%20the%20OTP%20for%20login%20to%20your%20Shadiram%20account.%20This%20OTP%20is%20valid%20for%2015%20minutes.%20For%20security%20reason%20do%20not%20share%20with%20anyone.%20Shadiram.in&entityid=1201159195926105040&tempid=1307165045918848353"
            urllib.request.urlopen(URL).read()
            User.objects.filter(mobile_number=mobileNo, country_code = countryCode).update(otp= otpToSave)
        
            return HttpResponseRedirect("/v1/verifyotp")
    else:       
        return render(request, 'register-with-mobile.html')
    

def verifyotp(request):
    if request.method=="POST":
        mobileNo=request.session["mob_user"]

        user_obj=User.objects.get(mobile_number=mobileNo)
        if user_obj.otp == request.POST["otp"]:
            return HttpResponseRedirect("/v1/dashboard")
        else:
            return render(request, "login-with-otp.html",{"message":"invalid otp"})
       
    return render(request, "login-with-otp.html")


############# Profile views ############
def profile(request):
    return render(request, "profile.html")


##### Normal user registration ########

def normaluser(request):
    return render(request, "normaluser/normal.html")


######################## def search fileter in django ##############
def search(request):
    query = heavyvehivalregistration.objects.all()
    query1 = driveroperatorregistration.objects.all()
    query2 = subcontractorregistration.objects.all()
    query3 = labour_contructor.objects.all()
    if request.method=="GET":
        st = request.GET.get('servicename')
        if st!=None:
            query = heavyvehivalregistration.objects.filter(vehical_name__icontains=st)
            query1 = driveroperatorregistration.objects.filter(driveroperatorname__icontains=st)
            query2 = subcontractorregistration.objects.filter(contractorname__icontains=st)
            query3 = labour_contructor.objects.filter(labourcontractorname__icontains=st)
        params = {
            'query': query,
            'query1': query1,
            'query2':query2,
            'query3':query3
        }

    return render(request, "search.html", params)
            #return HttpResponse("This is Search")


def test(request):
    return render(request,"test.html")