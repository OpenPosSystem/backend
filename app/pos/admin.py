from django.contrib import admin

from pos.models import CardContent, Card, User


# Register your models here.


admin.site.register(User)
admin.site.register(Card)
admin.site.register(CardContent)
