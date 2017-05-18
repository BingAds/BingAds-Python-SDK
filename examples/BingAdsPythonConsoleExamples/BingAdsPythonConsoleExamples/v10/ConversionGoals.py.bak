from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v10 import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport.http').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    DEVELOPER_TOKEN='DeveloperTokenGoesHere'
    ENVIRONMENT='production'
    
    # If you are using OAuth in production, CLIENT_ID is required and CLIENT_STATE is recommended.
    CLIENT_ID='ClientIdGoesHere'
    CLIENT_STATE='ClientStateGoesHere'

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=10,
    )

    customer_service=ServiceClient(
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=9,
    )

def authenticate_with_username():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with PasswordAuthentication.
    '''
    global authorization_data
    authentication=PasswordAuthentication(
        user_name='UserNameGoesHere',
        password='PasswordGoesHere'
    )

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication
 
def authenticate_with_oauth():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with OAuthDesktopMobileAuthCodeGrant.
    '''
    global authorization_data

    authentication=OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID
    )

    # It is recommended that you specify a non guessable 'state' request parameter to help prevent
    # cross site request forgery (CSRF). 
    authentication.state=CLIENT_STATE

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication   

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    try:
        # If we have a refresh token let's refresh it
        if refresh_token is not None:
            authorization_data.authentication.request_oauth_tokens_by_refresh_token(refresh_token)
        else:
            request_user_consent()
    except OAuthTokenRequestException:
        # The user could not be authenticated or the grant is expired. 
        # The user must first sign in and if needed grant the client application access to the requested scope.
        request_user_consent()
    
def request_user_consent():
    global authorization_data

    webbrowser.open(authorization_data.authentication.get_authorization_endpoint(), new=1)
    # For Python 3.x use 'input' instead of 'raw_input'
    if(sys.version_info.major >= 3):
        response_uri=input(
            "You need to provide consent for the application to access your Bing Ads accounts. " \
            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
            "please enter the response URI that includes the authorization 'code' parameter: \n"
        )
    else:
        response_uri=raw_input(
            "You need to provide consent for the application to access your Bing Ads accounts. " \
            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
            "please enter the response URI that includes the authorization 'code' parameter: \n"
        )

    if authorization_data.authentication.state != CLIENT_STATE:
       raise Exception("The OAuth response state does not match the client request state.")

    # Request access and refresh tokens using the URI that you provided manually during program execution.
    authorization_data.authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

def get_refresh_token():
    ''' 
    Returns a refresh token if stored locally.
    '''
    file=None
    try:
        file=open("refresh.txt")
        line=file.readline()
        file.close()
        return line if line else None
    except IOError:
        if file:
            file.close()
        return None

def save_refresh_token(oauth_tokens):
    ''' 
    Stores a refresh token locally. Be sure to save your refresh token securely.
    '''
    with open("refresh.txt","w+") as file:
        file.write(oauth_tokens.refresh_token)
        file.close()
    return None

def search_accounts_by_user_id(user_id):
    ''' 
    Search for account details by UserId.
    
    :param user_id: The Bing Ads user identifier.
    :type user_id: long
    :return: List of accounts that the user can manage.
    :rtype: ArrayOfAccount
    '''
    global customer_service
   
    paging={
        'Index': 0,
        'Size': 10
    }

    predicates={
        'Predicate': [
            {
                'Field': 'UserId',
                'Operator': 'Equals',
                'Value': user_id,
            },
        ]
    }

    search_accounts_request={
        'PageInfo': paging,
        'Predicates': predicates
    }
        
    return customer_service.SearchAccounts(
        PageInfo = paging,
        Predicates = predicates
    )

def output_status_message(message):
    print(message)

def output_bing_ads_webfault_error(error):
    if hasattr(error, 'ErrorCode'):
        output_status_message("ErrorCode: {0}".format(error.ErrorCode))
    if hasattr(error, 'Code'):
        output_status_message("Code: {0}".format(error.Code))
    if hasattr(error, 'Message'):
        output_status_message("Message: {0}".format(error.Message))
    output_status_message('')

