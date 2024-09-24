from django.contrib import admin
from .models import Category, Location, Company, Job, Application,Contact
# Register your models here.
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Contact)
