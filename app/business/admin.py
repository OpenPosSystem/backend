from django.contrib import admin

from business.models import Contract, Profile, Ticket, Incompatibility, Prerequisite

admin.site.register(Contract)
admin.site.register(Profile)
admin.site.register(Ticket)
admin.site.register(Incompatibility)
admin.site.register(Prerequisite)
