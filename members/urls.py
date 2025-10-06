# members/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard, Profile, Member List
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('list/', views.member_list, name='member_list'),
    path('detail/<int:pk>/', views.member_detail, name='member_detail'),
    path('announcements/', views.announcement_list, name='announcements'),
    
    # Registration
    path('register/', views.register_member, name='register_member'),

    # Authentication (Login, Logout, Password Change/Reset)
    path('login/', auth_views.LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='members/logged_out.html'), name='logout'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='members/password_change_form.html', success_url='/members/password_change/done/'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='members/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='members/password_reset_form.html', success_url='/members/password_reset/done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='members/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='members/password_reset_confirm.html', success_url='/members/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='members/password_reset_complete.html'), name='password_reset_complete'),
    path('list/', views.member_list, name='member_list'),
    path('export/csv/', views.export_members_csv, name='export_members_csv'), # <- ይህንን ጨምር
    path('detail/<int:pk>/', views.member_detail, name='member_detail'),
    path('detail/<int:pk>/', views.member_detail, name='member_detail'),
    path('id_card/<int:pk>/', views.member_id_card, name='member_id_card'),
]