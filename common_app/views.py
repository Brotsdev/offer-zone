from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from django.conf import settings
from django.core.files.base import ContentFile
import base64
import random
import string

from .models import FileManager
from .serializers import *
# Create your views here.



class FileUploadBase64(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            datalist = {}
            data = request.data
            if 'image_encode' in data and data['image_encode']:
                file = data['image_encode']
                file_exe = data['image_type'] if "image_type" in data else "png"
                output_string = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(10))
                imgname = output_string + "." + file_exe
                your_file = ContentFile(base64.b64decode(file),imgname)
                f = FileManager.objects.create(upload=your_file)
                datalist.update({"image":f.pk})
                return Response({
                    'status':"success",
                    'message': 'Image added successfully',
                    'response_code': status.HTTP_200_OK,
                    'data':datalist
                })
            return Response({
                    'status':"success",
                    'message': 'Image not added. Please check post data.',
                    'response_code': status.HTTP_200_OK,
                    'data':datalist
                })
        except Exception as e:
            message = str(e)     
            return Response({'status':'error','response_code':500,"message":message})

class FileDelete(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,file_id, **kwargs):
        try:
            FileManager.objects.filter(id=file_id).delete()
            return Response(
                {
                    'status': 'success',
                    'message': 'file delete successfullly.',
                    'response_code': status.HTTP_200_OK
                }
            )
        except Exception as e:
            message = str(e)
            return Response(
                {
                    'status': 'error', 
                    'response_code': 500, 
                    "message": "Unable to delete."
                }
            )


class FileUpload(generics.CreateAPIView):
    queryset = FileManager.objects.all()
    serializer_class = FileManagerSerializer
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        try:
            response = super().post(request, **kwargs)
            return Response(
                {
                    'status': 'success',
                    'message': 'image updated',
                    'response_code': status.HTTP_200_OK,
                    'data': response.data
                }
            )
        except Exception as e:
            message = str(e)
            return Response(
                {
                    'status': 'error', 
                    'response_code': 500, 
                    "message": "Upload Not Completed."
                }
            )
            