'''Provide services related to auth module.'''
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q

from auth.utils import assign_perm
from auth.models import UserGroup, User
from infra.utils import prod_logger

class PermissionService:
    '''Provide services for Permissons.'''
    # pylint: disable=redefined-builtin
    @classmethod
    @transaction.atomic()
    def assign_object_permissions(cls, user=None, instance=None):
        '''
        The function is used to provide permissions for releated user when
        an object is created (a teacher create a tranning record for exmaple).
        Parameters
        ----------
        user: User
            the current user who create the object.
        instance: Model
            a model instance
        Returns
        -------
        None
        '''
        # i: assgin User-Object-Permissions for the current user
        group = Group.objects.get(name='个人权限')
        cls._assign_group_permissions(group, user, instance)


class UserGroupService:
    '''
    Provide services for UserGroups.
    '''
    @staticmethod
    def add_user_to_group(user=None, group=None):
        '''Add a user to a group with notification.

        Parametsers
        ----------
        user: User
            related user
        group: Group
            related group
        Returns
        -------
        usergroup: UserGroup
        '''
        from infra.services import NotificationService

        with transaction.atomic():
            usergroup = UserGroup.objects.create(
                user=user, group=group)
            msg = (
                f'用户 {user.first_name}(工号: {user.username})'
                f' 被管理员添加至用户组 {group} 中'
            )
            prod_logger.info(msg)
            NotificationService.send_system_notification(user, msg)
            return usergroup
