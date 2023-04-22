
from .models import *
from django.db.models.functions import Concat
from django.db.models import Value,F
from django.conf import settings

    
def get_files_info(file_id):
    try:
        file_obj = FileManager.objects.get(id=file_id)
        return file_obj.upload.url
    except Exception as e:
        return ""

def get_files_info_bulk(file_ids):
    try:
        files_urls = list(FileManager.objects.filter(id__in=file_ids).values_list('upload',flat=True).all())
        return files_urls
    except Exception as e:
        return []

def get_files_id_check(file_ids):
    try:
        files_ids = list(FileManager.objects.filter(id__in=file_ids).values_list('id',flat=True).all())
        return files_ids
    except Exception as e:
        return False

def generate_urls(image_list):
    generated_url = []
    for url_value in image_list:
        if type(url_value) == str:
            generated_url.append(settings.STATIC_URL + url_value)
    
    return generated_url

def image_url_mapping(data_list):
    generated_url = []
    for image_dict in data_list:
        if "image" in image_dict:
            image_url = settings.STATIC_URL + image_dict["image"]
            image_dict["image"] = image_url
        generated_url.append(image_dict)
    
    return generated_url

def get_files_dict(file_ids):
    try:
        files_urls = FileManager.objects.filter(id__in=file_ids).values('upload','id','user_code').order_by('folder_name').all()
        for file_obj in files_urls:
            file_obj['upload'] = settings.MEDIA_URL + file_obj["upload"]
        return files_urls
    except Exception as e:
        import  traceback
        traceback.print_exc()
        return []