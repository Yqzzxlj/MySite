from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)

from auth.services import UserGroupService
import auth.models
from infra.mixins import HumanReadableValidationErrorMixin

User = get_user_model()

class PermissionSerializer(HumanReadableValidationErrorMixin,
                           serializers.ModelSerializer):
    '''Indicate how to serialize Permission instance.'''
    label = serializers.CharField(source='name')

    class Meta:
        model = Permission
        fields = ('id', 'codename', 'label')


class GroupSerializer(HumanReadableValidationErrorMixin,
                      serializers.ModelSerializer):
    '''Indicate how to serialize Group instance.'''

    class Meta:
        model = auth.models.Group
        fields = ('id', 'name',)


class GroupPermissionSerializer(BulkSerializerMixin,
                                HumanReadableValidationErrorMixin,
                                serializers.ModelSerializer):
    '''Indicate how to serialize GroupPermission instance.'''

    class Meta:
        model = auth.models.GroupPermission
        fields = ('id', 'group', 'permission')
        list_serializer_class = BulkListSerializer


class UserSerializer(HumanReadableValidationErrorMixin,
                     serializers.ModelSerializer):
    '''Indicate how to serialize User instance.'''
    gender_str = serializers.CharField(source='get_gender_display')

    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'first_name', 'last_name',
                  'email', 'is_active', 'date_joined',
                  'groups', 'gender_str', 'age', 'cell_phone_number')


class UserGroupSerializer(HumanReadableValidationErrorMixin,
                          serializers.ModelSerializer):
    '''Indicate how to serialize UserGroup instance.'''
    user_first_name = serializers.CharField(
        source='user.first_name', read_only=True)

    class Meta:
        model = auth.models.UserGroup
        fields = ('id', 'user', 'group', 'user_first_name')
        validators = [
            UniqueTogetherValidator(
                queryset=auth.models.UserGroup.objects.all(),
                fields=['user', 'group']
            )
        ]

    def create(self, validated_data):
        return UserGroupService.add_user_to_group(**validated_data)
