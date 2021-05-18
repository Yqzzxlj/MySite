from django.db import models
from django.contrib.auth.models import (
    AbstractUser, Group, Permission)

# Create your models here.

class User(AbstractUser):
    GENDER_UNKNOWN = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_PRIVATE = 3
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, '未知'),
        (GENDER_MALE, '男性'),
        (GENDER_FEMALE, '女性'),
        (GENDER_PRIVATE, '未说明'),
    )
    GENDER_CHOICES_MAP = {label: key for key, label in GENDER_CHOICES}

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        default_permissions = ()
    
    gender = models.PositiveSmallIntegerField(
        verbose_name='性别', choices=GENDER_CHOICES, default=GENDER_UNKNOWN,
    )
    age = models.PositiveSmallIntegerField(verbose_name='年龄', default=0)
    cell_phone_number = models.CharField(
        verbose_name='手机号', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    '''A mapping to User-Group Many-To-Many relationship.'''
    class Meta:
        verbose_name = '用户组'
        verbose_name_plural = '用户组'
        managed = False  # This model is managed by Django.
        db_table = 'mysite_auth_user_groups'
        default_permissions = ()

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name='用户',
                             on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name='用户组',
                              on_delete=models.CASCADE)

    def __str__(self):
        return '用户{}位于用户组{}中'.format(self.user_id, self.group_id)

class GroupPermission(models.Model):
    '''A mapping to Group-Permission Many-To-Many relationship.'''
    class Meta:
        verbose_name = '用户组权限'
        verbose_name_plural = '用户组权限'
        managed = False  # This model is managed by Django.
        db_table = 'auth_group_permissions'
        default_permissions = ()

    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, verbose_name='用户组',
                              on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, verbose_name='权限',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return '用户组{}拥有权限{}'.format(self.group_id, self.permission_id)
