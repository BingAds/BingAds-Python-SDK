from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v10 import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    ENVIRONMENT='production'
    DEVELOPER_TOKEN='YourDeveloperTokenGoesHere'
    CLIENT_ID='YourClientIdGoesHere'

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

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication   

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    # If we have a refresh token let's refresh it
    if refresh_token is not None:
        authentication.request_oauth_tokens_by_refresh_token(refresh_token)
    else:
        webbrowser.open(authentication.get_authorization_endpoint(), new=1)
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

        # Request access and refresh tokens using the URI that you provided manually during program execution.
        authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

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
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v9:Entities.
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

def output_campaign_ids(campaign_ids):
    for id in campaign_ids['long']:
        output_status_message("Campaign successfully added and assigned CampaignId {0}\n".format(id))

def output_negative_keyword_ids(id_collections):
    if not hasattr(id_collections, 'IdCollection'):
        return None
    for index in range(0, len(id_collections['IdCollection'])):
        output_status_message("NegativeKeyword Ids at entity index {0}:\n".format(index))
        for id in id_collections['IdCollection'][index].Ids['long']:
            output_status_message("\tId: {0}\n".format(id))

def output_entity_negative_keywords(entity_negative_keywords):
    if not hasattr(entity_negative_keywords, 'EntityNegativeKeyword'):
        return None
    output_status_message("EntityNegativeKeyword item:\n")
    for entity_negative_keyword in entity_negative_keywords['EntityNegativeKeyword']:
        output_status_message("\tEntityId: {0}".format(entity_negative_keyword.EntityId))
        output_status_message("\tEntityType: {0}\n".format(entity_negative_keyword.EntityType))
        output_negative_keywords(entity_negative_keyword.NegativeKeywords)
        
def get_and_output_shared_entity_identifiers(shared_entity_type):
    shared_entities=campaign_service.GetSharedEntitiesByAccountId(SharedEntityType=shared_entity_type)
    if not hasattr(shared_entities, 'SharedEntity'):
        return None
    shared_entity_ids=[]
    index=0
    for shared_entity in shared_entities['SharedEntity']:
        shared_entity_ids.append(shared_entity.Id)
        output_status_message(
            "SharedEntity[{0}] ({1}) has SharedEntity Id {2}.\n".format(
                index,
                shared_entity.Name,
                shared_entity.Id
            )
        )
        index=index+1
    return shared_entity_ids

def output_negative_keywords(negative_keywords):
    if not hasattr(negative_keywords, 'NegativeKeyword'):
        return None
    output_status_message("NegativeKeyword item:\n")
    for negative_keyword in negative_keywords['NegativeKeyword']:
        output_status_message("\tText: {0}".format(negative_keyword.Text))
        output_status_message("\tId: {0}".format(negative_keyword.Id))
        output_status_message("\tMatchType: {0}\n".format(negative_keyword.MatchType))

def output_negative_keyword_results(
            shared_list_id,
            shared_list_items,
            shared_list_item_ids,
            partial_errors
        ):
    if not hasattr(shared_list_items, 'SharedListItem'):
        return None
    for index in range(0, len(shared_list_items['SharedListItem'])-1):
        # Determine if the SharedListItem is a NegativeKeyword.
        if shared_list_items['SharedListItem'][index].Type == 'NegativeKeyword':
            # Determine if the corresponding index has a valid identifier
            if shared_list_item_ids['long'][index] > 0:
                output_status_message(
                    "NegativeKeyword[{0}] ({1}) successfully added to NegativeKeywordList ({2}) and assigned Negative Keyword Id {3}.".format(
                        index,
                        shared_list_items['SharedListItem'][index].Text,
                        shared_list_id,
                        shared_list_item_ids['long'][index]
                    )
                )
            else:
                output_status_message("SharedListItem is not a NegativeKeyword.")
    output_partial_errors(partial_errors)

def output_shared_entity_associations(associations):
    if not hasattr(associations, 'SharedEntityAssociation'):
        return None
    output_status_message("SharedEntityAssociation item:\n")
    for shared_entity_association in associations['SharedEntityAssociation']:
        output_status_message("\tEntityId: {0}".format(shared_entity_association.EntityId))
        output_status_message("\tEntityType: {0}".format(shared_entity_association.EntityType))
        output_status_message("\tSharedEntityId: {0}".format(shared_entity_association.SharedEntityId))
        output_status_message("\tSharedEntityType: {0}\n".format(shared_entity_association.SharedEntityType))
    
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

