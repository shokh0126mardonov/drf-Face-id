from django.contrib import admin

from .models import CustomUser, Rules, Student, Payment, Tracking

admin.site.register([CustomUser, Rules, Student, Payment, Tracking])
