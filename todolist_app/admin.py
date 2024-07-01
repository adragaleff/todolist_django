from django.contrib import admin
from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')
    search_fields = ('name', )

admin.site.register(Task)
admin.site.register(License)
admin.site.register(CommentsTask)