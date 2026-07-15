from django.contrib import admin
from .models import BodyData, DietRecord, SportRecord

admin.site.register(BodyData)
admin.site.register(DietRecord)
admin.site.register(SportRecord)
