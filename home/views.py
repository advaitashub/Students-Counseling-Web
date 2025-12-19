from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentDetailForm,UserRegistrationForm
from .models import CustomUser, AdminProfile, StudentDetail
# ,RegisteredStudent
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .forms import MassAllotmentForm
from django.urls import reverse
from django.db.models import F
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa






def assign_ranks():
    students = StudentDetail.objects.filter(Percentage_12__isnull=False).order_by('-Percentage_12')
    rank = 1
    for student in students:
        student.rank = rank
        student.save(update_fields=['rank'])
        rank += 1

def mark_fees_paid(request, student_id):
    if request.method == "POST":  # ✅ security check
        student = get_object_or_404(StudentDetail, id=student_id)
        student.fee_paid = "YES"
        student.save()
        messages.success(request, f"Fees marked as paid for {student.user.username}")
        return redirect(reverse("admin_student_panel")) 
    else:
        return redirect("admin_student_panel")



# Create your views here.
def index(request):
    return render(request,'index.html')
def login_page(request):
    return render(request, 'student_login.html')

def student_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user')  # reads input name="username"
        password = request.POST.get('password')  # reads input name="password"

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'is_student') and user.is_student:
                login(request, user)
                return redirect('student_dashboard')  # redirect to dashboard
            else:
                messages.error(request, "This is not a student account.")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'student_login.html')

@login_required
def student_dashboard(request):
    try:
        student=StudentDetail.objects.get(user=request.user)
        
    except StudentDetail.DoesNotExist:
        student=None
    student_data=[]
    if student:
        for field in StudentDetail._meta.fields:
            if field.name not in ['user','rank']:
                if field.choices:
                    # Use get_FOO_display() for fields with choices
                    value = getattr(student, f"get_{field.name}_display")()
                else:
                    value = getattr(student, field.name)

                student_data.append((field.verbose_name.replace('_', ' ').title(), value))

    return render(request, 'student_dashboard.html',
                  {
                      'student_data': dict(student_data),
                      'student': student
                  })

@login_required
def student_form_view(request):
    if request.method == 'POST':
        form = StudentDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # create this route
    else:
        form = StudentDetailForm()
    return render(request, 'home/student_login.html', {'form': form})


@login_required
def form_submit(request):
    try:
        existing_entry=StudentDetail.objects.get(user=request.user)
        messages.success(request, "Form already submitted successfully! Changes can't be made")
        return redirect('student_dashboard')
    except StudentDetail.DoesNotExist:
        existing_entry = None
    if request.method == 'POST':
        form = StudentDetailForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user  # link form to logged-in user
            student.save()
            assign_ranks()
            # messages.success(request, "Form submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = StudentDetailForm(instance=existing_entry)
    return render(request, 'form.html', {'form': form})


# views.py
@login_required
def upload_fee_receipt(request):
    student = request.user.studentdetail  # assuming OneToOne relation with User
    if request.method == "POST" and request.FILES.get("receipt"):
        student.fee_receipt = request.FILES["receipt"]
        student.save()
        messages.success(request, "Fee receipt uploaded successfully!")
    return redirect("student_dashboard")  # change to your student dashboard name

@login_required
def accept_seat(request):
    student = request.user.studentdetail
    student.is_allotted = "YES"   # mark seat as accepted
    student.save(update_fields=["is_allotted"])
    messages.success(request, "Seat accepted successfully. Please upload your fee receipt.")
    return redirect("upload_fee_receipt")


@login_required
def generate_offer_letter(request):
    student = request.user.studentdetail
    if student.fee_paid != "YES":
        return HttpResponse("Payment not verified yet.")

    html = render_to_string("offer_letter.html", {"student": student})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response



