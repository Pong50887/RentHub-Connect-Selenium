from django.urls import path

from . import views

app_name = 'renthub'

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:room_id>/", views.room, name="rental"),
    path("<int:room_id>/payment", views.room_payment, name="payment"),
    path("<int:room_id>/payment/submit", views.submit_payment, name="submit"),

]