def output_webfault_errors(ex):
    if hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFault') \
        and hasattr(ex.fault.detail.ApiFault, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFault.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFault.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
        and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
        and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
        api_errors=ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.ApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'EditorialErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.EditorialErrors, 'EditorialError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.EditorialErrors.EditorialError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    # Handle serialization errors e.g. The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v10:Entities.
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors=ex.fault.detail.ExceptionDetail
        if type(api_errors) == list:
            for api_error in api_errors:
                output_status_message(api_error.Message)
        else:
            output_status_message(api_errors.Message)
    else:
        raise Exception('Unknown WebFault')
        
def set_elements_to_none(suds_object):
    # Bing Ads Campaign Management service operations require that if you specify a non-primitives, 
    # it must be one of the values defined by the service i.e. it cannot be a nil element. 
    # Since Suds requires non-primitives and Bing Ads won't accept nil elements in place of an enum value, 
    # you must either set the non-primitives or they must be set to None. Also in case new properties are added 
    # in a future service release, it is a good practice to set each element of the SUDS object to None as a baseline. 

    for (element) in suds_object:
        suds_object.__setitem__(element[0], None)
    return suds_object

def output_uet_tag(uet_tag):
    if uet_tag is not None:
        output_status_message("Description: {0}".format(uet_tag.Description))
        output_status_message("Id: {0}".format(uet_tag.Id))
        output_status_message("Name: {0}".format(uet_tag.Name))
        output_status_message("TrackingNoScript: {0}".format(uet_tag.TrackingNoScript))
        output_status_message("TrackingScript: {0}".format(uet_tag.TrackingScript))
        output_status_message("TrackingStatus: {0}\n".format(uet_tag.TrackingStatus))
    
def output_conversion_goal(conversion_goal):
    if conversion_goal is not None:
        output_status_message("ConversionWindowInMinutes: {0}".format(conversion_goal.ConversionWindowInMinutes))
        output_status_message("CountType: {0}".format(conversion_goal.CountType))
        output_status_message("Id: {0}".format(conversion_goal.Id))
        output_status_message("Name: {0}".format(conversion_goal.Name))
        output_conversion_goal_revenue(conversion_goal.Revenue)
        output_status_message("Scope: {0}".format(conversion_goal.Scope))
        output_status_message("Status: {0}".format(conversion_goal.Status))
        output_status_message("TagId: {0}".format(conversion_goal.TagId))
        output_status_message("TrackingStatus: {0}".format(conversion_goal.TrackingStatus))
        output_status_message("Type: {0}".format(conversion_goal.Type))

        if conversion_goal.Type == 'AppInstall':
            output_status_message("AppPlatform: {0}".format(conversion_goal.AppPlatform))
            output_status_message("AppStoreId: {0}\n".format(conversion_goal.AppStoreId))
        elif conversion_goal.Type == 'Duration':
            output_status_message("MinimumDurationInSeconds: {0}\n".format(conversion_goal.MinimumDurationInSeconds))
        elif conversion_goal.Type == 'Event':
            output_status_message("ActionExpression: {0}".format(conversion_goal.ActionExpression))
            output_status_message("ActionOperator: {0}".format(conversion_goal.ActionOperator))
            output_status_message("CategoryExpression: {0}".format(conversion_goal.CategoryExpression))
            output_status_message("CategoryOperator: {0}".format(conversion_goal.CategoryOperator))
            output_status_message("LabelExpression: {0}".format(conversion_goal.LabelExpression))
            output_status_message("LabelOperator: {0}".format(conversion_goal.LabelOperator))
            output_status_message("Value: {0}".format(conversion_goal.Value))
            output_status_message("ValueOperator: {0}\n".format(conversion_goal.ValueOperator))
        elif conversion_goal.Type == 'PagesViewedPerVisit':
            output_status_message("MinimumPagesViewed: {0}\n".format(conversion_goal.MinimumPagesViewed))
        elif conversion_goal.Type == 'Url':
            output_status_message("UrlExpression: {0}".format(conversion_goal.UrlExpression))
            output_status_message("UrlOperator: {0}\n".format(conversion_goal.UrlOperator))