def student_signup_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        #CHECK IF PASSWORDS MATCHES
        if password != confirm_password:
         messages.error(request, "Passwords do not match")
         return render(request,'student_signup.html',{"form":form})
         # CHECK PASSWORD LENGTH
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return render(request, 'student_signup.html', {"form": form})
        if form.is_valid():
            # Create user
            user = form.save(commit=False)  # Don't save yet
            user.is_student = True           # ✅ Mark this user as a student
            user.password = make_password(password)  # ✅ Hash the password
            user.save()                      # Now save to DB 


            messages.success(request, "Account created successfully. Please log in.")
            return redirect('student_login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'student_signup.html', {'form': form})



def admin_panel(request):
    search_query = request.GET.get('search', '')
    branch_filter = request.GET.get('branch', '')
    
    students = StudentDetail.objects.all().order_by('-rank')
    
    if search_query:
        students = students.filter(name__icontains=search_query)  # adjust field names
    if branch_filter:
        students = students.filter(allotted_branch=branch_filter)
    
    return render(request, 'admin-temp/admin_dashboard.html', {
        'students': students
    })


def allot_branch_by_name_or_percentage(request):
    if request.method == "POST":
        name = request.POST.get("student_name")
        min_percentage = request.POST.get("min_percentage")
        max_percentage = request.POST.get("max_percentage")
        branch_to_allot = request.POST.get("branch_to_allot")

        if not branch_to_allot:
            messages.error(request, "Please select a branch to allot.")
            return redirect("mass_allocation")  # or your page URL

        students = StudentDetail.objects.all()

        # Filter by name if provided
        if name:
            students = students.filter(name__icontains=name)

        # Filter by percentage if provided
        if min_percentage and max_percentage:
            students = students.filter(percentage_12__gte=min_percentage, percentage_12__lte=max_percentage)

        if students.exists():
            students.update(allotted_branch=branch_to_allot)
            messages.success(request, f"Branch '{branch_to_allot}' allotted successfully.")
        else:
            messages.warning(request, "No students found for the given criteria.")

        return redirect("mass_allocation")

    return redirect("mass_allocation")


def mass_allocation(request):
    students = StudentDetail.objects.all().order_by('-Percentage_12')  # always defined

    if request.method == "POST":
        form = MassAllotmentForm(request.POST)
        if form.is_valid():
            min_percentage = form.cleaned_data['min_percentage']
            max_percentage = form.cleaned_data['max_percentage']
            branch = form.cleaned_data['branch_to_allot']

            # Get eligible students
            eligible_students = StudentDetail.objects.filter(
                Percentage_12__gte=min_percentage,
                Percentage_12__lte=max_percentage,
                is_allotted__in=['', 'NO', 'COMMING']  # only students not yet fully allotted
            )
            count = eligible_students.count()

            if count == 0:
                messages.info(request, "No students meet the criteria or all have been allotted.")
            else:
                # Update all eligible students
                for student in eligible_students:
                    student.allotted_branch = branch
                    student.save()
                messages.success(request, f"Successfully allotted branch '{branch}' to {count} students.")

            return redirect('mass_allocation')  # prevent resubmission

    else:
        form = MassAllotmentForm()

    context = {
        'form': form,
        'students': students,
    }
    return render(request, 'admin-temp/mass_allocation.html', context)


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Superuser allowed
            if user.is_superuser:
                login(request, user)
                return redirect("admin_student_panel")  # goes to custom dashboard
            # Ensure user is admin and approved
            if not user.is_student and hasattr(user, 'admin_profile') and user.admin_profile.approved:
                login(request, user)
                return redirect("admin_student_panel")  # ✅ custom admin dashboard
            else:
                messages.error(request, "You are not approved to access the admin dashboard.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin-temp/admin_login.html')





def admin_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "admin-temp/admin_signup.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "admin-temp/admin_signup.html")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_student=False,
            is_staff=True   # ✅ Required for admin access
        )

        # Create AdminProfile with pending approval
        AdminProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=email,
            approved=False
        )

        messages.success(request, "Signup successful! Your request is pending approval from superadmin.")
        return redirect("admin_login")

    return render(request, "admin-temp/admin_signup.html")









def logout(request):
   return render(request,'index.html')
def aboutus(request):
   return render(request,'aboutus.html')
def FAQs(request):
   return render(request,'FAQs.html')
# def logout(request):
#    return render(request,'index.html')



