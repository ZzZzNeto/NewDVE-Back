from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group

from newdve_back.announces.api.serializers import TagSerializer
from newdve_back.users.api.imported_serializers import SimpleAnnouncementSerializer
from newdve_back.users.models import Address, User_file

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class User_fileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_file
        fields = ['id','file']

class UserSerializer(serializers.ModelSerializer):
    preference_tags = TagSerializer(many=True, required=False, read_only=True)
    saved_announcements = SimpleAnnouncementSerializer(many=True, required=False, read_only=True)
    address = AddressSerializer(required=False, read_only=True)
    groups = GroupSerializer(many=True)
    files = serializers.SerializerMethodField('get_files', required=False, read_only=True)

    class Meta:
        model = User
        fields = ["groups","name", "email","cnpj", "address", "profile_picture", "description", "contact_mail", "phone", "instagram", "linkedin", 
                  "twitter", "ocupattion", "birth_date", "preference_tags", "portfolio", "schooling", "saved_announcements", "registration_ifrn", "course",'files']

    def get_files(self,instance):
        files = User_file.objects.filter(user=instance)
        serializer = User_fileSerializer(files,many=True)
        return serializer.data
