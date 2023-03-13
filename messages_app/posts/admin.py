from django.contrib import admin
from .models import Messages
# Register your models here.
class InfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'like_count',)
    def like_count(self, obj):
        return obj.likes.all().count()
admin.site.register(Messages,InfoAdmin)
