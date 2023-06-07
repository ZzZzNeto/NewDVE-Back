from django.contrib import admin

from .models import Announcement, Tag, Announcement_image, Rating

class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ["company_name"]

class TagAdmin(admin.ModelAdmin):
    search_fields = ["tag_name"]

class Announcement_imageAdmin(admin.ModelAdmin):
    search_fields = ["announcement.company_name"]

class RatingAdmin(admin.ModelAdmin):
    search_fields = ["announcement.company_name"]

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Announcement_image, Announcement_imageAdmin)
admin.site.register(Rating, RatingAdmin)

