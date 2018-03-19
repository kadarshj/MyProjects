#from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Events
#import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.urls import reverse
import uuid
from .models import BookDetails, Events
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Sum
from datetime import datetime


# Create your views here.
def home(request):
    #artsharelist = Artistshare.objects.all()
    today = datetime.now()
    eventlist = Events.objects.order_by('-date')
    return render(request,"events/share_events.html",{'eventlist': eventlist, 'today':today})


def book(request):
    total_seats = request.POST.get('total_seats')
    price = request.POST.get('price')
    events_id = request.POST.get('events_id')
    booked_seats = request.POST.get('booked_seats')
    return render(request, "events/book.html",{'total_seats': total_seats, 'price': price, 'events_id': events_id, 'booked_seats': booked_seats})

def booked(request):
    amount = request.POST.get('price')
    booked_seats = request.POST.get('booked_seats')
    seat_count = request.POST.get('seat_count')
    events_id = request.POST.get('events_id')
    firstname = request.POST.get('firstname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')


    MERCHANT_KEY = "gtKFFx"
    key = "gtKFFx"
    SALT = "eCwWELxi"
    PAYU_BASE_URL = "https://test.payu.in/_payment"
    action = ''
    posted = {}
    for i in request.POST:
        posted[i] = request.POST[i]
    # hash_object = hashlib.sha256(b'randint(0,20)')
    # txnid = hash_object.hexdigest()[0:20]
    txnid = str(uuid.uuid1().int >> 64)
    hashh = ''
    posted['txnid'] = txnid
    BookDetails.objects.create(name= firstname,phone= phone,email= email, event_id=events_id, amount=amount, booked_seats = booked_seats, count = seat_count, txnid = txnid)

    event_obj = get_object_or_404(Events, pk=events_id)
    # event_obj.left_seats = int(event_obj.total_seats) - int(seat_count)
    if (event_obj.booked_seats == ''):
        event_obj.booked_seats = booked_seats
    else:
        event_obj.booked_seats = event_obj.booked_seats + ',' + booked_seats
    event_obj.is_booked = True
    bookobj = BookDetails.objects.filter(event_id=events_id).aggregate(Sum('count'))['count__sum']
    event_obj.left_seats = event_obj.total_seats - bookobj
    event_obj.save()

    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    #posted['surl'] = request.build_absolute_uri(reverse("success"))
    #posted['furl'] = request.build_absolute_uri(reverse("failure"))
    posted['surl'] = request.build_absolute_uri(reverse("success"))
    posted['furl'] = request.build_absolute_uri(reverse("failure"))
    posted['amount'] = amount
    posted['productinfo'] = 'NoProductInfo'
    posted['firstname'] = firstname
    posted['email'] = email
    posted['phone'] = phone
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    action = PAYU_BASE_URL
    if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
            "firstname") != None and posted.get("email") != None):
        return render(request, 'events/booked.html',
                      {"posted": posted, "hashh": hashh, "MERCHANT_KEY": MERCHANT_KEY, "txnid": txnid,
                       "hash_string": hash_string, "action": "https://test.payu.in/_payment"})
    else:
        return render(request, 'events/booked.html',
                      {"posted": posted, "hashh": hashh, "MERCHANT_KEY": MERCHANT_KEY, "txnid": txnid,
                       "hash_string": hash_string, "action": "."})




@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    phone = request.POST["phone"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "eCwWELxi"

    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render(request, 'events/success.html', {"txnid": txnid, "status": status, "amount": amount})






@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    phone = request.POST["phone"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "eCwWELxi"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render(request, "events/failure.html", c)