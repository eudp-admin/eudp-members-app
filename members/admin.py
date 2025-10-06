# members/admin.py

from django.contrib import admin
from .models import Member, Meeting, Attendance, Announcement

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # በአዲሶቹ መስኮች እናስተካክለው
    list_display = ('membership_id', 'full_name', 'phone_number', 'email', 'region', 'city', 'membership_level')
    search_fields = ('full_name', 'phone_number', 'membership_id', 'city', 'zone', 'woreda')
    list_filter = ('region', 'gender', 'education_level', 'membership_level', 'is_active')
    list_per_page = 20

admin.site.register(Meeting)
admin.site.register(Attendance)
admin.site.register(Announcement)