def output_conversion_goal_revenue(conversion_goal_revenue):
    if conversion_goal_revenue is not None:
        output_status_message("CurrencyCode: {0}".format(conversion_goal_revenue.CurrencyCode))
        output_status_message("Type: {0}".format(conversion_goal_revenue.Type))
        output_status_message("Value: {0}".format(conversion_goal_revenue.Value))

def output_partial_errors(partial_errors):
    if not hasattr(partial_errors, 'BatchError'):
        return None
    output_status_message("BatchError (PartialErrors) item:\n")
    for error in partial_errors['BatchError']:
        output_status_message("\tIndex: {0}".format(error.Index))
        output_status_message("\tCode: {0}".format(error.Code))
        output_status_message("\tErrorCode: {0}".format(error.ErrorCode))
        output_status_message("\tMessage: {0}\n".format(error.Message))

        # In the case of an EditorialError, more details are available
        if error.Type == "EditorialError" and error.ErrorCode == "CampaignServiceEditorialValidationError":
            output_status_message("\tDisapprovedText: {0}".format(error.DisapprovedText))
            output_status_message("\tLocation: {0}".format(error.Location))
            output_status_message("\tPublisherCountry: {0}".format(error.PublisherCountry))
            output_status_message("\tReasonCode: {0}\n".format(error.ReasonCode))

