import traceback
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from app_security.models import UserAuthKey
from .models import *
from django.db.models import Q

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class AccountLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            if "user_name" not in post_data:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"User name key missing."})
            
            if not post_data['user_name']:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please enter a user name."})
            
            user_name = post_data['user_name']
            user_obj = LoginUser.objects.filter(Q(email=user_name) | Q(username=user_name) | Q(phone_number=user_name)).first()
            
            if not user_obj:
                return Response({"status":"400","message":"Please enter a valid user name."})
            
            if user_obj and user_obj.is_active == False:
                return Response({"status":"400","message":"You are not a active user."})
            
            if "otp" in post_data:
                auth_check = UserAuthKey()
                if user_obj and auth_check.validate_key(user_name,post_data['otp']):
                    token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({"status":status.HTTP_201_CREATED,"message":"Login Successfull.","data":{
                        "token":token.key,
                        "first_name":user_obj.first_name,
                        "last_name":user_obj.last_name,
                        "phone_code":user_obj.phone_code,
                        "phone_number":user_obj.phone_number,
                        "email":user_obj.email,
                    }})
                else:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Invalid OTP."})
                
            else:
                auth_key = UserAuthKey()
                auth_key.generate_token(user_name)
                return Response({"status":status.HTTP_201_CREATED,"message":"OTP succcessfully send.","data":auth_key.code})
            
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class AccountSignUp(APIView):
    permission_classes = [AllowAny]
    def post(self, request,process_type, *args, **kwargs):
        try:
            post_data = request.data
            
            if "phone_number" not in post_data or "phone_number" in post_data and not post_data['phone_number']:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Phone Numder key missing."})
            
            self.phone_number = post_data['phone_number']
            user_obj = LoginUser.objects.filter(Q(phone_number=self.phone_number)).first()
            if user_obj:
                return Response({"status":"400","message":"Phone number already exist."})
            
            if process_type == "phone-check":
                validate_phone = self.phone_validate()
                if not validate_phone:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please enter a valid phone."})

                auth_key = UserAuthKey()
                auth_key.generate_token(self.phone_number)
                LoginUserTemp.objects.filter(phone=self.phone_number).delete()
                return Response({"status":status.HTTP_201_CREATED,"message":"OTP succcessfully send.","data":auth_key.code})
            
            elif process_type == "otp-check":
                if "otp" in post_data and post_data['otp']:
                    auth_check = UserAuthKey()
                    if auth_check.validate_key(self.phone_number,post_data['otp']):
                        LoginUserTemp.objects.create(
                            phone=self.phone_number,
                            is_verified=True
                        )
                        return Response({"status":status.HTTP_201_CREATED,"message":"Phonenumber Successfull Verified.","data":{}})
                else:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Invalid otp or Phonenumber."})
                
                
            elif process_type == "profile-create":
                number_verified = LoginUserTemp.objects.filter(phone=self.phone_number,is_verified=True).first()
                if number_verified:
                    LoginUser.objects.create(
                            phone_number = self.phone_number,
                            email = post_data['email'] if 'email' in post_data else "",
                            username = post_data['username'] if 'username' in post_data else "",
                            first_name = post_data['first_name'] if 'first_name' in post_data else "",
                            last_name = post_data['last_name'] if 'last_name' in post_data else "",
                            is_shop = post_data['is_shop'] if 'is_shop' in post_data else False,
                            is_customer = post_data['is_customer'] if 'is_customer' in post_data else False,
                            image = post_data['image'] if 'image' in post_data else "",
                        )
                    LoginUserTemp.objects.filter(phone=self.phone_number).delete()
                    return Response({"status":status.HTTP_201_CREATED,"message":"Account Successfull Created.","data":post_data})
                else:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please verify your phone number.."})
            else:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Invalid operation."})
            
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def email_validate(self):
        
        pass

    def phone_validate(self):
        if self.phone_number:
            import phonenumbers
            if phonenumbers.is_possible_number(self.phone_number):
                return True
        return False