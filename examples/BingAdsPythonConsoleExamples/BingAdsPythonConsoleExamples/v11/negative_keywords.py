import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

from auth_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Add a campaign that will later be associated with negative keywords. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'
        campaigns.Campaign.append(campaign)

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("Campaign Ids:")
        output_ids(campaign_ids)

        # You may choose to associate an exclusive set of negative keywords to an individual campaign 
        # or ad group. An exclusive set of negative keywords cannot be shared with other campaigns 
        # or ad groups. This example only associates negative keywords with a campaign.

        entity_negative_keywords=campaign_service.factory.create('ArrayOfEntityNegativeKeyword')
        entity_negative_keyword=set_elements_to_none(campaign_service.factory.create('EntityNegativeKeyword'))
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

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
        negative_keyword_list.Name="My Negative Keyword List " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        negative_keyword_list.Type="NegativeKeywordList"
        
        negative_keywords=campaign_service.factory.create('ArrayOfSharedListItem')
        negative_keyword_1=set_elements_to_none(campaign_service.factory.create('NegativeKeyword'))
        negative_keyword_1.Text="car"
        negative_keyword_1.Type="NegativeKeyword"
        negative_keyword_1.MatchType='Exact'
        negative_keywords.SharedListItem.append(negative_keyword_1)
        negative_keyword_2=set_elements_to_none(campaign_service.factory.create('NegativeKeyword'))
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

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
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

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
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

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
        negative_keyword_list.Id=shared_entity_id
        negative_keywords=campaign_service.GetListItemsBySharedList(SharedList=negative_keyword_list)
        if negative_keywords is None or len(negative_keywords) == 0:
            output_status_message("None\n")
        else:
            output_negative_keywords(negative_keywords)

        # Whether you created the list with or without negative keywords, more can be added 
        # using the AddListItemsToSharedList operation.

        negative_keywords=campaign_service.factory.create('ArrayOfSharedListItem')
        negative_keyword_1=set_elements_to_none(campaign_service.factory.create('NegativeKeyword'))
        negative_keyword_1.Text="auto"
        negative_keyword_1.Type="NegativeKeyword"
        negative_keyword_1.MatchType='Exact'
        negative_keywords.SharedListItem.append(negative_keyword_1)
        negative_keyword_2=set_elements_to_none(campaign_service.factory.create('NegativeKeyword'))
        negative_keyword_2.Text="auto"
        negative_keyword_2.Type="NegativeKeyword"
        negative_keyword_2.MatchType='Phrase'
        negative_keywords.SharedListItem.append(negative_keyword_2)

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
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

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
        negative_keyword_list.Id=shared_entity_id
        negative_keywords=campaign_service.GetListItemsBySharedList(SharedList=negative_keyword_list)
        if negative_keywords is None or len(negative_keywords) == 0:
            output_status_message("None\n")
        else:
            output_negative_keywords(negative_keywords)

        # You can update the name of the negative keyword list. 

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
        negative_keyword_list.Id=shared_entity_id
        negative_keyword_list.Name="My Updated Negative Keyword List"
        negative_keyword_list.Type="NegativeKeywordList"

        negative_keyword_lists=campaign_service.factory.create('ArrayOfSharedEntity')
        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
        negative_keyword_list.Id=shared_entity_id
        negative_keyword_lists.SharedEntity.append(negative_keyword_list)
        partial_errors=campaign_service.UpdateSharedEntities(SharedEntities=negative_keyword_lists)
        if partial_errors is None:
            output_status_message("Updated Negative Keyword List Name to {0}.\n".format(negative_keyword_list.Name))
        else:
            output_partial_errors(partial_errors)

        # Get and print the negative keyword lists and return the list of identifiers.

        SHARED_ENTITY_TYPE="NegativeKeywordList"
        shared_entities=campaign_service.GetSharedEntitiesByAccountId(SharedEntityType=SHARED_ENTITY_TYPE)
        shared_entity_ids=[]
        if hasattr(shared_entities, 'SharedEntity'):
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

        # Negative keywords were added to the negative keyword list above. You can associate the 
        # shared list of negative keywords with a campaign with or without negative keywords. 
        # Shared negative keyword lists cannot be associated with an ad group. An ad group can only 
        # be assigned an exclusive set of negative keywords. 

        shared_entity_associations=campaign_service.factory.create('ArrayOfSharedEntityAssociation')
        shared_entity_association=set_elements_to_none(campaign_service.factory.create('SharedEntityAssociation'))
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

# Main execution
if __name__ == '__main__':

    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")
    
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
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)