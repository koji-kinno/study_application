from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'hello'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('edit/<int:num>', views.edit, name='edit'),    
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('delete/<int:num>', views.delete, name='delete'),
    path('find/', views.find, name='find'),
    path('plot/', views.get_svg, name='plot'),
    path('all_year/', views.all_year, name='all_year'),
    path('all_users/', views.all_users, name='all_users'),
    path('year_plot/', views.get_bar_svg, name='year_plot'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="hello/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="hello:index"), name='logout'),
]