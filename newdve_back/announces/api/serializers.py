from rest_framework import serializers
from newdve_back.users.models import User
from newdve_back.announces.api.imported_serializers import AddressSerializer, SimpleUserSerializer, SimpleAnnouncementSerializer

from newdve_back.announces.models import Announcement, Tag, Announcement_image, Rating

class InscripsCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class Announcement_imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement_image
        fields = ['id','image','announcement']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, required=False)
    address = AddressSerializer(read_only=True)
    creator = SimpleUserSerializer(read_only=True, required=False)
    inscripts = SimpleUserSerializer(many=True, read_only=True, required=False)
    images = serializers.SerializerMethodField('get_images', required=False)

    class Meta:
        model = Announcement
        fields = ['company_name','tags','schedule','salary','journey','vacancies','deadline','benefits','requeriments','description','address',
                  'curriculum','course','total_workload','inscripts','creator','images']
        
    def get_images(self, instance):
        images = Announcement_image.objects.filter(announcement=instance)
        serializer = Announcement_imageSerializer(images, many=True)
        return serializer.data

class RatingSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(required=False, read_only=True)
    announcement = SimpleAnnouncementSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id','rate','user','announcement']

