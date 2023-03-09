import random
from django.conf import settings
from user.models import ExtendUser
import math
import random
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


def otpGenerator() -> int:
    # variable to store digit use in Otp
    digits = '123456789'
    otp = ''
    for i in range(5):
        otp += str(math.floor(random.random() * 10))
    return int(otp)


def sendEmail(otp: int, username,user_email = None):
    html = get_template("email/otp.html")
    param = {'username': username, 'otp': otp}
    html_content = html.render(param)
    subject = f"Welcome {username} to our gadgets maker "
    from_email = settings.EMAIL_HOST_USER
    to = user_email
    try:
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        print("Error in sending the email")
        return -1
    return 0


def savingUserModel(request):
    name_list = request.POST.get('fullname').split()
    otp = otpGenerator()
    try:
        new_user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            first_name=name_list[0],
            last_name=name_list[1] if len(name_list) > 1 else '',
        )
        new_user.save()
    except Exception as error:
        print("some error occur in saving the user")
        print(error)
        return -1
    sendEmail(otp, username=request.user.username, email=request.user.email)
    try:
        print("here")
        new_extenduser = ExtendUser(
            username=User.objects.get(username=request.POST.get('username')),
            phone_number=request.POST.get("phone_number"),
            full_name=request.POST.get('fullname'),
            address=request.POST.get('address'),
            is_verified=False,
            otp=otp,
        )
        if request.FILES.get("profile", False):
            print("its done")
            new_extenduser.profile = request.FILES["profile"]
        new_extenduser.save()
    except Exception as error:
        print("some error occur in saving extend user")
        print(error, request.FILES)
        return -1
    return 0
