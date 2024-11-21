from django.urls import path, re_path
from django.shortcuts import redirect

from . import views

app_name = 'renthub'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('room-type/<str:room_type>/', views.RoomTypeView.as_view(), name='room_type'),
    path('room/', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:room_number>/', views.RoomDetailView.as_view(), name='room'),
    path('payment/', views.RoomPaymentListView.as_view(), name='payment_list'),
    path('payment/history/<int:pk>/', views.RoomPaymentHistoryView.as_view(), name='payment_history'),
    path('room/<int:room_number>/payment/', views.RoomPaymentView.as_view(), name='payment'),
    path('announcement/<int:pk>/', views.AnnouncementView.as_view(), name='announcement'),
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('notifications/mark-read/', views.MarkNotificationsReadView.as_view(), name='mark_notifications_read'),
    path('room/<int:room_number>/payment/delete-qr-code/', views.DeleteQRCodeView.as_view(), name='delete_qr_code'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('overview/', views.RoomOverviewView.as_view(), name='room_overview'),
    path('profile/', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('user/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    re_path(r'^.*$', lambda request: redirect('renthub:home')),
]
