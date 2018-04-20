"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.template.loader import get_template, render_to_string
from DjangoWebProject import settings
from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User

from app.models import BingAdsUser
from app.forms import BingAdsPasswordAuthenticationForm

from bingads import *
from bingads.v12.bulk import *

import pickle

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)

authorization_data = AuthorizationData(account_id=None, customer_id=None, developer_token=None, authentication=None)
bulk_service = BulkServiceManager(authorization_data=authorization_data,poll_interval_in_milliseconds = 15000)
customer_service = ServiceClient(
    service='CustomerManagementService', 
    version=12,
    authorization_data=authorization_data,
    environment=environment
)

def home(request, 
         template_name='/index.html',
         authentication_form=None,
         extra_context=None):
    """
    Handles the submission of the Bing Ads username and password authorization form.
    If an authenticated user returns to this page after logging in, the appropriate 
    context is provided to index.html for rendering the page. 
    """
    assert isinstance(request, HttpRequest)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        clear_session_data(request)
        # create a form instance and populate it with data from the request:
        form = authentication_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            authentication = PasswordAuthentication(form.cleaned_data['username'], form.cleaned_data['password'])
            authentication_type = 'PasswordAuthentication'
            environment = form.cleaned_data['environment']
            return authorize_bing_ads_user(request, authentication, authentication_type, environment)
    
    # if returning to this page in the same session with existing Bing Ads credentials
    elif user_has_active_session(request):
        return authorize_bing_ads_user(request, 
                                        pickle.loads(request.session['authentication']), 
                                        request.session['authentication_type'], 
                                        request.session['environment'])

    # if the web application user has a refresh token stored, try to use it
    elif user_has_refresh_token(request.user.username):
        return redirect('/callback')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = authentication_form()
        form.username = ""
        form.password = ""

        return render(
            request,
            'app/index.html',
            context_instance = RequestContext(request,
            {
                'form': form,
                'year':datetime.now().year,
            })
        )

def viewcampaigns(request):
    """Renders the viewcampaigns page that contains campaign data for accounts that the user can access."""
    assert isinstance(request, HttpRequest)

    if not user_has_active_session(request):
        return render(
            request,
            'app/viewcampaigns.html',
            context_instance = RequestContext(request,
            {
                'title': 'Campaign Data',
                'accounts': None,
                'year':datetime.now().year,
            })
        )

    global bulk_service
    global customer_service

    user = None
    accounts = None
    campaigns = []
    ad_groups = []
    text_ads = []
    keywords = []
    errors = []

    try:
        user = get_user(None)
        accounts = search_accounts_by_user_id(user.Id)

        download_parameters = DownloadParameters(data_scope = { 'EntityData' },
                                                    entities = { 'Campaigns', 'AdGroups', 'Keywords', 'Ads' },
                                                    file_type = 'Csv',
                                                    campaign_ids = None,
                                                    last_sync_time_in_utc = None,
                                                    location_target_version = None,
                                                    performance_stats_date_range = None)

        for account in accounts:
            bulk_service._authorization_data.account_id = account.Id
            bulk_service._authorization_data.customer_id = account.ParentCustomerId

            bulk_file_reader = bulk_service.download_entities(download_parameters, progress = None)
        
            for bulk_entity in bulk_file_reader:
                if(isinstance(bulk_entity, BulkCampaign)):
                    campaigns.append(bulk_entity)
                if(isinstance(bulk_entity, BulkAdGroup)):
                    ad_groups.append(bulk_entity)
                if(isinstance(bulk_entity, BulkTextAd)):
                    text_ads.append(bulk_entity)
                if(isinstance(bulk_entity, BulkKeyword)):
                    keywords.append(bulk_entity)

    except KeyError:
        pass

    except WebFault as ex:
        errors=get_webfault_errors(ex)
        pass

    return render(
        request,
        'app/viewcampaigns.html',
        context_instance = RequestContext(request,
        {
            'title': 'Campaign Data',
            'bingadsuser': user,
            'accounts': accounts,
            'campaigns': campaigns,
            'ad_groups': ad_groups,
            'errors': errors,
            'year':datetime.now().year,
        })
    )

def callback(request):
    """Handles the Microsoft Account authorization callback."""
    assert isinstance(request, HttpRequest)

    authentication = OAuthWebAuthCodeGrant(settings.CLIENT_ID,
                                          settings.CLIENT_SECRET, 
                                          settings.REDIRECTION_URI)
    authentication_type = 'OAuthWebAuthCodeGrant'
    environment = 'production'

    return authorize_bing_ads_user(request, authentication, authentication_type, environment)

def authorize_bing_ads_user(request, authentication, authentication_type, environment):
    assert isinstance(request, HttpRequest)
    
    global customer_service
    bingadsuser = None

    try:
        Users = get_user_model()
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=request.user.username, password=password)
 
    try:
        bingadsuser = user.bingadsuser
    except BingAdsUser.DoesNotExist:
        bingadsuser = BingAdsUser()
        bingadsuser.user = user
        pass
    
    # If we have a refresh token let's refresh it
    if(authentication_type == 'OAuthWebAuthCodeGrant' and bingadsuser != None and bingadsuser.refresh_token != ""):
        authentication.request_oauth_tokens_by_refresh_token(bingadsuser.refresh_token)
        bingadsuser.refresh_token = authentication.oauth_tokens.refresh_token

    # If the current HTTP request is a callback from the Microsoft Account authorization server,
    # use the current request url containing authorization code to request new access and refresh tokens
    elif (authentication_type == 'OAuthWebAuthCodeGrant' and request.GET.get('code') != None):
        authentication.request_oauth_tokens_by_response_uri(response_uri = request.get_full_path()) 
        bingadsuser.refresh_token = authentication.oauth_tokens.refresh_token

    # If there is no refresh token saved and no callback from the authorization server, 
    # then connect to the authorization server and request user consent.
    elif (authentication_type == 'OAuthWebAuthCodeGrant' and bingadsuser.refresh_token == ""):
        return redirect(authentication.get_authorization_endpoint())

    set_session_data(request, authentication, authentication_type, environment)
    
    user.save()
    bingadsuser.save()
    
    # At this point even if the user has a valid web application user account, we don't know whether they have access to Bing Ads.
    # Let's test to see if they can call Bing Ads services, and only let Bing Ads users login to this application. 

    bing_ads_user = None
    errors=[]

    try:
        bing_ads_user = get_user(None)
    except WebFault as ex:
        errors=get_webfault_errors(ex)
        pass

    form = BingAdsPasswordAuthenticationForm()
    form.username = ""
    form.password = ""

    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'bingadsuser': bing_ads_user,
            'errors': errors,
            'form': form,
            'year':datetime.now().year,
        })
    )

