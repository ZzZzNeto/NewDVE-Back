from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group

from newdve_back.announces.api.serializers import TagSerializer
from newdve_back.users.api.imported_serializers import SimpleAnnouncementSerializer
from newdve_back.users.models import Address, User_file
from newdve_back.announces.models import Announcement

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
    inscriptions = serializers.SerializerMethodField()
    my_announcements = serializers.SerializerMethodField()
    address = AddressSerializer(required=False, read_only=True)
    group = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField('get_files', required=False, read_only=True)
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id","group","name","access","refresh","email","cnpj", "address", "profile_picture", "description", "contact_mail", "phone", "instagram", "linkedin", "inscriptions",
                  "twitter", "my_announcements", "ocupattion", "birth_date", "preference_tags", "portfolio", "schooling", "saved_announcements", "registration_ifrn", "course",'files']

    def get_my_announcements(self, instance):
        announcements = Announcement.objects.filter(creator=instance)
        return SimpleAnnouncementSerializer(announcements, many=True).data
    
    def get_group(self, instance):
        return instance.groups.all().first().name

    def get_inscriptions(self, instance):
        announcements = Announcement.objects.filter(inscripts__id=instance.id)
        serializer = SimpleAnnouncementSerializer(announcements, many=True)
        return serializer.data

    def get_refresh(self,instance):
        return self.context.get("refresh")

    def get_access(self,instance):
        return self.context.get("access")

    def get_files(self,instance):
        files = User_file.objects.filter(user=instance)
        serializer = User_fileSerializer(files,many=True)
        return serializer.data