def output_nested_partial_errors(nested_partial_errors):
    if not hasattr(nested_partial_errors, 'BatchErrorCollection'):
        return None
    output_status_message("BatchErrorCollection (NestedPartialErrors) item:\n")
    for collection in nested_partial_errors['BatchErrorCollection']:
        # The top level list index corresponds to the campaign or ad group index identifier.
        if collection is not None:
            if hasattr(collection, 'Code'):
                output_status_message("\tIndex: {0}".format(collection.Index))
                output_status_message("\tCode: {0}".format(collection.Code))
                output_status_message("\tErrorCode: {0}".format(collection.ErrorCode))
                output_status_message("\tMessage: {0}\n".format(collection.Message))
            
            # The nested list of batch errors would include any errors specific to the negative keywords 
            # that you attempted to add or remove from the campaign or ad group.
            for error in collection.BatchErrors['BatchError']:
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
        
        # Add a campaign that will later be associated with negative keywords. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=campaign_service.factory.create('Campaign')
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' # Accepts 'true', 'false', True, or False
        campaign.Status='Paused'
        campaigns.Campaign.append(campaign)

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        
        output_campaign_ids(campaign_ids)

        # You may choose to associate an exclusive set of negative keywords to an individual campaign 
        # or ad group. An exclusive set of negative keywords cannot be shared with other campaigns 
        # or ad groups. This example only associates negative keywords with a campaign.

        entity_negative_keywords=campaign_service.factory.create('ArrayOfEntityNegativeKeyword')
        entity_negative_keyword=campaign_service.factory.create('EntityNegativeKeyword')
        entity_negative_keyword.EntityId=campaign_ids['long'][0]
        entity_negative_keyword.EntityType="Campaign"
        negative_keywords=campaign_service.factory.create('ArrayOfNegativeKeyword')
        negative_keyword=campaign_service.factory.create('NegativeKeyword')
        negative_keyword.MatchType='Phrase'
        negative_keyword.Text="auto"
        negative_keywords.NegativeKeyword.append(negative_keyword)
        entity_negative_keyword.NegativeKeywords=negative_keywords
        entity_negative_keywords.EntityNegativeKeyword.append(entity_negative_keyword)

        add_negative_keywords_to_entities_response=campaign_service.AddNegativeKeywordsToEntities(
            EntityNegativeKeywords=entity_negative_keywords
        )

        output_negative_keyword_ids(add_negative_keywords_to_entities_response.NegativeKeywordIds)
        output_nested_partial_errors(add_negative_keywords_to_entities_response.NestedPartialErrors)

        if add_negative_keywords_to_entities_response.NestedPartialErrors is None \
        and len(add_negative_keywords_to_entities_response.NestedPartialErrors['BatchErrorCollection']) == 0:
            output_status_message("Added an exclusive set of negative keywords to the Campaign.\n")
            output_negative_keyword_ids(add_negative_keywords_to_entities_response.NegativeKeywordIds)
        else:
            output_nested_partial_errors(add_negative_keywords_to_entities_response.NestedPartialErrors)
        
        get_negative_keywords_by_entity_ids_response=campaign_service.GetNegativeKeywordsByEntityIds(
            EntityIds=campaign_ids, 
            EntityType="Campaign", 
            ParentEntityId=authorization_data.account_id
        )

        output_entity_negative_keywords(get_negative_keywords_by_entity_ids_response.EntityNegativeKeywords)
        output_partial_errors(get_negative_keywords_by_entity_ids_response.PartialErrors)

        if hasattr(get_negative_keywords_by_entity_ids_response.PartialErrors, 'BatchError'):
            output_partial_errors(get_negative_keywords_by_entity_ids_response.PartialErrors)
        else:
            output_status_message("Retrieved an exclusive set of negative keywords for the Campaign.\n")
            output_entity_negative_keywords(get_negative_keywords_by_entity_ids_response.EntityNegativeKeywords)
        '''
        if get_negative_keywords_by_entity_ids_response.PartialErrors is None \
        and len(get_negative_keywords_by_entity_ids_response.PartialErrors) == 0:
            output_status_message("Retrieved an exclusive set of negative keywords for the Campaign.\n")
            output_entity_negative_keywords(get_negative_keywords_by_entity_ids_response.EntityNegativeKeywords)
        else:
            output_partial_errors(get_negative_keywords_by_entity_ids_response.PartialErrors)
        '''
        # If you attempt to delete a negative keyword without an identifier the operation will
        # succeed but will return partial errors corresponding to the index of the negative keyword
        # that was not deleted. 
        nested_partial_errors=campaign_service.DeleteNegativeKeywordsFromEntities(
            EntityNegativeKeywords=entity_negative_keywords
        )

        if nested_partial_errors is None or len(nested_partial_errors) == 0:
            output_status_message("Deleted an exclusive set of negative keywords from the Campaign.\n")
        else:
            output_status_message("Attempt to DeleteNegativeKeywordsFromEntities without NegativeKeyword identifier partially fails by design.")
            output_nested_partial_errors(nested_partial_errors)

        # Delete the negative keywords with identifiers that were returned above.
        nested_partial_errors=campaign_service.DeleteNegativeKeywordsFromEntities(get_negative_keywords_by_entity_ids_response.EntityNegativeKeywords)
        if nested_partial_errors is None or len(nested_partial_errors) == 0:
            output_status_message("Deleted an exclusive set of negative keywords from the Campaign.\n")
        else:
            output_nested_partial_errors(nested_partial_errors)

        # Negative keywords can also be added and deleted from a shared negative keyword list. 
        # The negative keyword list can be shared or associated with multiple campaigns.
        # NegativeKeywordList inherits from SharedList which inherits from SharedEntity.

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Name="My Negative Keyword List " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        negative_keyword_list.Type="NegativeKeywordList"
        
        negative_keywords=campaign_service.factory.create('ArrayOfSharedListItem')
        negative_keyword_1=campaign_service.factory.create('NegativeKeyword')
        negative_keyword_1.Text="car"
        negative_keyword_1.Type="NegativeKeyword"
        negative_keyword_1.MatchType='Exact'
        negative_keywords.SharedListItem.append(negative_keyword_1)
        negative_keyword_2=campaign_service.factory.create('NegativeKeyword')
        negative_keyword_2.Text="car"
        negative_keyword_2.Type="NegativeKeyword"
        negative_keyword_2.MatchType='Phrase'
        negative_keywords.SharedListItem.append(negative_keyword_2)

        # You can create a new list for negative keywords with or without negative keywords.

        add_shared_entity_response=campaign_service.AddSharedEntity(
            SharedEntity=negative_keyword_list, 
            ListItems=negative_keywords
        )
        shared_entity_id=add_shared_entity_response.SharedEntityId
        list_item_ids=add_shared_entity_response.ListItemIds

        output_status_message("NegativeKeywordList successfully added to account library and assigned identifer {0}\n".format(shared_entity_id))

        output_negative_keyword_results(
            shared_entity_id,
            negative_keywords,
            list_item_ids,
            add_shared_entity_response.PartialErrors
        )

        output_status_message("Negative keywords currently in NegativeKeywordList:")

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keywords=campaign_service.GetListItemsBySharedList(SharedList=negative_keyword_list)
        if negative_keywords is None or len(negative_keywords) == 0:
            output_status_message("None\n")
        else:
            output_negative_keywords(negative_keywords)

        # To update the list of negative keywords, you must either add or remove from the list
        # using the respective AddListItemsToSharedList or DeleteListItemsFromSharedList operations.
        # To remove the negative keywords from the list pass the negative keyword identifers
        # and negative keyword list (SharedEntity) identifer.

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        partial_errors=campaign_service.DeleteListItemsFromSharedList(
            ListItemIds=list_item_ids, 
            SharedList=negative_keyword_list
        )
        if partial_errors is None:
            output_status_message("Deleted most recently added negative keywords from negative keyword list.\n")
        else:
            output_partial_errors(partial_errors)

        output_status_message("Negative keywords currently in NegativeKeywordList:")

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keywords=campaign_service.GetListItemsBySharedList(SharedList=negative_keyword_list)
        if negative_keywords is None or len(negative_keywords) == 0:
            output_status_message("None\n")
        else:
            output_negative_keywords(negative_keywords)

        # Whether you created the list with or without negative keywords, more can be added 
        # using the AddListItemsToSharedList operation.

        negative_keywords=campaign_service.factory.create('ArrayOfSharedListItem')
        negative_keyword_1=campaign_service.factory.create('NegativeKeyword')
        negative_keyword_1.Text="auto"
        negative_keyword_1.Type="NegativeKeyword"
        negative_keyword_1.MatchType='Exact'
        negative_keywords.SharedListItem.append(negative_keyword_1)
        negative_keyword_2=campaign_service.factory.create('NegativeKeyword')
        negative_keyword_2.Text="auto"
        negative_keyword_2.Type="NegativeKeyword"
        negative_keyword_2.MatchType='Phrase'
        negative_keywords.SharedListItem.append(negative_keyword_2)

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id

        add_list_items_to_shared_list_response=campaign_service.AddListItemsToSharedList(
            ListItems=negative_keywords,
            SharedList=negative_keyword_list
        )
        list_item_ids=add_list_items_to_shared_list_response.ListItemIds

        output_negative_keyword_results(
            shared_entity_id,
            negative_keywords,
            list_item_ids,
            add_list_items_to_shared_list_response.PartialErrors
        )

        output_status_message("Negative keywords currently in NegativeKeywordList:")

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keywords=campaign_service.GetListItemsBySharedList(SharedList=negative_keyword_list)
        if negative_keywords is None or len(negative_keywords) == 0:
            output_status_message("None\n")
        else:
            output_negative_keywords(negative_keywords)

        # You can update the name of the negative keyword list. 

        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keyword_list.Name="My Updated Negative Keyword List"
        negative_keyword_list.Type="NegativeKeywordList"

        negative_keyword_lists=campaign_service.factory.create('ArrayOfSharedEntity')
        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keyword_lists.SharedEntity.append(negative_keyword_list)
        partial_errors=campaign_service.UpdateSharedEntities(SharedEntities=negative_keyword_lists)
        if partial_errors is None:
            output_status_message("Updated Negative Keyword List Name to {0}.\n".format(negative_keyword_list.Name))
        else:
            output_partial_errors(partial_errors)

        # Get and print the negative keyword lists and return the list of identifiers.

        SHARED_ENTITY_TYPE="NegativeKeywordList"
        shared_entity_ids=get_and_output_shared_entity_identifiers(SHARED_ENTITY_TYPE)

        # Negative keywords were added to the negative keyword list above. You can associate the 
        # shared list of negative keywords with a campaign with or without negative keywords. 
        # Shared negative keyword lists cannot be associated with an ad group. An ad group can only 
        # be assigned an exclusive set of negative keywords. 

        shared_entity_associations=campaign_service.factory.create('ArrayOfSharedEntityAssociation')
        shared_entity_association=campaign_service.factory.create('SharedEntityAssociation')
        shared_entity_association.EntityId=campaign_ids['long'][0]
        shared_entity_association.EntityType="Campaign"
        shared_entity_association.SharedEntityId=shared_entity_id
        shared_entity_association.SharedEntityType="NegativeKeywordList" 
        shared_entity_associations.SharedEntityAssociation.append(shared_entity_association)
        
        partial_errors=campaign_service.SetSharedEntityAssociations(Associations=shared_entity_associations)
        if partial_errors is None:
            output_status_message(
                "Associated CampaignId {0} with Negative Keyword List Id {1}.\n".format(campaign_ids['long'][0], shared_entity_id)
            )
        else:
            output_partial_errors(partial_errors)

        # Get and print the associations either by Campaign or NegativeKeywordList identifier.
        get_shared_entity_associations_by_entity_ids_response=campaign_service.GetSharedEntityAssociationsByEntityIds(
            EntityIds=campaign_ids, 
            EntityType="Campaign", 
            SharedEntityType="NegativeKeywordList"
        )
        output_shared_entity_associations(get_shared_entity_associations_by_entity_ids_response.Associations)
        output_partial_errors(get_shared_entity_associations_by_entity_ids_response.PartialErrors)

        # Currently the GetSharedEntityAssociationsBySharedEntityIds operation accepts only one shared entity identifier in the list.
        get_shared_entity_associations_by_shared_entity_ids_response=campaign_service.GetSharedEntityAssociationsBySharedEntityIds(
            EntityType="Campaign", 
            SharedEntityIds={'long': [shared_entity_ids[len(shared_entity_ids) - 1]]}, 
            SharedEntityType="NegativeKeywordList"
        )
        output_shared_entity_associations(get_shared_entity_associations_by_shared_entity_ids_response.Associations)
        output_partial_errors(get_shared_entity_associations_by_shared_entity_ids_response.PartialErrors)

        # Explicitly delete the association between the campaign and the negative keyword list.

        partial_errors=campaign_service.DeleteSharedEntityAssociations(Associations=shared_entity_associations)
        if partial_errors is None:
            output_status_message("Deleted NegativeKeywordList associations\n")
        else:
            output_partial_errors(partial_errors)

        # Delete the campaign and any remaining assocations. 

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )

        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

        # DeleteCampaigns does not delete the negative keyword list from the account's library. 
        # Call the DeleteSharedEntities operation to delete the shared entities.

        negative_keyword_lists=campaign_service.factory.create('ArrayOfSharedEntity')
        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keyword_lists.SharedEntity.append(negative_keyword_list)
        partial_errors=campaign_service.DeleteSharedEntities(SharedEntities=negative_keyword_lists)
        if partial_errors is None:
            output_status_message("Deleted Negative Keyword List (SharedEntity) Id {0}\n".format(shared_entity_id))
        else:
            output_partial_errors(partial_errors)

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

