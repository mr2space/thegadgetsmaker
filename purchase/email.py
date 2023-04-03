from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
import threading

ADMIN_EMAIL = "princegoswami.space@gmail.com"


class PurchaseEmailThread(threading.Thread):
    def __init__(self, username, course, method, upi, email=ADMIN_EMAIL):
        self.username = username
        self.method = method
        self.upi = upi
        self.email = email
        self.course = course
        threading.Thread.__init__(self)

    def run(self):
        temp = "email/payment_info_user_online.html"
        if self.email == ADMIN_EMAIL:
            temp = "email/payment_info_admin.html"
        elif self.method == "upi":
            temp = "email/payment_info_user.html"
        try:
            html = get_template(temp)
            param = {'username': self.username, 'payment_method': self.method, "upi": self.upi,
                     "course": self.course}
            html_content = html.render(param)
            subject = f"New Payment for {self.course}" if self.email == ADMIN_EMAIL else f"Thanks for your Purchase"
            from_email = ADMIN_EMAIL
            to = self.email
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            print("Sending mail")
            msg.send()
        except Exception as error:
            print("Error in sending the email", error)
            return -1
        return 0
