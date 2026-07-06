from django.shortcuts import render , redirect
import os
from django.http import HttpResponse
from . services import Student
from django.core.files.storage import FileSystemStorage
###########LANDINGPAGE###########################
def landing_page(request):
    return render(request,'landing_page.html')


###########LANDINGPAGE###########################
def authentication(request):
    return render(request,'auth.html')
def signup(request):
    if request.method=="POST":
        full_name=request.POST.get("full_name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        role=request.POST.get("role")
        teacher_access_token=request.POST.get("Teacher_Access_Token")
        

        if role == "teacher":
         if teacher_access_token != os.getenv("TEACHER_ACCESS_CODE"):
          return HttpResponse("Invalid Teacher Access Code")
        obj=Student()
        data=obj.signup_user(full_name,email,phone,password,role)
        if data:
           return redirect("login")
        else:
           return redirect("signup")

def login_page(request):
    return render(request, "auth.html")

def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        obj = Student()
        data = obj.login_authentication(email, password)

        if data:

            request.session["authenticated"] = True
            request.session["user_id"] = data[0]

            first_name = data[1].split()[0]
            request.session["username"] = first_name

            role = data[4]
           

            request.session["role"] = role


            if role == "student":
                return redirect("student_dashboard")

            elif role == "teacher":
                return redirect("teacher_dashboard")

        else:
            return HttpResponse("Invalid Email or Password")

    return render(request, "auth.html")
###########STUDENT###########################
def student_dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")
    username = request.session.get("username")

    if not request.session.get("authenticated"):
        return redirect("authentication")

    if request.session.get("role") != "student":
        return HttpResponse("Access Denied")
    user_id = request.session.get("user_id")
    obj = Student()

    user = obj.get_user_profile(user_id)
    student = obj.get_student_profile(user_id)

    print(user)
    return render(request, 'student/student_dashboard.html' , {
        
            "user": user,
             "student": student

        })


######## edit profile student ########
def edit_student_page(request):

    user_id = request.session["user_id"]

    obj = Student()

    user = obj.get_user_profile(user_id)
    student = obj.get_student_profile(user_id)

    return render(
        request,
        "student/edit_profile_student.html",
        {
            "user": user,
            "student": student
        }
    )
def edit_information(request):

    if request.method == "POST":

        user_id = request.session["user_id"]

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        enrollment_no = request.POST.get("enrollment_no")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        section = request.POST.get("section")
        college_name = request.POST.get("college_name")
        joining_date = request.POST.get("joining_date")

        profile_image = request.FILES.get("profile_image")

        obj = Student()

        # Upload image
        if profile_image:

            fs = FileSystemStorage(
                location="media/profile_images"
            )

            filename = fs.save(
                profile_image.name,
                profile_image
            )

            image_path = "profile_images/" + filename

            obj.update_profile_image(
                user_id,
                image_path
            )

            print("IMAGE UPDATED:", image_path)

        # Students table
        obj.save_student_profile(
            user_id,
            enrollment_no,
            course,
            semester,
            section,
            college_name,
            joining_date
        )

        # Users table
        obj.update_user_profile(
            user_id,
            full_name,
            email,
            phone
        )

    return redirect("edit_student_page")

###########TEACHER###########################
def teacher_dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")


    if not request.session.get("authenticated"):
        return redirect("authentication")

    if request.session.get("role") != "teacher":
        return HttpResponse("Access Denied")
    
    return render(request, "teacher/teacher_dashboard.html")

###logout
def logout_user(request):

    request.session.pop("user_id", None)
    request.session.pop("role", None)

    return redirect("login")




def ai_result_page(request):
    return render (request,"student/ai_result.html")

def ai_evaluation(request):

    if request.method == "POST":

        uploaded_image = request.FILES.get("code_image")

        if not uploaded_image:
          return redirect("student_dashboard")

        fs = FileSystemStorage(
            location="media/homework"
        )

        filename = fs.save(
            uploaded_image.name,
            uploaded_image
        )

        full_path = fs.path(filename)

        print("FULL PATH =", full_path)
        obj = Student()

        result = obj.evaluate_code_image(full_path)

        user_id = request.session["user_id"]

        user = obj.get_user_profile(user_id)
        student = obj.get_student_profile(user_id)

        return render(
    request,
    "student/student_dashboard.html",
    {
        "user": user,
        "student": student,
        "result": result
    }
)

      