def revoke(request):
    """Revokes access to the Bing Ads accounts of the user authenticated in the current session."""
    assert isinstance(request, HttpRequest)

    try:
        Users = get_user_model()
        user = User.objects.get(username=request.user.username)
        bingadsuser = user.bingadsuser
        if(bingadsuser != None):
            bingadsuser.refresh_token = ""
            bingadsuser.save()
    except User.DoesNotExist:
        pass
    except BingAdsUser.DoesNotExist:
        pass

    clear_session_data(request)

    form = BingAdsPasswordAuthenticationForm()
    form.username = ""
    form.password = ""

    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'form': form,
            'year':datetime.now().year,
        })
    )

def user_has_active_session(request):
    try:
        return True if request.session['authentication'] else False 
    except KeyError:
        return False

def user_has_refresh_token(username):
    try:
        Users = get_user_model()
        user = User.objects.get(username=username)
        bingadsuser = user.bingadsuser
        if(bingadsuser != None and bingadsuser.refresh_token != ""):
            return True
    except User.DoesNotExist:
        return False
    except BingAdsUser.DoesNotExist:
        return False

def set_session_data(request, authentication, authentication_type, environment):
    global authorization_data
    global bulk_service
    global customer_service
    
    try:
        request.session['authentication'] = pickle.dumps(authentication)
        request.session['authentication_type'] = authentication_type
        request.session['environment'] = environment

        authorization_data.authentication = authentication
        authorization_data.developer_token = settings.DEVELOPER_TOKEN_SANDBOX \
                                            if request.session['environment'] == 'sandbox' \
                                            else settings.DEVELOPER_TOKEN
        
        bulk_service = BulkServiceManager(authorization_data=authorization_data,
                                          poll_interval_in_milliseconds = 15000,
                                          environment=environment)
        customer_service = customer_service = ServiceClient(
            service='CustomerManagementService', 
            version=12,
            authorization_data=authorization_data,
            environment=environment
        )

    except KeyError:
        pass
    return None   

def clear_session_data(request):
    global authorization_data
    global bulk_service
    global customer_service

    request.session['authentication'] = None
    request.session['authentication_type'] = None
    request.session['environment'] = None

    authorization_data = AuthorizationData(account_id=None, customer_id=None, developer_token=None, authentication=None)
    bulk_service = BulkServiceManager(authorization_data=authorization_data,poll_interval_in_milliseconds = 15000)
    customer_service = customer_service = ServiceClient(
        service='CustomerManagementService', 
        version=12,
        authorization_data=authorization_data,
        environment=environment
    )

def applogout(request):
    logout(request)
    clear_session_data(request)
    return redirect('/')

def get_user(user_id):
    ''' 
    Gets a User object by the specified UserId.
    
    :param user_id: The Bing Ads user identifier.
    :type user_id: long
    :return: The Bing Ads user.
    :rtype: User
    '''
    global customer_service
    return customer_service.GetUser(
            UserId = user_id
        ).User

def search_accounts_by_user_id(user_id):
    ''' 
    Search for account details by UserId.
    
    :param user_id: The Bing Ads user identifier.
    :type user_id: long
    :return: List of accounts that the user can manage.
    :rtype: ArrayOfAdvertiserAccount
    '''
    global customer_service
    paging = {
            'Index': 0,
            'Size': 10
        }

    predicates = {
        'Predicate':
            [
                {
                    'Field': 'UserId',
                    'Operator': 'Equals',
                    'Value': user_id,
                },
            ]
        }

    search_accounts_request = {
            'PageInfo': paging,
            'Predicates': predicates
        }
        
    search_accounts_response = customer_service.SearchAccounts(
        PageInfo = paging,
        Predicates = predicates
    )
        
    return search_accounts_response['AdvertiserAccount']

def get_webfault_errors(ex):
    errors=[]
    if hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
        and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
        and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
        api_errors = ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
        if type(api_errors) == list:
            for api_error in api_errors:
                errors.append(api_error)
        else:
            errors.append(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors = ex.fault.detail.ApiFaultDetail.Errors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                errors.append(api_error)
        else:
            errors.append(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors = ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                errors.append(api_error)
        else:
            errors.append(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFault') \
        and hasattr(ex.fault.detail.ApiFault, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFault.OperationErrors, 'OperationError'):
        api_errors = ex.fault.detail.ApiFault.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                errors.append(api_error)
        else:
            errors.append(api_errors)
    # Handle serialization errors e.g. The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v9:Entities.
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors = ex.fault.detail.ExceptionDetail
        if type(api_errors) == list:
            for api_error in api_errors:
                errors.append(api_error)
        else:
            errors.append(api_errors)
    else:
        raise Exception('Unknown WebFault')
    return errors
