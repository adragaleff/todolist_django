from django.urls import path, include
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home_view, name='home'),
    path('task/<int:id>', views.view_task, name='task'),
    path('edittask/<int:id>', views.edittask_view, name='edittask'),
    path('archtask/<int:id>', views.archive_task, name='archivetask'),
    path('addtask/', addtask_view),
    path('delete/<int:id>', views.delete_task, name='deletetask'),
    path('deletecomment/<int:id>', views.delete_comment, name='deletecomment'),

    path('login/', LoginUser.as_view(), name='login'),
    path('profile/<int:pk>', views.profile_view, name='profile'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

]