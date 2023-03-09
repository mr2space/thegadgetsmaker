from django.contrib import admin
from .models import PaymentInfo, FailedPayment


admin.site.register(PaymentInfo)
admin.site.register(FailedPayment)