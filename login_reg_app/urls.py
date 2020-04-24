from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_login),
    path('register_user',views.register_user),
    path('success', views.render_success),
    path('log_In', views.user_login),
    path('logout', views.logout)

]