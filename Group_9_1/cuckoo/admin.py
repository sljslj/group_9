from django.contrib import admin
from . import models

# admin.site.register(models.User)
admin.site.register(models.Favorite)
admin.site.register(models.SearchInput)
admin.site.register(models.SearchResult)
admin.site.register(models.History)
admin.site.register(models.EmailVerifyRecord)