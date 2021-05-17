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
