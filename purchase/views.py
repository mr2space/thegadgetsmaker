from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from courses.models import Course
from django.contrib.auth.models import User

from home.templatetags import url
from .email import PurchaseEmailThread
from .models import PaymentInfo, FailedPayment
from django.conf import settings
import stripe



#TODO: ADD USER RESTRICTIONS
stripe.api_key = settings.STRIPE_SECRET_KEY
ADMIN_EMAIL = "princegoswami.space@gmail.com"





@login_required(login_url="/auth/")
def index(request, courseId):
    details = {
        "method":"",
        "upi":False,
        "course":""
    }
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
        PurchaseEmailThread(username=request.user, course=course.title, method="online", upi=False).start()
        PurchaseEmailThread(username=request.user, course=course.title, method="online", upi=False,
                            email=request.user.email).start()
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
    param = url.setPara(request, "")
    param["courseId"] = courseId
    if request.method != "POST":
        return render(request, "purchase/upi.html", param)
    if not request.FILES['upi_img']:
        return render(request, "purchase/upi.html",param)
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
    # details = {"method": "upi", "upi": True, "course": course.title, "username":request.user}
    # sendEmail(request.user, details=details)
    PurchaseEmailThread(username=request.user, course=course.title, method="upi", upi=True).start()
    PurchaseEmailThread(username=request.user,course=course.title,method="upi",upi=True,email=request.user.email).start()
    # sendEmail(request.user, details=details, email=request.user.email, temp="email/payment_info_user.html")
    #TODO:upi waiting page
    return render(request, "purchase/upi_wait.html", param)


@login_required(login_url="/auth/")
def payment_success(request):
    param = url.setPara(request, "")
    #TODO: paymenr success page
    return HttpResponse("payment success")


@login_required(login_url="/auth/")
def payment_failed(request):
    param = url.setPara(request, "")
    #TODO: payment failed page
    return HttpResponse("payment failed")


def updateThePayment(session):
    purchase_id = session["metadata"]["purchase_id"]
    course_id = session["metadata"]["course_id"]
    user_id = session["metadata"]["user_id"]
    post_payment_id = session["payment_intent"]
    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
    except Exception as error:
        return 0
    try:
        print("in try")
        payment = PaymentInfo.objects.get(id=purchase_id)
        payment.payment_id=post_payment_id
        payment.payment_completed=True
        payment.save()
        details = {"method": "upi", "upi": True, "course": course.title, "username": user.username}
        # sendEmail({"user":user.username}, details=details)
        # print(user.email)
        # sendEmail({"user":user.username}, details=details, email=user.email, temp="email/payment_info_user_online.html")
        #TODO : SEND EMAIL page  FIX
        #TODO: COURSE PURCHASE PAGE
        return 1
    except Exception as error:
        print("bad value happen", post_payment_id,error)
        print("go to stripe for payment refund")
        failp = FailedPayment(
            user=user_id,
            course=course_id,
            payment_id=post_payment_id,
        )
        failp.save()
        return 0


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
        if updateThePayment(session):
            return HttpResponse(status=200)

    return  HttpResponse(status=500)

