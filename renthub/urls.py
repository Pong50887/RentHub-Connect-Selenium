from django.urls import path

from . import views

app_name = 'renthub'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('<str:room_type>/', views.RoomTypeView.as_view(), name='room_type'),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="rental"),
    path("<int:pk>/payment", views.RoomPaymentView.as_view(), name="payment"),
    path("<int:room_id>/payment/submit", views.submit_payment, name="submit"),

]
