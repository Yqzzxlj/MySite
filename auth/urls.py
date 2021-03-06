'''Register URL routes in auth module.'''
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token, obtain_jwt_token
from django.urls import path

import django_cas.views as cas_views
import auth.views

router = routers.SimpleRouter()
router.register(r'users', auth.views.UserViewSet)
router.register(r'groups', auth.views.GroupViewSet)
router.register(r'user-groups', auth.views.UserGroupViewSet)
router.register(r'permissions', auth.views.PermissionViewSet)
router.register(r'group-permissions', auth.views.GroupPermissionViewSet)
urlpatterns = router.urls

# JWT authentication and CAS authentication
AUTHENTICATION_URLS = [
    path('jwt-verify/', verify_jwt_token),
    path('jwt-retrieve/', obtain_jwt_token),
    path('login/', cas_views.LoginView.as_view(), name='cas-login'),
    path('logout/', cas_views.LogoutView.as_view(), name='cas-logout'),
]

urlpatterns += AUTHENTICATION_URLS
