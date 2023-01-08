from django.contrib import admin
from main.models import Company, Founder, TwitterInfo

# Register your models here.
admin.site.register(Company)
admin.site.register(Founder)
admin.site.register(TwitterInfo)