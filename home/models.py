from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)

    # models.py
class RegisteredStudent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True,blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True)
    # add other fields if needed

    def __str__(self):
        return self.user.username



class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")
    email = models.EmailField(unique=True,blank=True, null=True)
    name = models.CharField(max_length=150,blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)
    approved = models.BooleanField(default=False)  # superuser can approve
    created_at = models.DateTimeField(auto_now_add=True)
     


    def __str__(self):
        return self.user.username   
    
class StudentDetail(models.Model):
    COURSE_CHOISE=[
        ('','NOT CHOSEN'),
        ('MCA','MCA'),
        ('BCA','BCA'),
        ('B-TECH','B-TECH'),
    ]
    ALLOTTED_BRANCH= [
                        ('', 'Waiting'),
                        ('CSE', 'Computer Science'),
                        ('ECE', 'Electronics'),
                        ('ME', 'Mechanical'),
                        ('CE', 'Civil'),
                      ]
    # OFFER_LETTER_GENERATED= [
    #                     ('', 'Waiting'),
    #                     ('NO','NO'),
    #                     ('YES','YES'),
    #                     ('COMMING','COMMING'),
    #                   ]
    FEE_PAID=[('','Waiting'),
                ('NO','NO'),
                ('YES','YES'),
                ('COMMING','COMMING'),]
    
    IS_ALLOTTED=[('','Waiting'),
                ('NO','NO'),
                ('YES','YES'),
                ('COMMING','COMMING'),

    ]

    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)

    # Personal Info
    #name = models.CharField(max_length=100)
    name = models.CharField(max_length=150,blank=True, null=True)
    phone = models.CharField(max_length=15,blank=True, null=True)
    email = models.EmailField(unique=True,blank=True, null=True)
    father_name=models.CharField(max_length=100)
    mother_name=models.CharField(max_length=100)
    #email = models.EmailField(unique=True)

    adhar_no=models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField()

    # High School Marks
    math_10 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    science_10 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    english_10 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    hindi_10 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    Percentage_10 = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
                                   default=0.0)

    # 10+2 Marks
    physics_12 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    chemistry_12 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    math_12 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    Percentage_12 = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
                                   default=0.0)

    # Preferences and Allotment
    course_opted = models.CharField(
        max_length=50,
        choices=COURSE_CHOISE,
        blank=True,
        default='',
        verbose_name="Course Opted"
    )
    branch_1 = models.CharField(max_length=50)
    branch_2 = models.CharField(max_length=50)

    fee_receipt = models.ImageField(
        upload_to="fee_receipts/",   # folder inside MEDIA_ROOT
        blank=True,
        null=True,
        verbose_name="Fee Receipt"
    )

    #Admin purpose

    rank = models.PositiveIntegerField(null=True, blank=True)

    is_allotted = models.CharField(
        max_length=50,
        choices=IS_ALLOTTED,
        blank=True,
        default='',
        verbose_name="Is Allotted"
    )
    allotted_branch = models.CharField(
        max_length=50,
        choices=ALLOTTED_BRANCH,
        blank=True,
        default='',
        verbose_name="Allotted Branch"
    )
    # Payment and Offer
    fee_paid = models.CharField(max_length=50,
        choices=FEE_PAID,
        blank=True,
        default='',
        verbose_name="Fee Paid"
    )
    # offer_letter_generated = models.CharField(
    #     max_length=50,
    #     choices=OFFER_LETTER_GENERATED,
    #     blank=True,
    #     default='',
    #     verbose_name="Offer Letter Generated"
    # )
     

    def __str__(self):
        return self.user.username



