from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Setup a campaign with one ad group.
                
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
        
        # Add an ad group within the campaign.

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoe Sale"
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        current_time=gmtime()
        end_date.Year=current_time.tm_year + 1
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        ad_groups.AdGroup.append(ad_group)

        output_status_message("-----\nAddAdGroups:")
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups,
            ReturnInheritedBidStrategyTypes=False
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("AdGroupIds:")
        output_array_of_long(ad_group_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ad_groups_response.PartialErrors)

        # When you first create a campaign or ad group using the Bing Ads API, it will not have any 
        # criterions. Effectively, the brand new campaign and ad group target all ages, days, hours, 
        # devices, genders, and locations. As a best practice, you should consider at a minimum 
        # adding a campaign location criterion corresponding to the customer market country.

        campaign_criterions=campaign_service.factory.create('ArrayOfCampaignCriterion')
        campaign_location_criterion=set_elements_to_none(campaign_service.factory.create('BiddableCampaignCriterion'))
        campaign_location_criterion.Type='BiddableCampaignCriterion'
        campaign_location_criterion.CampaignId=campaign_ids['long'][0]
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

        output_status_message("-----\nAddCampaignCriterions:")
        add_campaign_criterions_response = campaign_service.AddCampaignCriterions(
            CampaignCriterions=campaign_criterions,
            CriterionType='Targets'
        )
        campaign_criterion_ids={
            'long': add_campaign_criterions_response.CampaignCriterionIds['long'] 
            if add_campaign_criterions_response.CampaignCriterionIds['long'] else None
        }
        output_status_message("CampaignCriterionIds:")
        output_array_of_long(campaign_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherrorcollection(add_campaign_criterions_response.NestedPartialErrors)  

        # A negative location criterion is an excluded location.
        # Ads in this ad group will not be shown to people in Redmond, WA.

        ad_group_criterions=campaign_service.factory.create('ArrayOfAdGroupCriterion')
        ad_group_negative_location_criterion=set_elements_to_none(campaign_service.factory.create('NegativeAdGroupCriterion'))
        ad_group_negative_location_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_negative_location_criterion.Status='Active'
        location_criterion=set_elements_to_none(campaign_service.factory.create('LocationCriterion'))
        # Redmond|Washington|United States
        location_criterion.LocationId=67555
        location_criterion.Type='LocationCriterion'
        ad_group_negative_location_criterion.Criterion=location_criterion
        ad_group_criterions.AdGroupCriterion.append(ad_group_negative_location_criterion)
         
        output_status_message("-----\nAddAdGroupCriterions:")
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_criterions,
            CriterionType='Targets'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] 
            if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("AdGroupCriterionIds:")
        output_array_of_long(ad_group_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherror(add_ad_group_criterions_response.NestedPartialErrors)

        # Delete the campaign and everything it contains e.g., ad groups and ads.

        output_status_message("-----\nDeleteCampaigns:")
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted Campaign Id {0}".format(campaign_ids['long'][0]))

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
