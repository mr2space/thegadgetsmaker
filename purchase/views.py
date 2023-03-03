from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course
from django.contrib.auth.models import User
from .models import PaymentInfo,FailedPayment
from django.conf import settings
import stripe



#TODO: ADD USER RESTRICTIONS
stripe.api_key = settings.STRIPE_SECRET_KEY
ADMIN_EMAIL = "princegoswami.space@gmail.com"


def sendEmail(request,details:dict, email="princegoswami.space@gmail.com", temp="email/payment_info_admin.html" ):
    #TODO: set setting.admin_email
    #TODO: chnage email subject
    html = get_template(temp)
    param = {'username': request.user, 'payment_method':details["method"], "upi":details["upi"], "course":details["course"]}
    html_content = html.render(param)
    subject = f"New Payment for {details['course']}" if email == "princegoswami.space@gmail.com" else f"Thanks for your Purchase"
    from_email = settings.EMAIL_HOST_USER
    to = email
    try:
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        print("Error in sending the email")
        return -1
    return 0


@login_required(login_url="/auth/")
def index(request, courseId):
    details = {
        "method":"",
        "upi":False,
        "course":""
    }
    print(courseId)
    purchase_id = 0
    try:
        user = User.objects.get(id=request.user.id)
        course = Course.objects.get(id=courseId)
    except:
        print("model not import")
        return HttpResponse("failed")
    try:
        is_purchased = PaymentInfo.objects.get(course=course, user=user)
        purchase_id = is_purchased.id
    except Exception as error:
        upi = True
        print("error ", error)
        purchase = PaymentInfo(
            course=course,
            user=user,
            price=course.price,
            method="online",
            payment_id="default",
            payment_completed = False,
        )
        purchase.save()
        purchase_id = purchase.id
    else:
        if is_purchased.payment_completed:
            return HttpResponse("course already purchased")

        if request.FILES.get("upi_img", False):
            is_purchased.upi_img = request.FILESS["upi_img"]
            details["method"] = "upi"
            details["upi"] = True
            details["course"] = course.title
            sendEmail(request, details=details)
            return HttpResponse("wait for the verification")
        is_purchased.save()

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': int(course.price*100),
                    'product_data': {
                        'name': course.title,

                    },
                },
                'quantity': 1,
            },
        ],
        metadata={
            "purchase_id":purchase_id,
            "course_id": course.id,
            "user_id":user.id,
        },
        mode='payment',
        success_url='http://127.0.0.1:8000/payment/success',
        cancel_url='http://127.0.0.1:8000/payment/failed',
    )
    return redirect(checkout_session.url, code=303)


@login_required(login_url="/auth/")
def upiPayment(request, courseId):
    if request.method != "POST":
        return render(request, "purchase/upi.html",{'courseId':courseId})
    if not request.FILES['upi_img']:
        return render(request, "purchase/upi.html", {'courseId':courseId})
    try:
        user = User.objects.get(id=request.user.id)
        course = Course.objects.get(id=courseId)
    except:
        print("model not import")
        return HttpResponse("failed")
    try:
        is_purchased = PaymentInfo.objects.get(course=course, user=user)
    except Exception as error:
        upi = True
        print("error ", error)
        purchase = PaymentInfo(
            course=course,
            user=user,
            price=course.price,
            method="online",
            upi_img = request.FILES['upi_img'],
            payment_id="default",
            payment_completed=False,
        )
        purchase.save()

    else:
        if is_purchased.payment_completed:
            return HttpResponse("course already purchased")
        is_purchased = PaymentInfo.objects.get(course=course, user=user)
        is_purchased.upi_img = request.FILES['upi_img']
        is_purchased.save()
    details = {"method": "upi", "upi": True, "course": course.title, "username":request.user}
    sendEmail(request, details=details)
    sendEmail(request, details=details, email=request.user.email, temp="email/payment_info_user.html")
    return HttpResponse("wait for the verification")


@login_required(login_url="/auth/")
def payment_success(request):
    return HttpResponse("payment success")


@login_required(login_url="/auth/")
def payment_failed(request):
    return HttpResponse("payment failed")


def updateThePayment(session):
    purchase_id = session["metadata"]["purchase_id"]
    course_id = session["metadata"]["course_id"]
    user_id = session["metadata"]["user_id"]
    post_payment_id = session["payment_intent"]

    try:
        print("in try")
        payment = PaymentInfo.objects.get(id=purchase_id)
        payment.payment_id=post_payment_id
        payment.payment_completed=True
        payment.save()
        sendEmail(request,)
        return HttpResponse("course purchased")
    except Exception as error:
        print("bad value happen", post_payment_id,error)
        print("go to stripe for payment refund")
        failp = FailedPayment(
            user=user_id,
            course=course_id,
            payment_id=post_payment_id,
        )
        failp.save()
        return HttpResponse("payment failed")


@csrf_exempt
def stripeWebhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=401)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=402)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        updateThePayment(session)

    return HttpResponse(status=200)

