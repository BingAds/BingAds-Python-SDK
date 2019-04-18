from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Create an Audience campaign with one ad group.

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        # CampaignType must be set for Audience campaigns
        campaign.CampaignType = ['Audience']
        # Languages must be set for Audience campaigns
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages = languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.DailyBudget = 50
        campaign.BudgetType = 'DailyBudgetStandard'
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
        ad_group.Network='OwnedAndOperatedAndSyndicatedSearch'
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        # Network cannot be set for ad groups in Audience campaigns
        ad_group.Network = None
        # Sets the "target and bid" option for CompanyName, Industry, and JobFunction. 
        # Microsoft will only deliver ads to people who meet at least one of your criteria.
        # By default the "bid only" option is set for Audience, Age, and Gender.
        # Microsoft will deliver ads to all audiences, ages, and genders, if they meet
        # your company name, industry, or job function criteria.  
        ad_group_settings=campaign_service.factory.create('ArrayOfSetting')
        ad_group_target_setting=campaign_service.factory.create('TargetSetting')
        ad_group_companyname_target_setting_detail=campaign_service.factory.create('TargetSettingDetail')
        ad_group_companyname_target_setting_detail.CriterionTypeGroup='CompanyName'
        ad_group_companyname_target_setting_detail.TargetAndBid=True
        ad_group_target_setting.Details.TargetSettingDetail.append(ad_group_companyname_target_setting_detail)
        ad_group_industry_target_setting_detail=campaign_service.factory.create('TargetSettingDetail')
        ad_group_industry_target_setting_detail.CriterionTypeGroup='Industry'
        ad_group_industry_target_setting_detail.TargetAndBid=True
        ad_group_target_setting.Details.TargetSettingDetail.append(ad_group_industry_target_setting_detail)
        ad_group_jobfunction_target_setting_detail=campaign_service.factory.create('TargetSettingDetail')
        ad_group_jobfunction_target_setting_detail.CriterionTypeGroup='JobFunction'
        ad_group_jobfunction_target_setting_detail.TargetAndBid=True
        ad_group_target_setting.Details.TargetSettingDetail.append(ad_group_jobfunction_target_setting_detail)
        ad_group_settings.Setting.append(ad_group_target_setting)
        ad_group.Settings=ad_group_settings        
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

        # Whether or not the "target and bid" option has been set for a given
        # criterion type group, you can set bid adjustments for specific criteria.
                
        ad_group_criterions=campaign_service.factory.create('ArrayOfAdGroupCriterion')
        bid_multiplier=set_elements_to_none(campaign_service.factory.create('BidMultiplier'))
        bid_multiplier.Multiplier=20
        
        ad_group_companyname_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        ad_group_companyname_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_companyname_criterion.Status='Paused'
        companyname_criterion=set_elements_to_none(campaign_service.factory.create('ProfileCriterion'))
        companyname_criterion.ProfileId = 808251207 # Microsoft
        companyname_criterion.ProfileType = 'CompanyName'
        ad_group_companyname_criterion.Criterion=companyname_criterion        
        ad_group_companyname_criterion.CriterionBid=bid_multiplier
        ad_group_criterions.AdGroupCriterion.append(ad_group_companyname_criterion)

        ad_group_industry_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        ad_group_industry_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_industry_criterion.Status='Paused'
        industry_criterion=set_elements_to_none(campaign_service.factory.create('ProfileCriterion'))
        industry_criterion.ProfileId = 807658654 # Computer & Network Security
        industry_criterion.ProfileType = 'Industry'
        ad_group_industry_criterion.Criterion=industry_criterion        
        ad_group_industry_criterion.CriterionBid=bid_multiplier
        ad_group_criterions.AdGroupCriterion.append(ad_group_industry_criterion)

        ad_group_jobfunction_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        ad_group_jobfunction_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_jobfunction_criterion.Status='Paused'
        jobfunction_criterion=set_elements_to_none(campaign_service.factory.create('ProfileCriterion'))
        jobfunction_criterion.ProfileId = 807658477 # Engineering
        jobfunction_criterion.ProfileType = 'JobFunction'
        ad_group_jobfunction_criterion.Criterion=jobfunction_criterion        
        ad_group_jobfunction_criterion.CriterionBid=bid_multiplier
        ad_group_criterions.AdGroupCriterion.append(ad_group_jobfunction_criterion)

        # Exclude ages twenty-five through thirty-four.

        ad_group_negative_age_criterion=set_elements_to_none(campaign_service.factory.create('NegativeAdGroupCriterion'))
        ad_group_negative_age_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_negative_age_criterion.Status='Paused'
        age_criterion=set_elements_to_none(campaign_service.factory.create('AgeCriterion'))
        age_criterion.AgeRange = 'TwentyFiveToThirtyFour'
        ad_group_negative_age_criterion.Criterion=age_criterion
        ad_group_criterions.AdGroupCriterion.append(ad_group_negative_age_criterion)

        output_status_message("-----\nAddAdGroupCriterions:")         
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_criterions,
            CriterionType='Targets'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("AdGroupCriterionIds:")
        output_array_of_long(ad_group_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherrorcollection(add_ad_group_criterions_response.NestedPartialErrors)

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
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    authenticate(authorization_data)
    
    main(authorization_data)
