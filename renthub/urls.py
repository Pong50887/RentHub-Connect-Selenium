from django.urls import path

from . import views

app_name = 'renthub'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('<str:room_type>', views.RoomTypeView.as_view(), name='room_type'),
    path('rental/', views.RoomListView.as_view(), name='rental_list'),
    path("rental/<int:room_number>/", views.RoomDetailView.as_view(), name="rental"),
    path("payment/", views.RoomPaymentListView.as_view(), name="payment_list"),
    path("rental/<int:room_number>/payment/", views.RoomPaymentView.as_view(), name="payment"),
    path("rental/<int:room_number>/payment/submit/", views.submit_payment, name="submit"),
]
