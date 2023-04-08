from django.urls import path
from . import views
urlpatterns = [
    path("course/<int:courseId>", views.index, name="purchase"),
    path("course/upi/<int:courseId>", views.upiPayment, name="upi"),
    path("code/<int:id>", views.codePurchase, name="purchase"),
    path("code/upi/<int:id>", views.fileUpiPayment, name="upi file"),
    path("course/success/<int:purchase_id>/<int:id>",views.course_payment_success),
    path("course/failed/<int:id>", views.course_payment_failed),
    path("code/success/<int:purchase_id>/<int:id>",views.code_payment_success),
    path("code/failed/<int:id>", views.code_payment_failed),
    path("webhook/", views.stripeWebhook),
]