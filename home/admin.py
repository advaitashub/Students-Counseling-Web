from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import StudentDetail, AdminProfile


Students = get_user_model()

# --- Default Django admin (for superuser only) ---
admin.site.site_title = "Superuser Admin Portal"
admin.site.site_header = "Superuser Admin Panel"
admin.site.index_title = "Manage Admin Approvals"


# --- Custom User Admin ---
class StudentDetailInline(admin.StackedInline):
    model = StudentDetail
    can_delete = False
    verbose_name_plural = 'Student Details'
    extra = 0


exclude_fields = ('password', 'id', 'first_name', 'last_name', 'last_login', 'is_superuser')
user_fields = [f.name for f in Students._meta.fields if f.name not in exclude_fields]
student_fields = [f.name for f in StudentDetail._meta.fields if f.name not in ('id',)]


class CustomUserAdmin(BaseUserAdmin):
    inlines = (StudentDetailInline,)
    list_display = user_fields + student_fields
    search_fields = ('username', 'name', 'email', 'course_opted')
    list_filter = ('is_active', 'is_staff')


def make_getter(field_name):
    def getter(self, obj):
        return getattr(obj.studentdetail, field_name, None)
    getter.short_description = field_name.replace('_', ' ').title()
    return getter


for field in student_fields:
    setattr(CustomUserAdmin, field, make_getter(field))


# --- Custom Admin Site (for approved staff only) ---
class CustomAdminSite(AdminSite):
    site_header = 'Student Counseling Admin Panel'
    site_title = 'Counseling Admin'
    index_title = 'Dashboard'

    def has_permission(self, request):
        # Superuser should NOT land here, only staff with approved profile
        return (
            request.user.is_active
            and request.user.is_staff
            and hasattr(request.user, "adminprofile")
            and request.user.adminprofile.approved
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.admin_view(self.dashboard)),
            path('mass_allocation/', self.admin_view(self.mass_allocation)),
            path('mark_fees/', self.admin_view(self.mark_fees)),
        ]
        return my_urls + urls

    def dashboard(self, request):
        total_students = Students.objects.filter(is_student=True).count()
        allotted = StudentDetail.objects.filter(is_allotted="YES").count()
        not_allotted = StudentDetail.objects.filter(is_allotted="NO").count()
        students = StudentDetail.objects.all()

        return TemplateResponse(request, "admin/admin_dashboard.html", {
            "total_students": total_students,
            "allotted": allotted,
            "not_allotted": not_allotted,
            "students": students
        })

    def mass_allocation(self, request):
        StudentDetail.objects.filter(is_allotted="NO").update(is_allotted="YES")
        self.message_user(request, "Mass allocation completed successfully.")
        return redirect("admin:index")

    def mark_fees(self, request):
        ids = request.POST.getlist("student_ids")
        StudentDetail.objects.filter(id__in=ids).update(fee_paid="YES")
        self.message_user(request, "Selected students marked as fees paid.")
        return redirect("admin:index")


# Register models in custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Students, CustomUserAdmin)
custom_admin_site.register(StudentDetail)
custom_admin_site.register(AdminProfile)


# --- Default superuser admin site ---
@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'email', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__username', 'name', 'email')




admin.site.register(StudentDetail)




