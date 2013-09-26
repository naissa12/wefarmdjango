from models import Farmer
from forms import FarmerForm, UserEditForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from wepay import WePay
import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from wepay.exceptions import WePayError
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404


# GET /
def index(request):
    items = Farmer.objects.all()
    context = {'farmer_list': items}
    return render(request, 'index.html', context)


# GET edit/
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    farmer = get_object_or_404(Farmer, user=user)

    production = settings.WEPAY['in_production']
    wepay = WePay(production)

    redirect_uri = settings.WEPAY['authorize_url']

    auth_url = None
    show_edit = False
    if farmer.user.pk == request.user.pk:
        show_edit = True

        if not farmer.has_access_token:
            auth_url = wepay.get_authorization_url(
                redirect_uri, settings.WEPAY['client_id'])

    context = {
        'farmer': farmer,
        'auth_url': auth_url,
        'show_edit': show_edit
    }

    return render(request, 'profile.html', context)


# GET /farmers/buy/1
def buy(request, pk):
    # get farmer
    farmer = get_object_or_404(Farmer, pk=pk)

    checkout = farmer.create_checkout(None)

    checkout_uri = None
    if checkout[0]:
        checkout_uri = checkout[1]

    context = {
        'farmer': farmer,
        'checkout_uri': checkout_uri
    }

    return render(request, 'buy.html', context)


# GET /authorize/
@login_required
def authorize(request):
    user = request.user
    farmer = get_object_or_404(Farmer, user=user)

    production = settings.WEPAY['in_production']
    wepay = WePay(production)

    redirect_uri = settings.WEPAY['authorize_url']

    try:
        if 'code' in request.GET:
            code = request.GET['code']

            token = wepay.get_token(
                redirect_uri,
                settings.WEPAY['client_id'],
                settings.WEPAY['client_secret'],
                code)

            if token:
                farmer.save_access_token(token['access_token'])
                created = farmer.create_account()

                if not created[0]:
                    return HttpResponse(
                        "WePay error on update. %s" % error, status=500)

            # redirect back to profile
            return HttpResponseRedirect(reverse('profile', args=[user.pk]))

        else:
            url = wepay.get_authorization_url(
                redirect_uri, settings.WEPAY['client_id'])

            # redirect to authorization url
            return redirect(url)

    except WePayError as error:
        return HttpResponse("WePay error on update. %s" % error, status=500)


# GET /edit/
@login_required
def edit(request):

    user = request.user
    f = get_object_or_404(Farmer, user=user)
    u = user

    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=f)
        uform = UserEditForm(request.POST, instance=u)

        if uform.is_valid() and form.is_valid():
            uform.save()
            form.save()

            return redirect(reverse('home'))
    else:
        form = FarmerForm(instance=f)
        uform = UserEditForm(instance=u)

    return render(request, 'registration/edit.html', {
        'form': form,
        'uform': uform
    })
