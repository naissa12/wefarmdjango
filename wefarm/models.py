from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from wepay import WePay
from wepay.exceptions import WePayError
import settings
import logging
from decimal import *


class FarmerManager(models.Manager):

    def accessible(self):
        return self.exclude(wepay_access_token=None)


class Farmer(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    farm = models.CharField(max_length=255)
    produce = models.CharField(max_length=255)
    produce_price = models.DecimalField(
        default=0, max_digits=20, decimal_places=2)
    wepay_access_token = models.CharField(
        max_length=255, null=True)
    wepay_account_id = models.BigIntegerField(
        default=0, null=True)
    objects = FarmerManager()

    def create_account(self):
        """
        Create a WePay account to deposit any money for produce.
        """
        name = self.user.first_name + ' ' + self.user.last_name
        desc = name + ' account'
        production = settings.WEPAY['in_production']
        access_token = self.wepay_access_token

        wepay = WePay(production, access_token)

        try:
            create_response = wepay.call('/account/create',
                                         {'name': name, 'description': desc})
            self.wepay_account_id = create_response['account_id']
            self.save()

            return True, create_response
        except WePayError as e:
            return False, e

    @property
    def has_access_token(self):
        """
        Checks to see if this account have a wepay access token.
        i.e. Did they give us access to deposit money into their account.
        """
        if self.get_access_token():
            return True
        return False

    @property
    def has_account_id(self):
        """
        Checks to see if this account has a wepay account id.
        i.e. Did they give us access to deposit money into their account.
        """
        if self.get_account_id():
            return True
        return False

    def get_access_token(self):
        """
        Gets the access token
        """
        return self.wepay_access_token

    def get_account_id(self):
        """
        Returns wepay account id
        """
        return self.wepay_account_id

    def create_checkout(self, redirect_uri):
        """
        Performs WePay checkout/create API call request.
        Returns checkout_uri to create checkout form.
        """
        production = settings.WEPAY['in_production']
        access_token = self.wepay_access_token

        wepay = WePay(production, access_token)

        name = self.user.first_name + " " + self.user.last_name
        desc = "Purchasing " + self.produce + " from " + name
        price = str(self.produce_price)
        account_id = str(self.get_account_id())
        app_fee = str(Decimal('0.1') * self.produce_price)

        params = {
            'account_id': account_id,
            'short_description': desc,
            'type': 'GOODS',
            'app_fee': app_fee,
            'amount': price,
            'mode': 'iframe'
        }

        try:
            create_response = wepay.call('/checkout/create', params)

            checkout_uri = create_response['checkout_uri']

            return True, checkout_uri

        except WePayError as e:
            return False, e

    def save_account_id(self, account_id):
        """
        Saves wepay account id
        """
        self.wepay_account_id = account_id
        self.save()

    def save_access_token(self, access_token):
        """
        Saves wepay access token
        """
        self.wepay_access_token = access_token
        self.save()

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def create_checkout(self, redirect_uri):
          production = settings.WEPAY['in_production']
          access_token = self.wepay_access_token

          wepay = WePay(production, access_token)

          name = self.user.first_name + " " + self.user.last_name
          desc = "Purchasing " + self.produce + " from " + name
          price = str(self.produce_price)
          account_id = str(self.get_account_id())
          app_fee = str(Decimal('0.1') * self.produce_price)

          params = {
              'account_id': account_id,
              'short_description': desc,
              'type': 'GOODS',
              'app_fee': app_fee,
              'amount': price,
              'mode': 'iframe'
          }

          try:
              create_response = wepay.call('/checkout/create', params)

              checkout_uri = create_response['checkout_uri']

              return True, checkout_uri

          except WePayError as e:
              return False, e

def user_get_absolute_url(self):
    return "/farmers/%i/" % self.pk

User.get_absolute_url = user_get_absolute_url
