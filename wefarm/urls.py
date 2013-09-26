from django.conf.urls import patterns, include, url
from registration.backends.simple.views import RegistrationView
from forms import CustomRegistrationForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wefarm import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', views.index, name='home'),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^edit/$', views.edit, name="edit"),

                       url(r'^authorize/$', views.authorize, name='authorize'),

                       url(r'^farmers/buy/(?P<pk>\d+)/$',
                           views.buy, name='buy'),

                       url(r'^farmers/(?P<pk>\d+)/$',
                           views.profile, name='profile'),

                       url(r'^register/$', RegistrationView.as_view(
                           form_class=CustomRegistrationForm),
                           name='registration_register'),

                       url(r'^', include(
                           'registration.backends.simple.urls')),
                       )


urlpatterns += staticfiles_urlpatterns()
