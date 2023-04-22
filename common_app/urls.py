from django.urls import path
from .views import *

urlpatterns = [
    path('file-upload-64', FileUploadBase64.as_view()),
    path('file-upload', FileUpload.as_view()),
    path('file-upload-delete/<int:file_id>', FileDelete.as_view()),
    # path('file-update/<int:file_id>', FileUpdate.as_view()),

]
