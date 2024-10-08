from django.urls import path

from . import views

app_name = 'renthub'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="rental"),
    path("<int:pk>/payment", views.RoomPaymentView.as_view(), name="payment"),
    path("<int:room_id>/payment/submit", views.submit_payment, name="submit"),

]