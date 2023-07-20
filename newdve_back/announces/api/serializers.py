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

class ImageSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Announcement_image
        fields = ['image']

class CompanySeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']

class SimpleAnnouncementSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True) 
    city = serializers.SerializerMethodField()
    company_image = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    total_rates = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id','company_name','company_image', 'main_image', 'rate', 'total_rates', 'city', 'tags', 'vacancies', 'schedule']

    def get_city(self, instance):
        return f"{instance.address.city}/{instance.address.state}"
    
    def get_company_image(self, instance):
        serializer = CompanySeralizer(instance.creator)
        return serializer.data
    
    def get_main_image(self, instance):
        image = Announcement_image.objects.filter(announcement=instance).first()
        if image: 
            return ImageSeralizer(image).data
        else: 
            return None

    
    def get_rate(self, instance): 
        rates = Rating.objects.filter(announcement=instance)
        total = 0
        for rate in rates:
            total += rate.rate
        if rates.count() > 0:
            return round(total / rates.count(), 1)
        else:
            return 0
    
    def get_total_rates(self, instance):
        return Rating.objects.filter(announcement=instance).count()