from django.contrib import admin
from .models import PaymentInfo, FailedPayment, FilePaymentInfo, FileFailedPayment


admin.site.register(PaymentInfo)
admin.site.register(FailedPayment)

admin.site.register(FilePaymentInfo)
admin.site.register(FileFailedPayment)