from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

from cms.apps.checkout.classes import CheckoutOffer, CheckoutSummary
from cms.apps.checkout.models import Purchase
from cms.apps.checkout.services import process_purchase, send_purchase_mail
from cms.apps.travel.models import Travel


@login_required(login_url='/login/')
def add(request):
    data = request.POST
    count = int(data.get('count') or 1)
    ref = data.get('ref') or None
    offer = CheckoutOffer(data.get('travel-id'), count, ref)
    existing = request.session.get('offers', [])

    for exist in existing:
        if offer.offer_id == exist.offer_id:
            return render(request, 'checkout/offer_exists.html')

    travel = get_object_or_404(Travel, pk=data.get('travel-id'), active=True)
    places_taken = Purchase.objects.filter(travel=travel).aggregate(Sum('passengers'))
    places_left = travel.passengers_limit - (places_taken['passengers__sum'] or 0)

    if count > places_left:
        return render(request, 'checkout/places_taken.html')

    existing.append(offer)
    request.session['offers'] = existing
    return redirect('checkout:new')


@login_required(login_url='/login/')
def new(request):
    return render(request, 'checkout/new.html')


@login_required(login_url='/login/')
def summary(request):
    offers = request.session.get('offers')

    if not offers:
        return redirect('travel:index')

    checkout_summary = CheckoutSummary
    checkout_summary.offers = []

    total = 0
    total_discount = 0

    for checkout_offer in offers:
        count = int(checkout_offer.people)
        offer = Travel.objects.get(pk=checkout_offer.offer_id)

        discount_percent = offer.discount_per_person * count
        if discount_percent > offer.max_discount:
            discount_percent = offer.max_discount

        total += offer.price * count * (100 - discount_percent) / 100
        total_discount += offer.price * count * discount_percent / 100
        checkout_summary.offers.append({'offer': offer, 'people': count, 'total': offer.price * count})

    checkout_summary.total_price = total
    checkout_summary.total_discount = total_discount

    now = datetime.datetime.now()
    years = range(now.year, now.year + 10)
    months = range(1, 12)

    return render(request, 'checkout/summary.html', {'summary': checkout_summary, 'years': years, 'months': months})


@login_required(login_url='/login/')
def remove(request, offer_id):
    existing = request.session.get('offers', [])

    for exist in existing:
        if int(exist.offer_id) == offer_id:
            existing.remove(exist)
            Travel.objects.filter(id=offer_id).update(rejections=F('rejections')+1)

    request.session['offers'] = existing
    return redirect('checkout:summary')


@login_required(login_url='/login/')
def purchase(request):
    data = request.POST
    offers = request.session.get('offers')
    user = request.user

    result = process_purchase(offers, data, user)
    send_purchase_mail(user, offers)

    if result:
        del request.session['offers']
        request.session.modified = True
        return render(request, 'checkout/purchase_completed.html')

    return render(request, 'checkout/error.html')
