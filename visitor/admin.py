from django.contrib import admin
from .models import Child, Teacher, Attendance

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'teacher', 'parent_email')
    list_filter = ('class_name', 'teacher')
    search_fields = ('name', 'parent_email')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'email')
    list_filter = ('class_name',)
    search_fields = ('name', 'email')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('parent_name', 'child', 'check_in_time', 'check_out_time', 'is_checked_in', 'duration')
    list_filter = ('child__class_name', 'is_checked_in', 'check_in_time')
    search_fields = ('parent_name', 'child__name')
    readonly_fields = ('duration',)

    def duration(self, obj):
        if obj.check_out_time:
            return obj.check_out_time - obj.check_in_time
        return None
    duration.short_description = 'Duration'
