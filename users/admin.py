from django.contrib import admin
from .models import *


class MyModelAdmin(admin.ModelAdmin):
    readonly_fields = ('bmr', 'amr', 'created')


# admin.site.register(Profile)
admin.site.register(Profile, MyModelAdmin)
admin.site.register(Weight)
