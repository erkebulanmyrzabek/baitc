from django.contrib import admin
from .models import Hackathon, News, Webinar, CaseCup
# Register your models here.
admin.site.register(Hackathon)
admin.site.register(News)
admin.site.register(Webinar)
admin.site.register(CaseCup)
