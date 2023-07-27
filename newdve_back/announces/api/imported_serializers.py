from rest_framework import serializers
from newdve_back.users.models import Address, User
from newdve_back.announces.models import Announcement

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name','profile_picture']
    
class SimpleAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id','company_name','curriculum']