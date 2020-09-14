from django.contrib.auth.models import User
from bucket.models import Bucket, Todo
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class BucketSerializer(serializers.ModelSerializer):
    created_name = serializers.SerializerMethodField()

    class Meta:
        model = Bucket
        fields = ("id", "name", "created_by", "created_name", "created", "modified")

    def get_created_name(self, obj):
        return obj.created_by.username if obj.created_by else ''


class TodoSerializer(serializers.ModelSerializer):
    created_name = serializers.SerializerMethodField()
    bucket_name = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ("id", "task", "created_by", "created_name", "created", "modified", "bucket_name", "task_bucket", "is_completed")

    def get_created_name(self, obj):
        return obj.created_by.username if obj.created_by else ''

    def get_bucket_name(self, obj):
        return obj.task_bucket.name if obj.task_bucket else ''
