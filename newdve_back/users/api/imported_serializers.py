from rest_framework import serializers
from newdve_back.announces.models import Announcement

class SimpleAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id','company_name','curriculum']