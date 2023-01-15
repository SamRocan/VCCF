from django.contrib import admin
from main.models import Company, Founder, TwitterInfo,Favourite

# Register your models here.
admin.site.register(Company)
admin.site.register(Founder)
admin.site.register(TwitterInfo)
admin.site.register(Favourite)