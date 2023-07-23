import datetime
from rest_framework import serializers
from newdve_back.announces.models import Announcement, Announcement_image, Rating
from newdve_back.users.api.serializers import TagSerializer
from newdve_back.users.models import User

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
    expired = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id','company_name','company_image', 'main_image', 'rate', 'total_rates', 'city', 'tags', 'vacancies','expired']

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

    def get_expired(self, instance):
        now = datetime.datetime.now()
        if instance.deadline < now.date():
            return True
        else:
            return False
    
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