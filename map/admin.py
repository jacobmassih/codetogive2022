from django.contrib import admin
from .models import Comment, Topic

class topic(admin.ModelAdmin):
    list_display = ["title", "author", "description", "date", "city", "label", "likes"]

class comment(admin.ModelAdmin):
    list_display = ["author", "comment", "date", "status", "topic"]

admin.site.register(Topic, topic)
admin.site.register(Comment, comment)