from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # To discover all remarketing lists that the user can associate with ad groups in the current account (per CustomerAccountId header), 
        # set AudienceIds to null when calling the GetAudiencesByIds operation.
        remarketing_lists=campaign_service.GetAudiencesByIds(
            AudienceIds=None,
            Type='RemarketingList'
        ).Audiences

        # For this example you must already have at least one remarketing list. 

        if (len(remarketing_lists) < 1):
            output_status_message("You do not have any remarketing lists that the current user can associate with ad groups.\n")
            sys.exit(0)

        # Add an ad group in a campaign. The ad group will later be associated with remarketing lists. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'
        
        campaigns.Campaign.append(campaign)

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoes"
        ad_group.AdDistribution='Search'
        ad_group.Network='OwnedAndOperatedAndSyndicatedSearch'
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        search_bid=campaign_service.factory.create('Bid')
        search_bid.Amount=0.09
        ad_group.SearchBid=search_bid
        ad_group.Language='English'

        # Applicable for all remarketing lists that are associated with this ad group. TargetAndBid indicates 
        # that you want to show ads only to people included in the remarketing list, with the option to change
        # the bid amount. Ads in this ad group will only show to people included in the remarketing list.
        ad_group.RemarketingTargetingSetting='TargetAndBid'

        ad_groups.AdGroup.append(ad_group)

        # Add the campaign and ad group

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("Campaign Ids:")
        output_array_of_long(campaign_ids)
        
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("Ad Group Ids:")
        output_array_of_long(ad_group_ids)

        # If the campaign or ad group add operations failed then we cannot continue this example. 

        if ad_group_ids is None or len(ad_group_ids) < 1:
            sys.exit(0)
        
        ad_group_remarketing_list_associations=campaign_service.factory.create('ArrayOfAdGroupCriterion')
        
        # This example associates all of the remarketing lists with the new ad group.

        for remarketing_list in remarketing_lists['Audience']:
            biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
            biddable_ad_group_criterion.AdGroupId=ad_group_ids['long'][0]
            biddable_ad_group_criterion.Status='Paused'
            audience_criterion=set_elements_to_none(campaign_service.factory.create('AudienceCriterion'))
            audience_criterion.AudienceId=remarketing_list.Id
            audience_criterion.AudienceType='RemarketingList'
            biddable_ad_group_criterion.Criterion=audience_criterion
            bid_multiplier=set_elements_to_none(campaign_service.factory.create('BidMultiplier'))
            bid_multiplier.Multiplier=20.00
            biddable_ad_group_criterion.CriterionBid=bid_multiplier

            ad_group_remarketing_list_associations.AdGroupCriterion.append(biddable_ad_group_criterion)

            output_status_message("\nAssociating the following remarketing list with the ad group\n")
            output_remarketinglist(remarketing_list)

         
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_remarketing_list_associations,
            CriterionType='Audience'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("Ad Group Criterion Ids:")
        output_array_of_long(ad_group_criterion_ids)

        get_ad_group_criterions_by_ids_response = campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=ad_group_criterion_ids,
            CriterionType='RemarketingList'
        )
        
        for ad_group_remarketing_list_association in get_ad_group_criterions_by_ids_response['AdGroupCriterion']:
            output_status_message("\nThe following ad group remarketing list association was added.\n")
            output_biddableadgroupcriterion(ad_group_remarketing_list_association)
               
        # If the associations were added and retrieved successfully let's practice updating and deleting one of them.

        ad_group_remarketing_list_associations=campaign_service.factory.create('ArrayOfAdGroupCriterion')

        if ad_group_criterion_ids is not None and len(ad_group_criterion_ids) > 0:
            update_biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
            update_biddable_ad_group_criterion.AdGroupId=ad_group_ids['long'][0]
            update_biddable_ad_group_criterion.Id=ad_group_criterion_ids['long'][0]
            update_biddable_ad_group_criterion.Status='Active'
            update_audience_criterion=set_elements_to_none(campaign_service.factory.create('AudienceCriterion'))
            update_audience_criterion.AudienceType='RemarketingList'
            update_audience_criterion.Criterion=audience_criterion
            update_bid_multiplier=set_elements_to_none(campaign_service.factory.create('BidMultiplier'))
            update_bid_multiplier.Multiplier=10.00
            update_biddable_ad_group_criterion.CriterionBid=update_bid_multiplier

            ad_group_remarketing_list_associations.AdGroupCriterion.append(update_biddable_ad_group_criterion)

            update_ad_group_criterions_response = campaign_service.UpdateAdGroupCriterions(
                AdGroupCriterions=ad_group_remarketing_list_associations,
                CriterionType='Audience'
            )
             
            delete_ad_group_criterions_response = campaign_service.DeleteAdGroupCriterions(
                AdGroupId=ad_group_ids['long'][0],
                AdGroupCriterionIds=ad_group_criterion_ids,
                CriterionType='Audience'
            )

        # Delete the campaign, ad group, and ad group remarketing list associations that were previously added. 
        # You should remove this line if you want to view the added entities in the 
        # Bing Ads web application or another tool.
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
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
            
    authenticate(authorization_data)
        
    main(authorization_data)
