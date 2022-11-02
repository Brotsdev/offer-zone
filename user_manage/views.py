import traceback
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from dtuser_auth.models import UserAuthKey
from .models import LoginUser
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
            
            user_name = post_data['user_name']
            user_obj = LoginUser.objects.filter(Q(email=user_name) | Q(username=user_name) | Q(phone_number=user_name)).first()
            if user_obj and user_obj.is_active == False:
                return Response({"status":"400","message":"You are not a active user."})
            
            if "otp" in post_data:
                auth_check = UserAuthKey()
                if auth_check.validate_key(user_name):
                    token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({"status":status.HTTP_201_CREATED,"message":"Login Successfull.","data":{
                        "token":token,
                        "first_name":user_obj.first_name,
                        "last_name":user_obj.last_name,
                        "phone_code":user_obj.phone_code,
                        "phone_number":user_obj.phone_number,
                        "email":user_obj.email,
                    }})
                
            else:
                auth_key = UserAuthKey()
                auth_key.generate_token(user_name)
                return Response({"status":status.HTTP_201_CREATED,"message":"OTP succcessfully send.","data":auth_key.code})
            
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class CreateManagerAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            for key in ["name","company_name","email","phone"]:
                if key not in post_data:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":key+" Missing. Please add required keys"})
            
            user_obj = LoginUser()
            user_obj.first_name = post_data['name']
            user_obj.last_name = post_data['company_name']
            user_obj.email = post_data['email']
            user_obj.phone_number = post_data['phone']
            user_obj.is_manager = True
            user_obj.save()

        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def check_mail(self,email):
        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return True
    
        else:
            return False

class CreateCompanyAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            
            pass
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})