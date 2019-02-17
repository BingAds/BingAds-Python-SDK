from auth_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Add a campaign that will later be associated with negative keywords. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        campaign.Description="Red shoes line."
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaigns.Campaign.append(campaign)

        output_status_message("-----\nAddCampaigns:")
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("CampaignIds:")
        output_array_of_long(campaign_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_campaigns_response.PartialErrors)

        # You may choose to associate an exclusive set of negative keywords to an individual campaign 
        # or ad group. An exclusive set of negative keywords cannot be shared with other campaigns 
        # or ad groups. This example only associates negative keywords with a campaign.

        entity_negative_keywords=campaign_service.factory.create('ArrayOfEntityNegativeKeyword')
        entity_negative_keyword=set_elements_to_none(campaign_service.factory.create('EntityNegativeKeyword'))
        entity_negative_keyword.EntityId=campaign_ids['long'][0]
        entity_negative_keyword.EntityType="Campaign"
        negative_keywords=campaign_service.factory.create('ArrayOfNegativeKeyword')
        auto_exact=campaign_service.factory.create('NegativeKeyword')
        auto_exact.MatchType='Exact'
        auto_exact.Text="auto"
        negative_keywords.NegativeKeyword.append(auto_exact)
        auto_phrase=campaign_service.factory.create('NegativeKeyword')
        auto_phrase.MatchType='Phrase'
        auto_phrase.Text="auto"
        negative_keywords.NegativeKeyword.append(auto_phrase)
        entity_negative_keyword.NegativeKeywords=negative_keywords
        entity_negative_keywords.EntityNegativeKeyword.append(entity_negative_keyword)

        output_status_message("-----\nAddNegativeKeywordsToEntities:")
        add_negative_keywords_to_entities_response=campaign_service.AddNegativeKeywordsToEntities(
            EntityNegativeKeywords=entity_negative_keywords
        )
        output_status_message("Added an exclusive set of negative keywords to the Campaign.")
        output_status_message("NegativeKeywordIds:")
        output_array_of_idcollection(add_negative_keywords_to_entities_response.NegativeKeywordIds)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherrorcollection(add_negative_keywords_to_entities_response.NestedPartialErrors)
        
        # If you attempt to delete a negative keyword without an identifier the operation will return
        # partial errors corresponding to the index of the negative keyword that was not deleted. 
        
        output_status_message("-----\nDeleteNegativeKeywordsFromEntities:")
        nested_partial_errors=campaign_service.DeleteNegativeKeywordsFromEntities(
            EntityNegativeKeywords=entity_negative_keywords
        )
        output_status_message("Attempt to DeleteNegativeKeywordsFromEntities without NegativeKeyword identifier partially fails by design.")
        output_array_of_batcherrorcollection(nested_partial_errors)

        # Negative keywords can also be added and deleted from a shared negative keyword list. 
        # The negative keyword list can be shared or associated with multiple campaigns.
        # NegativeKeywordList inherits from SharedList which inherits from SharedEntity.

        negative_keyword_list=set_elements_to_none(campaign_service.factory.create('NegativeKeywordList'))
        negative_keyword_list.Name="My Negative Keyword List " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        negative_keyword_list.Type="NegativeKeywordList"
        
        negative_keywords=campaign_service.factory.create('ArrayOfSharedListItem')
        car_exact=set_elements_to_none(campaign_service.factory.create('NegativeKeyword'))
        car_exact.Text="car"
        car_exact.Type="NegativeKeyword"
        car_exact.MatchType='Exact'
        negative_keywords.SharedListItem.append(car_exact)
        car_phrase=set_elements_to_none(campaign_service.factory.create('NegativeKeyword'))
        car_phrase.Text="car"
        car_phrase.Type="NegativeKeyword"
        car_phrase.MatchType='Phrase'
        negative_keywords.SharedListItem.append(car_phrase)

        # You can create a new list for negative keywords with or without negative keywords.

        output_status_message("-----\nAddSharedEntity:")
        add_shared_entity_response=campaign_service.AddSharedEntity(
            SharedEntity=negative_keyword_list, 
            ListItems=negative_keywords
        )
        shared_entity_id=add_shared_entity_response.SharedEntityId
        list_item_ids=add_shared_entity_response.ListItemIds
        output_status_message("NegativeKeywordList added to account library and assigned identifer {0}".format(shared_entity_id))
        
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
        
        output_status_message("-----\nSetSharedEntityAssociations:")
        partial_errors=campaign_service.SetSharedEntityAssociations(
            Associations=shared_entity_associations)
        output_status_message(
            "Associated CampaignId {0} with Negative Keyword List Id {1}.".format(campaign_ids['long'][0], shared_entity_id)
        )

        # Delete the campaign and everything it contains e.g., ad groups and ads.

        output_status_message("-----\nDeleteCampaigns:")
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted Campaign Id {0}".format(campaign_ids['long'][0]))

        # DeleteCampaigns does not delete the negative keyword list from the account's library. 
        #/ Call the DeleteSharedEntities operation to delete the negative keyword list.

        negative_keyword_lists=campaign_service.factory.create('ArrayOfSharedEntity')
        negative_keyword_list=campaign_service.factory.create('NegativeKeywordList')
        negative_keyword_list.Id=shared_entity_id
        negative_keyword_lists.SharedEntity.append(negative_keyword_list)

        output_status_message("-----\nDeleteSharedEntities:")
        partial_errors=campaign_service.DeleteSharedEntities(
            SharedEntities=negative_keyword_lists)
        output_status_message("Deleted Negative Keyword List Id {0}".format(shared_entity_id))

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
