'''Register URL routes in auth module.'''
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token, obtain_jwt_token
from django.urls import path


router = routers.SimpleRouter()
urlpatterns = router.urls

# JWT authentication and CAS authentication
AUTHENTICATION_URLS = [
    path('jwt-verify/', verify_jwt_token),
    path('jwt-retrieve/', obtain_jwt_token),
]

urlpatterns += AUTHENTICATION_URLS
