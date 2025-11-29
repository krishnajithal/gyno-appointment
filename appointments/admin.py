from django.contrib import admin

from .models import Appointment

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):

    list_display = ('patient','doctor', 'date', 'time', 'reason')

    list_filter = ('status', 'date')

    search_fields = ('patient__username','doctor__username', 'reason')

admin.site.register(Appointment, AppointmentAdmin)    