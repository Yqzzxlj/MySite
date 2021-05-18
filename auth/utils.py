'''Utility functions provided by auth module.'''
import hashlib
import os.path as osp

import guardian.shortcuts
from django.conf import settings
from django.contrib.auth.models import Group



def get_user_secret_key(user):
    '''Generate a secret key for a user.'''
    unhashed_key = '{}.{}'.format(
        settings.SECRET_KEY,  # Django secret key
        user.username,  # Username
        ).encode()
    sha1 = hashlib.new('sha1')
    sha1.update(unhashed_key)
    secret_key = sha1.hexdigest()
    return secret_key


def jwt_response_payload_handler(token, user=None, request=None):
    """Returns the response data for both the login and refresh views."""
    from auth.serializers import UserSerializer
    return {
        'user': UserSerializer(user).data,
        'token': token
    }

def assign_perm(perm_name, user_or_group, obj=None):
    '''Re-export assign_perm from django-guardian.'''
    ret = guardian.shortcuts.assign_perm(perm_name, user_or_group, obj)
    msg = (
        f'赋予用户(组) {user_or_group}'
        f' 对 {obj} 的 {perm_name} 权限'
    )
    prod_logger.info(msg)
    return ret


def remove_perm(perm_name, user_or_group, obj=None):
    '''Re-export remove_perm from django-guardian.'''
    return guardian.shortcuts.remove_perm(perm_name, user_or_group, obj)
  