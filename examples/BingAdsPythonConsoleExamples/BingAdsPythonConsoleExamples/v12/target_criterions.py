from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def get_example_campaign_ids(authorization_data):

    campaigns=campaign_service.factory.create('ArrayOfCampaign')
    campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
    campaign.CampaignType=['Search']
    campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    campaign.Description='Red shoes line.'
    campaign.DailyBudget=50
    campaign.BudgetType='DailyBudgetStandard'
    campaign.TimeZone='PacificTimeUSCanadaTijuana'
    campaigns.Campaign.append(campaign)

    ad_groups=campaign_service.factory.create('ArrayOfAdGroup')

    for index in range(3):
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Shoe Sale " + str(index)
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        ad_group.Language='English'
        ad_groups.AdGroup.append(ad_group)

    # Add the campaigns and ad groups

    add_campaigns_response=campaign_service.AddCampaigns(
        AccountId=authorization_data.account_id,
        Campaigns=campaigns
    )
    campaign_ids={
        'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
    }
    output_status_message('Campaign Ids:')
    output_array_of_long(campaign_ids)
    if hasattr(add_campaigns_response.PartialErrors, 'BatchError'):
        output_array_of_batcherror(add_campaigns_response.PartialErrors)
        
    add_ad_groups_response=campaign_service.AddAdGroups(
        CampaignId=campaign_ids['long'][0],
        AdGroups=ad_groups
    )
    ad_group_ids={
        'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
    }
    output_status_message("Ad Group Ids:")
    output_array_of_long(ad_group_ids)
    if hasattr(add_ad_groups_response.PartialErrors, 'BatchError'):
        output_array_of_batcherror(add_ad_groups_response.PartialErrors)
    
    return campaign_ids

