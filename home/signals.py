# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from .models import RegisteredStudent, StudentDetail

# User = settings.AUTH_USER_MODEL  # 'home.CustomUser'

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_student_profile(sender, instance, created, **kwargs):
#     if created:
#         # Create RegisteredStudent
#         RegisteredStudent.objects.create(
#             user=instance,
#             email=instance.email
#         )
#         # Create StudentDetail
#         StudentDetail.objects.create(user=instance, email=instance.email)
