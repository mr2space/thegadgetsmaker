from django.urls import path
from . import views
urlpatterns = [
    path("<int:courseId>", views.index, name="purchase"),
    path("upi/<int:courseId>", views.upiPayment, name="upi"),
    path("success/",views.payment_success),
    path("failed/", views.payment_failed),
    path("webhook/", views.stripeWebhook)
]