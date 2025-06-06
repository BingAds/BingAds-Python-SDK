from auth_helper_rest import *
from openapi_client.models.campaign import *
from time import strftime, gmtime


def main(authorization_data):
    try:
        # Add a campaign that will later be associated with negative keywords.
        campaign = Campaign(
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50,
            languages=['All'],
            name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            time_zone='PacificTimeUSCanadaTijuana'
        )
        campaigns = [campaign]

        add_campaigns_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=campaigns
        )

        add_campaigns_response = campaign_service.add_campaigns(
            add_campaigns_request=add_campaigns_request
        )
        campaign_ids = add_campaigns_response.CampaignIds

        # Create exclusive negative keywords for the campaign
        negative_keywords = [
            NegativeKeyword(
                match_type=MatchType.EXACT,
                text="auto"
            ),
            NegativeKeyword(
                match_type=MatchType.PHRASE,
                text="auto"
            )
        ]

        entity_negative_keyword = EntityNegativeKeyword(
            entity_id=campaign_ids[0],
            entity_type="Campaign",
            negative_keywords=negative_keywords
        )
        entity_negative_keywords = [entity_negative_keyword]

        add_negative_keywords_request = AddNegativeKeywordsToEntitiesRequest(
            entity_negative_keywords=entity_negative_keywords
        )

        add_negative_keywords_response = campaign_service.add_negative_keywords_to_entities(
            add_negative_keywords_to_entities_request=add_negative_keywords_request
        )

        # Delete negative keywords (demonstrates partial failure by design)
        delete_negative_keywords_request = DeleteNegativeKeywordsFromEntitiesRequest(
            entity_negative_keywords=entity_negative_keywords
        )
        nested_partial_errors = campaign_service.delete_negative_keywords_from_entities(
            delete_negative_keywords_from_entities_request=delete_negative_keywords_request
        )

        # Create a shared negative keyword list
        negative_keyword_list = NegativeKeywordList(
            name="My Negative Keyword List " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            type="NegativeKeywordList"
        )

        shared_list_items = [
            SharedListItem(NegativeKeyword(
                text="car",
                type="NegativeKeyword",
                match_type=MatchType.EXACT
            )),
            SharedListItem(NegativeKeyword(
                text="car",
                type="NegativeKeyword",
                match_type=MatchType.PHRASE
            ))
        ]

        add_shared_entity_request = AddSharedEntityRequest(
            shared_entity=SharedEntity(SharedList(negative_keyword_list)),
            list_items=shared_list_items
        )

        add_shared_entity_response = campaign_service.add_shared_entity(
            add_shared_entity_request=add_shared_entity_request
        )
        shared_entity_id = add_shared_entity_response.SharedEntityId

        # Associate the shared negative keyword list with the campaign
        shared_entity_association = SharedEntityAssociation(
            entity_id=campaign_ids[0],
            entity_type="Campaign",
            shared_entity_id=shared_entity_id,
            shared_entity_type="NegativeKeywordList"
        )
        shared_entity_associations = [shared_entity_association]

        set_shared_entity_associations_request = SetSharedEntityAssociationsRequest(
            associations=shared_entity_associations
        )

        partial_errors = campaign_service.set_shared_entity_associations(
            set_shared_entity_associations_request=set_shared_entity_associations_request
        )

        # Delete the campaign
        delete_campaigns_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=campaign_ids
        )

        campaign_service.delete_campaigns(
            delete_campaigns_request=delete_campaigns_request
        )

        # Delete the shared negative keyword list
        negative_keyword_list = NegativeKeywordList(
            id=shared_entity_id
        )
        negative_keyword_lists = [SharedEntity(SharedList(negative_keyword_list))]

        delete_shared_entities_request = DeleteSharedEntitiesRequest(
            shared_entities=negative_keyword_lists
        )

        partial_errors = campaign_service.delete_shared_entities(
            delete_shared_entities_request=delete_shared_entities_request
        )

    except Exception as ex:
        print(f"Error occurred: {str(ex)}")


if __name__ == '__main__':
    print("Loading the web service client...")

    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    authenticate(authorization_data)

    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)