# Main execution
if __name__ == '__main__':

    try:
        # You should authenticate for Bing Ads production services with a Microsoft Account, 
        # instead of providing the Bing Ads username and password set. 
        # Authentication with a Microsoft Account is currently not supported in Sandbox.
        authenticate_with_oauth()
        
        # Uncomment to run with Bing Ads legacy UserName and Password credentials.
        # For example you would use this method to authenticate in sandbox.
        #authenticate_with_username()
        
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)

        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId
        
        # Before you can track conversions or target audiences using a remarketing list, 
        # you need to create a UET tag in Bing Ads (web application or API) and then 
        # add the UET tag tracking code to every page of your website. For more information, please see 
        # Universal Event Tracking at https://msdn.microsoft.com/library/bing-ads-universal-event-tracking-guide.aspx.

        # First you should call the GetUetTagsByIds operation to check whether a tag has already been created. 
        # You can leave the TagIds element null or empty to request all UET tags available for the customer.

        uet_tags = campaign_service.GetUetTagsByIds(None).UetTags

        # If you do not already have a UET tag that can be used, or if you need another UET tag, 
        # call the AddUetTags service operation to create a new UET tag. If the call is successful, 
        # the tracking script that you should add to your website is included in a corresponding 
        # UetTag within the response message. 

        if uet_tags is None or len(uet_tags) < 1:
            uet_tags=campaign_service.factory.create('ArrayOfUetTag')
            uet_tag=set_elements_to_none(campaign_service.factory.create('UetTag'))
            uet_tag.Description="My First Uet Tag"
            uet_tag.Name="New Uet Tag"
            uet_tags.UetTag.append(uet_tag)
            
            uet_tags = campaign_service.AddUetTags(uet_tags).UetTags

        if uet_tags is None or len(uet_tags) < 1:
            output_status_message(
                string.Format("You do not have any UET tags registered for CustomerId {0}.\n", authorizationData.CustomerId)
            )
            sys.exit(0)
        
        output_status_message("List of all UET Tags:\n")
        for uet_tag in uet_tags['UetTag']:
            output_uet_tag(uet_tag)


        # After you retreive the tracking script from the AddUetTags or GetUetTagsByIds operation, 
        # the next step is to add the UET tag tracking code to your website. We recommend that you, 
        # or your website administrator, add it to your entire website in either the head or body sections. 
        # If your website has a master page, then that is the best place to add it because you add it once 
        # and it is included on all pages. For more information, please see 
        # Universal Event Tracking at https://msdn.microsoft.com/library/bing-ads-universal-event-tracking-guide.aspx.


        # We will use the same UET tag for the remainder of this example.

        tag_id = uet_tags['UetTag'][0].Id

        # Optionally you can update the name and description of a UetTag with the UpdateUetTags operation.

        output_status_message("UET Tag BEFORE update:\n")
        output_uet_tag(uet_tags['UetTag'][0])

        update_uet_tags=campaign_service.factory.create('ArrayOfUetTag')
        update_uet_tag=set_elements_to_none(campaign_service.factory.create('UetTag'))
        update_uet_tag.Description="Updated Uet Tag Description"
        update_uet_tag.Name="Updated Uet Tag Name " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        update_uet_tag.Id=tag_id
        update_uet_tags.UetTag.append(update_uet_tag)
        
        campaign_service.UpdateUetTags(update_uet_tags)

        uet_tags = campaign_service.GetUetTagsByIds({'long': tag_id }).UetTags

        output_status_message("UET Tag AFTER update:\n")
        output_uet_tag(uet_tags['UetTag'][0])

        # Add conversion goals that depend on the UET Tag Id retreived above.
        # Please note that you cannot delete conversion goals. If you want to stop 
        # tracking conversions for the goal, you can set the goal status to Paused.

        conversion_goals=campaign_service.factory.create('ArrayOfConversionGoal')

        duration_goal=set_elements_to_none(campaign_service.factory.create('DurationGoal'))
        duration_goal.ConversionWindowInMinutes = 30
        duration_goal.CountType = 'All'
        duration_goal.MinimumDurationInSeconds = 60
        duration_goal.Name = "My Duration Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        duration_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        duration_goal_revenue.Type='FixedValue'
        duration_goal_revenue.Value=5.00
        duration_goal_revenue.CurrencyCode=None
        duration_goal.Revenue = duration_goal_revenue
        duration_goal.Scope = 'Account'
        duration_goal.Status = 'Active'
        duration_goal.TagId = tag_id
        conversion_goals.ConversionGoal.append(duration_goal)

        event_goal=set_elements_to_none(campaign_service.factory.create('EventGoal'))
        # The type of user interaction you want to track.
        event_goal.ActionExpression = "play"
        event_goal.ActionOperator = 'Contains'
        # The category of event you want to track. 
        event_goal.CategoryExpression = "video"
        event_goal.CategoryOperator = 'Contains'
        event_goal.ConversionWindowInMinutes = 30
        event_goal.CountType = 'All'
        # The name of the element that caused the action.
        event_goal.LabelExpression = "trailer"
        event_goal.LabelOperator = 'Contains'
        event_goal.Name = "My Event Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        event_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        event_goal_revenue.Type='FixedValue'
        event_goal_revenue.Value=5.00
        event_goal_revenue.CurrencyCode=None
        event_goal.Revenue = event_goal_revenue
        event_goal.Scope = 'Account'
        event_goal.Status = 'Active'
        event_goal.TagId = tag_id
        # A numerical value associated with that event. 
        # Could be length of the video played etc.
        event_goal.Value = 5.00
        event_goal.ValueOperator = 'Equals'
        conversion_goals.ConversionGoal.append(event_goal)

        pages_viewed_per_visit_goal=set_elements_to_none(campaign_service.factory.create('PagesViewedPerVisitGoal'))
        pages_viewed_per_visit_goal.ConversionWindowInMinutes = 30
        pages_viewed_per_visit_goal.CountType = 'All'
        pages_viewed_per_visit_goal.MinimumPagesViewed = 5
        pages_viewed_per_visit_goal.Name = "My Pages Viewed Per Visit Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        pages_viewed_per_visit_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        pages_viewed_per_visit_goal_revenue.Type='FixedValue'
        pages_viewed_per_visit_goal_revenue.Value=5.00
        pages_viewed_per_visit_goal_revenue.CurrencyCode=None
        pages_viewed_per_visit_goal.Revenue = pages_viewed_per_visit_goal_revenue
        pages_viewed_per_visit_goal.Scope = 'Account'
        pages_viewed_per_visit_goal.Status = 'Active'
        pages_viewed_per_visit_goal.TagId = tag_id
        conversion_goals.ConversionGoal.append(pages_viewed_per_visit_goal)
            
        url_goal=set_elements_to_none(campaign_service.factory.create('UrlGoal'))
        url_goal.ConversionWindowInMinutes = 30
        url_goal.CountType = 'All'
        url_goal.Name = "My Url Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        url_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        url_goal_revenue.Type='FixedValue'
        url_goal_revenue.Value=5.00
        url_goal_revenue.CurrencyCode=None
        url_goal.Revenue = url_goal_revenue
        url_goal.Scope = 'Account'
        url_goal.Status = 'Active'
        url_goal.TagId = tag_id
        url_goal.UrlExpression = "contoso"
        url_goal.UrlOperator = 'Contains'
        conversion_goals.ConversionGoal.append(url_goal)

        app_install_goal=set_elements_to_none(campaign_service.factory.create('AppInstallGoal'))
        # You must provide a valid app platform and app store identifier, 
        # otherwise this goal will not be added successfully. 
        app_install_goal.AppPlatform = "Windows"
        app_install_goal.AppStoreId = "AppStoreIdGoesHere"
        app_install_goal.ConversionWindowInMinutes = 30
        app_install_goal.CountType = 'All'
        app_install_goal.Name = "My App Install Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        app_install_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        app_install_goal_revenue.Type='FixedValue'
        app_install_goal_revenue.Value=5.00
        app_install_goal_revenue.CurrencyCode=None
        app_install_goal.Revenue = app_install_goal_revenue
        # Account scope is not supported for app install goals. You can
        # set scope to Customer or don't set it for the same result.
        app_install_goal.Scope = 'Customer'
        app_install_goal.Status = 'Active'
        # The TagId is inherited from the ConversionGoal base class,
        # however, App Install goals do not use a UET tag.
        app_install_goal.TagId = None
        conversion_goals.ConversionGoal.append(app_install_goal)

        add_conversion_goals_response=campaign_service.AddConversionGoals(ConversionGoals=conversion_goals)
        
        # Find the conversion goals that were added successfully. 

        conversion_goal_ids = []
        for goal_id in add_conversion_goals_response.ConversionGoalIds['long']:
            if goal_id is not None:
                conversion_goal_ids.append(goal_id)

        output_status_message("List of errors returned from AddConversionGoals (if any):\n");
        output_partial_errors(add_conversion_goals_response.PartialErrors);
        
        conversion_goal_types='AppInstall ' \
                              'Duration ' \
                              'Event ' \
                              'PagesViewedPerVisit ' \
                              'Url'
        
        get_conversion_goals = campaign_service.GetConversionGoalsByIds(
            ConversionGoalIds={'long': conversion_goal_ids}, 
            ConversionGoalTypes=conversion_goal_types
        ).ConversionGoals

        output_status_message("List of conversion goals BEFORE update:\n")
        for conversion_goal in get_conversion_goals['ConversionGoal']:
            output_conversion_goal(conversion_goal)
        
        update_conversion_goals=campaign_service.factory.create('ArrayOfConversionGoal')

        update_duration_goal=set_elements_to_none(campaign_service.factory.create('DurationGoal'))
        update_duration_goal.ConversionWindowInMinutes = 60
        update_duration_goal.CountType = 'Unique'
        # You can change the conversion goal type e.g. in this example an event goal
        # had been created above at index 1. Now we are using the returned identifier
        # at index 1 to update the type from EventGoal to DurationGoal.
        update_duration_goal.Id=conversion_goal_ids[1]
        update_duration_goal.MinimumDurationInSeconds = 120
        update_duration_goal.Name = "My Updated Duration Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        update_duration_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        update_duration_goal_revenue.Type='FixedValue'
        update_duration_goal_revenue.Value=10.00
        update_duration_goal_revenue.CurrencyCode=None
        update_duration_goal.Revenue = update_duration_goal_revenue
        # The Scope cannot be updated, even if you update the goal type.
        # You can either send the same value or leave Scope empty.
        update_duration_goal.Scope = 'Account'
        update_duration_goal.Status = 'Paused'
        # You can update the tag as needed. In this example we will explicitly use the same UET tag.
        # To keep the UET tag unchanged, you can also leave this element nil or empty.
        update_duration_goal.TagId = tag_id
        update_conversion_goals.ConversionGoal.append(update_duration_goal)

        update_event_goal=set_elements_to_none(campaign_service.factory.create('EventGoal'))
        # For both add and update conversion goal operations, you must include one or more  
        # of the following events:
        # ActionExpression, CategoryExpression, LabelExpression, or Value. 
        
        # For example if you do not include ActionExpression during update,
        # any existing ActionOperator and ActionExpression settings will be deleted.
        update_event_goal.ActionExpression = None
        update_event_goal.ActionOperator = None
        update_event_goal.CategoryExpression = "video"
        update_event_goal.CategoryOperator = 'Equals'
        update_event_goal.Id = conversion_goal_ids[0]
        # You cannot update the operator unless you also include the expression.
        # The following attempt to update LabelOperator will result in an error.
        update_event_goal.LabelExpression = None
        update_event_goal.LabelOperator = 'Equals'
        update_event_goal.Name = "My Updated Event Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        update_event_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        update_event_goal_revenue.Type='VariableValue'
        update_event_goal_revenue.Value=5.00
        update_event_goal_revenue.CurrencyCode=None
        update_event_goal.Revenue = update_event_goal_revenue
        # You must specify the previous settings unless you want
        # them replaced during the update conversion goal operation.
        update_event_goal.Value = None
        update_event_goal.ValueOperator = 'GreaterThan'
        update_conversion_goals.ConversionGoal.append(update_event_goal)

        update_pages_viewed_per_visit_goal=set_elements_to_none(campaign_service.factory.create('PagesViewedPerVisitGoal'))
        update_pages_viewed_per_visit_goal.Id = conversion_goal_ids[2]
        update_pages_viewed_per_visit_goal.Name = "My Updated Pages Viewed Per Visit Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        update_conversion_goals.ConversionGoal.append(update_pages_viewed_per_visit_goal)
            
        update_url_goal=set_elements_to_none(campaign_service.factory.create('UrlGoal'))
        update_url_goal.Id = conversion_goal_ids[3]
        update_url_goal.Name = "My Updated Url Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        # If not specified during update, the previous Url settings are retained.
        update_url_goal.UrlExpression = None
        update_url_goal.UrlOperator = 'BeginsWith'
        update_conversion_goals.ConversionGoal.append(update_url_goal)

        update_conversion_goals_response = campaign_service.UpdateConversionGoals(update_conversion_goals)

        output_status_message("List of errors returned from UpdateConversionGoals (if any):\n");
        output_partial_errors(update_conversion_goals_response.PartialErrors);
        
        get_conversion_goals = campaign_service.GetConversionGoalsByIds(
            ConversionGoalIds={'long': conversion_goal_ids}, 
            ConversionGoalTypes=conversion_goal_types
        ).ConversionGoals

        output_status_message("List of conversion goals AFTER update:\n")
        for conversion_goal in get_conversion_goals['ConversionGoal']:
            output_conversion_goal(conversion_goal)

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)