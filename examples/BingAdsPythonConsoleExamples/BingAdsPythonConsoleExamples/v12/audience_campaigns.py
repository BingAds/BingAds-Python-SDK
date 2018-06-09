from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# You'll need to add media before you can run this example. 
# For details, see image_media.py

LANDSCAPE_IMAGE_MEDIA_ID = 0
LANDSCAPE_LOGO_MEDIA_ID = 0
SQUARE_IMAGE_MEDIA_ID = 0
SQUARE_LOGO_MEDIA_ID = 0

def main(authorization_data):

    try:
        # Setup an Audience campaign with one ad group and a responsive ad.
                
        # Campaign

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        # CampaignType must be set for Audience campaigns
        campaign.CampaignType = ['Audience']
        # Languages must be set for Audience campaigns
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages = languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Red shoes line."
        campaign.DailyBudget = 50
        campaign.BudgetType = 'DailyBudgetStandard'
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'
        campaign.Settings=None
        campaigns.Campaign.append(campaign)

        # AdGroup

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
        # Language cannot be set for ad groups in Audience campaigns
        ad_group.Language = None
        # Network cannot be set for ad groups in Audience campaigns
        ad_group.Network = None

        # By including the corresponding TargetSettingDetail, 
        # this example sets the "target and bid" option for 
        # CompanyName, Industry, and JobFunction. We will only deliver ads to 
        # people who meet at least one of your criteria.
        # By default the "bid only" option is set for Audience, Age, and Gender.
        # We will deliver ads to all audiences, ages, and genders, if they meet
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

        # ResponsiveAd        

        ads=campaign_service.factory.create('ArrayOfAd')
        responsive_ad=set_elements_to_none(campaign_service.factory.create('ResponsiveAd'))
        # Not applicable for responsive ads
        responsive_ad.AdFormatPreference = None
        responsive_ad.BusinessName = "Contoso"
        responsive_ad.CallToAction = 'AddToCart'
        # Not applicable for responsive ads
        responsive_ad.DevicePreference = None
        responsive_ad.EditorialStatus = None
        responsive_ad.FinalAppUrls = None
        final_mobile_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
        responsive_ad.FinalMobileUrls=final_mobile_urls
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        responsive_ad.FinalUrls=final_urls
        responsive_ad.ForwardCompatibilityMap = None
        responsive_ad.Headline = "Fast & Easy Setup"
        responsive_ad.Id = None
        responsive_ad.LandscapeImageMediaId = LANDSCAPE_IMAGE_MEDIA_ID
        responsive_ad.LandscapeLogoMediaId = LANDSCAPE_LOGO_MEDIA_ID
        responsive_ad.LongHeadline = "Find New Customers & Increase Sales!"
        responsive_ad.SquareImageMediaId = SQUARE_IMAGE_MEDIA_ID
        responsive_ad.SquareLogoMediaId = SQUARE_LOGO_MEDIA_ID
        responsive_ad.Status = None
        responsive_ad.Text = "Find New Customers & Increase Sales! Start Advertising on Contoso Today."
        responsive_ad.TrackingUrlTemplate = None
        responsive_ad.Type = 'ResponsiveAd'
        responsive_ad.UrlCustomParameters = None
        ads.Ad.append(responsive_ad)
        
        # Add the campaign, ad group, and ad
        
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("Campaign Ids:")
        output_array_of_long(campaign_ids)
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
        output_array_of_batcherror(add_ad_groups_response.PartialErrors)
        
        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids={
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        output_status_message("Ad Ids:")
        output_array_of_long(ad_ids)
        output_array_of_batcherror(add_ads_response.PartialErrors)
        
        # Whether or not the "target and bid" option has been set for a given
        # criterion type group, you can set bid adjustments for specific criteria.
                
        ad_group_criterions=campaign_service.factory.create('ArrayOfAdGroupCriterion')
        fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
        fixed_bid.Amount=0.50
        
        ad_group_companyname_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        ad_group_companyname_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_companyname_criterion.Status='Paused'
        companyname_criterion=set_elements_to_none(campaign_service.factory.create('ProfileCriterion'))
        companyname_criterion.ProfileId = 808251207 # Microsoft
        companyname_criterion.ProfileType = 'CompanyName'
        ad_group_companyname_criterion.Criterion=companyname_criterion        
        ad_group_companyname_criterion.CriterionBid=fixed_bid
        ad_group_criterions.AdGroupCriterion.append(ad_group_companyname_criterion)

        ad_group_industry_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        ad_group_industry_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_industry_criterion.Status='Paused'
        industry_criterion=set_elements_to_none(campaign_service.factory.create('ProfileCriterion'))
        industry_criterion.ProfileId = 807658654 # Computer & Network Security
        industry_criterion.ProfileType = 'Industry'
        ad_group_industry_criterion.Criterion=industry_criterion        
        ad_group_industry_criterion.CriterionBid=fixed_bid
        ad_group_criterions.AdGroupCriterion.append(ad_group_industry_criterion)

        ad_group_jobfunction_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        ad_group_jobfunction_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_jobfunction_criterion.Status='Paused'
        jobfunction_criterion=set_elements_to_none(campaign_service.factory.create('ProfileCriterion'))
        jobfunction_criterion.ProfileId = 807658477 # Engineering
        jobfunction_criterion.ProfileType = 'JobFunction'
        ad_group_jobfunction_criterion.Criterion=jobfunction_criterion        
        ad_group_jobfunction_criterion.CriterionBid=fixed_bid
        ad_group_criterions.AdGroupCriterion.append(ad_group_jobfunction_criterion)

        # Exclude ages twenty-five through thirty-four.

        ad_group_negative_age_criterion=set_elements_to_none(campaign_service.factory.create('NegativeAdGroupCriterion'))
        ad_group_negative_age_criterion.AdGroupId=ad_group_ids['long'][0]
        ad_group_negative_age_criterion.Status='Paused'
        age_criterion=set_elements_to_none(campaign_service.factory.create('AgeCriterion'))
        age_criterion.AgeRange = 'TwentyFiveToThirtyFour'
        ad_group_negative_age_criterion.Criterion=age_criterion
        ad_group_criterions.AdGroupCriterion.append(ad_group_negative_age_criterion)

        output_status_message("\nAdding Ad Group Criteria . . . \n")         
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_criterions,
            CriterionType='Targets'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("New Ad Group Criterion Ids:")
        output_array_of_long(ad_group_criterion_ids)
        output_array_of_batcherrorcollection(add_ad_group_criterions_response.NestedPartialErrors)

        # Delete the campaign, ad group, criteria, and ad that were previously added. 
        # You should remove this line if you want to view the added entities in the 
        # Bing Ads web application or another tool.

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted CampaignId {0}\n".format(campaign_ids['long'][0]))
        
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