def main(authorization_data):

    try:
        campaign_ids = get_example_campaign_ids(authorization_data)
                
        # You can set campaign_ids null to get all campaigns in the account, instead of 
        # adding and retrieving the example campaigns.

        get_campaigns=campaign_service.GetCampaignsByIds(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids,
            CampaignType=ALL_CAMPAIGN_TYPES
        ).Campaigns
                        
        # Loop through all campaigns and ad groups to get the target criterion IDs.

        for campaign in get_campaigns['Campaign']:
            campaign_id = campaign.Id

            # Set campaign_criterion_ids null to get all criterions 
            # (of the specified target criterion type or types) for the current campaign.

            get_campaign_criterions_by_ids_response = campaign_service.GetCampaignCriterionsByIds(
                CampaignId=campaign_id,
                CampaignCriterionIds=None,
                CriterionType=ALL_TARGET_CAMPAIGN_CRITERION_TYPES
            )
            campaign_criterions= get_campaign_criterions_by_ids_response.CampaignCriterions['CampaignCriterion'] \
                if hasattr(get_campaign_criterions_by_ids_response.CampaignCriterions, 'CampaignCriterion') \
                else None
            
            # When you first create a campaign or ad group using the Bing Ads API, it will not have any 
            # criterions. Effectively, the brand new campaign and ad group target all ages, days, hours, 
            # devices, genders, and locations. As a best practice, you should consider at a minimum 
            # adding a campaign location criterion corresponding to the customer market country.

            if campaign_criterions is None or len(campaign_criterions['CampaignCriterion']) <= 0:
                campaign_criterions=campaign_service.factory.create('ArrayOfCampaignCriterion')

                # Define the Campaign Location Criterion

                campaign_location_criterion=set_elements_to_none(campaign_service.factory.create('BiddableCampaignCriterion'))
                campaign_location_criterion.Type='BiddableCampaignCriterion'
                campaign_location_criterion.CampaignId=campaign_id

                bid_multiplier=set_elements_to_none(campaign_service.factory.create('BidMultiplier'))
                bid_multiplier.Type='BidMultiplier'
                bid_multiplier.Multiplier=0
                campaign_location_criterion.CriterionBid=bid_multiplier
                
                location_criterion=set_elements_to_none(campaign_service.factory.create('LocationCriterion'))
                location_criterion.Type='LocationCriterion'
                # United States
                location_criterion.LocationId=190
                campaign_location_criterion.Criterion=location_criterion

                campaign_criterions.CampaignCriterion.append(campaign_location_criterion)

                # Define the Campaign Location Intent Criterion

                campaign_location_intent_criterion=set_elements_to_none(campaign_service.factory.create('BiddableCampaignCriterion'))
                campaign_location_intent_criterion.Type='BiddableCampaignCriterion'
                campaign_location_intent_criterion.CampaignId=campaign_id
                
                location_intent_criterion=set_elements_to_none(campaign_service.factory.create('LocationIntentCriterion'))
                location_intent_criterion.Type='LocationIntentCriterion'
                location_intent_criterion.IntentOption='PeopleInOrSearchingForOrViewingPages'
                campaign_location_intent_criterion.Criterion=location_intent_criterion

                campaign_criterions.CampaignCriterion.append(campaign_location_intent_criterion)

                add_campaign_criterions_response = campaign_service.AddCampaignCriterions(
                    CampaignCriterions=campaign_criterions,
                    CriterionType='Targets'
                )
                
                # Capture the new criterion IDs.

                if add_campaign_criterions_response is not None and len(add_campaign_criterions_response.CampaignCriterionIds) > 0:
                    campaign_criterion_ids={
                        'long': add_campaign_criterions_response.CampaignCriterionIds['long'] if add_campaign_criterions_response.CampaignCriterionIds['long'] else None
                    }
                    for index in range(len(campaign_criterion_ids['long'])):
                        campaign_criterions['CampaignCriterion'][index].Id = campaign_criterion_ids['long'][index]
                         
            # You can now store or output the campaign criterions

            output_status_message("Campaign Criterions: \n")
            output_array_of_campaigncriterion(campaign_criterions)

            get_ad_groups=campaign_service.GetAdGroupsByCampaignId(
                CampaignId=campaign_id
            )

            # Loop through all ad groups to get the target criterion IDs.
            for ad_group in get_ad_groups['AdGroup']:
                ad_group_id = ad_group.Id

                # Set ad_group_criterion_ids null to get all criterions 
                # (of the specified target criterion type or types) for the current ad group.
                get_ad_group_criterions_by_ids_response = campaign_service.GetAdGroupCriterionsByIds(
                    AdGroupId=ad_group_id,
                    AdGroupCriterionIds=None,
                    CriterionType=ALL_TARGET_AD_GROUP_CRITERION_TYPES
                )
                ad_group_criterions= get_ad_group_criterions_by_ids_response \
                    if hasattr(get_ad_group_criterions_by_ids_response, 'AdGroupCriterion') \
                    else None

                if ad_group_criterions is not None:

                    # If the Smartphones device criterion already exists, we'll increase the bid multiplier by 5 percent.
 
                    update_ad_group_criterions=campaign_service.factory.create('ArrayOfAdGroupCriterion')
                    for ad_group_criterion in ad_group_criterions['AdGroupCriterion']:
                        if ad_group_criterion.Criterion is not None \
                           and ad_group_criterion.Criterion.Type.lower() == 'devicecriterion' \
                           and ad_group_criterion.Criterion.DeviceName.lower() == "smartphones":
                            ad_group_criterion.CriterionBid.Multiplier *= 1.05
                            update_ad_group_criterions.AdGroupCriterion.append(ad_group_criterion)
                        
                    if update_ad_group_criterions is not None and len(update_ad_group_criterions) > 0:
                        update_ad_group_criterions_response = campaign_service.UpdateAdGroupCriterions(
                            AdGroupCriterions=update_ad_group_criterions,
                            CriterionType='Targets'
                        )
                        
                    # You can now store or output the ad group criterions

                    output_status_message("Ad Group Criterions: ")
                    output_array_of_adgroupcriterion(ad_group_criterions)

        # Delete the campaign and ad group that were previously added. 
                
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )

        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

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
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account.       

    authenticate(authorization_data)       

    main(authorization_data)
