from django.contrib import admin
from django.urls import path,include,reverse_lazy
from home import views
from . import views
from .views import student_form_view, student_dashboard
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('', views.index,name="home"),
    path('accept-seat/', views.accept_seat, name='accept_seat'),
    path('generate_offer_letter/', views.generate_offer_letter, name='generate_offer_letter'),
    path('student_login/', views.login_page, name='student_login'),
    path(
        'registration/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/custom_password_reset_email.html',
            extra_email_context={
                'domain': settings.DOMAIN,
                'protocol': settings.PROTOCOL,
            }
        ),
        name='password_reset',
    ),
    path('registration/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('registration/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirml.html',
        success_url=reverse_lazy("password_reset_done")), name='password_reset_confirm'),
    path('registration/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('student_signup/', views.student_signup_page, name='student_signup'),
    path('student_form/',views.student_login_view, name='student_logedin'),
    path('form_submit/', views.form_submit, name='form_submit'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path("upload-receipt/", views.upload_fee_receipt, name="upload_fee_receipt"),
    path('admin-temp/admin_login/', views.admin_login, name='admin_login'),
    path('admin-temp/admin_signup/', views.admin_signup, name='admin_signup'),
    path('admin-temp/mass_allocation/', views.mass_allocation, name='mass_allocation'),
    path('allot_branch/', views.allot_branch_by_name_or_percentage, name='allot_branch'),
    path('admin-temp/mark_fees_paid/<int:student_id>/', views.mark_fees_paid, name='mark_fees_paid'),
    path('admin-temp/admin_student_panel/', views.admin_panel, name='admin_student_panel'),
    path('logout', views.logout,name="logout"),
    path('aboutus', views.logout,name="aboutus"),
    path('login', views.logout,name="login"),
    path('FAQs', views.logout,name="FAQs"),
    
 ]