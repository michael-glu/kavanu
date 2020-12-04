from django.contrib import admin

from .models import Event

#user-name: michael
#email: glusteinm@gmail.com
#password: password

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'datetime', 'location')

admin.site.register(Event, EventAdmin)
# admin.site.register(User)
