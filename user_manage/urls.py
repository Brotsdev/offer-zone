from django.urls import path
from .views import *

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('account-login', AccountLogin.as_view()),
    path('account-signup/<str:process_type>', AccountSignUp.as_view()),
    # path('account-login-verify/<str:user_type>', CustomAuthToken.as_view()),
]
