"""
Definition of urls for DjangoWebProject.

"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm, BingAdsPasswordAuthenticationForm
from django.contrib.auth.views import HttpResponseRedirect

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^applogout', 'app.views.applogout', name='applogout'),
    url(r'^callback', 'app.views.callback', name='callback'),
    url(r'^viewcampaigns', 'app.views.viewcampaigns', name='viewcampaigns'),
    url(r'^revoke', 'app.views.revoke', name='revoke'),
    url(r'^$',
        'app.views.home',
        {
            'template_name': 'app/index.html',
            'authentication_form': BingAdsPasswordAuthenticationForm,
            'extra_context':
            {
                'title':'Home Page',
                'year':datetime.now().year,
            }
        },
        name='home'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
