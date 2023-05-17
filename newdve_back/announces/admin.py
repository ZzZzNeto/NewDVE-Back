from django.contrib import admin

from .models import Announce, Tag, Announce_image, Rating

class AnnounceAdmin(admin.ModelAdmin):
    search_fields = ["company_name"]
    readonly_fields = ["creator"]

class TagAdmin(admin.ModelAdmin):
    search_fields = ["tag_name"]

class Announce_imageAdmin(admin.ModelAdmin):
    search_fields = ["announce.company_name"]
    readonly_fields = ["announce"]

class RatingAdmin(admin.ModelAdmin):
    search_fields = ["announce.company_name"]
    readonly_fields = ["announce", "user"]

admin.site.register(Announce, AnnounceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Announce_image, Announce_imageAdmin)
admin.site.register(Rating, RatingAdmin)

