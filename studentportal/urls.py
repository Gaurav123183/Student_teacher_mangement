"""
URL configuration for studentportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing_page,name='landing_page'),
    path('student_dashboard/',views.student_dashboard,name="student_dashboard"),
    path('teacher_dashboard/',views.teacher_dashboard,name="teacher_dashboard"),
    path('authentication/',views.authentication),
    path('signup/',views.signup,name="signup"),
    path('login_page/',views.login_page,name="login_page"),
    path('login/',views.login,name="login"),
    path('edit_student_page/',views.edit_student_page,name="edit_student_page"),
    path('edit_information/',views.edit_information,name="edit_information"),
    path("logout/", views.logout_user, name="logout"),
    path('ai_result_page/',views.ai_result_page),
    path('ai_evaluation/',views.ai_evaluation,name="ai_evaluation"),


]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)