from auth_helper import *
from campaignmanagement_example_helper import *
import random

# You must provide credentials in auth_helper.py.

MAX_GET_LABELS_BY_IDS = 1000
MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS = 1
MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS = 100
MAX_PAGING_SIZE = 1000

def main(authorization_data):

    try:
        # Specify one or more campaigns.
        
        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Red shoes line."
        campaign.DailyBudget = 50
        campaign.BudgetType = 'DailyBudgetStandard'
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaigns.Campaign.append(campaign)

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoe Sale"
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        ad_group.Language='English'
        ad_groups.AdGroup.append(ad_group)

        keywords=campaign_service.factory.create('ArrayOfKeyword')
        keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
        keyword.Bid=campaign_service.factory.create('Bid')
        keyword.Bid.Amount=0.47
        keyword.Param2='10% Off'
        keyword.MatchType='Phrase'
        keyword.Text='Brand-A Shoes'
        keywords.Keyword.append(keyword)
        
        ads=campaign_service.factory.create('ArrayOfAd')
        expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad.TitlePart1='Contoso'
        expanded_text_ad.TitlePart2='Fast & Easy Setup'
        expanded_text_ad.Text='Find New Customers & Increase Sales! Start Advertising on Contoso Today.'
        expanded_text_ad.Path1='seattle'
        expanded_text_ad.Path2='shoe sale'
        expanded_text_ad.Type='ExpandedText'
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        expanded_text_ad.FinalUrls=final_urls
        ads.Ad.append(expanded_text_ad)

        labels=campaign_service.factory.create('ArrayOfLabel')
        for index in range(5):
            color = "#{0:06x}".format(random.randint(0,100000))
            label=set_elements_to_none(campaign_service.factory.create('Label'))
            label.ColorCode = color
            label.Description = "Label Description"
            label.Name = "Label Name " + color + " " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            labels.Label.append(label)
        

        # Add the campaign, ad group, keyword, ad, and labels.

        add_labels_response=campaign_service.AddLabels(
            Labels=labels
        )
        label_ids={
            'long': add_labels_response.LabelIds['long'] if add_labels_response.LabelIds['long'] else None
        }
        output_status_message("Label Ids:\n")
        output_array_of_long(label_ids)
        
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("Campaign Ids:\n")
        output_array_of_long(campaign_ids)
        
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("Ad Group Ids:\n")
        output_array_of_long(ad_group_ids)
        
        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids={
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        ad_errors={
            'BatchError': add_ads_response.PartialErrors['BatchError'] if add_ads_response.PartialErrors else None
        }    
        output_status_message("Ad Ids:\n")
        output_array_of_long(ad_ids)
        
        add_keywords_response=campaign_service.AddKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=keywords
        )
        keyword_ids={
            'long': add_keywords_response.KeywordIds['long'] if add_keywords_response.KeywordIds else None
        }
        keyword_errors={
            'BatchError': add_keywords_response.PartialErrors['BatchError'] if add_keywords_response.PartialErrors else None
        } 
        output_status_message("Keyword Ids:\n")
        output_array_of_long(keyword_ids)
        
        output_status_message("Get all the labels that we added above...\n")

        paging=set_elements_to_none(campaign_service.factory.create('Paging'))
        paging.Index=0
        paging.Size=10

        get_labels_by_ids_response = campaign_service.GetLabelsByIds(
            label_ids,
            paging
        )
        output_array_of_label(get_labels_by_ids_response.Labels)

        output_status_message("Update the label color and then retrieve the labels again to confirm the changes....\n")

        update_labels = campaign_service.factory.create('ArrayOfLabel')
        for label in get_labels_by_ids_response.Labels['Label']:
            label.ColorCode = "#{0:06x}".format(random.randint(0,100000))
            update_labels.Label.append(label)

        update_labels_response = campaign_service.UpdateLabels(update_labels)

        paging.Size=MAX_GET_LABELS_BY_IDS
        get_labels_by_ids_response = campaign_service.GetLabelsByIds(
            label_ids,
            paging
        )
        output_array_of_label(get_labels_by_ids_response.Labels)
        
        campaign_label_associations = create_example_label_associations_by_entity_id(campaign_ids['long'][0], label_ids)
        output_status_message("Associating all of the labels with a campaign...\n")
        output_array_of_labelassociation(campaign_label_associations)
        set_label_associations_response = campaign_service.SetLabelAssociations('Campaign', campaign_label_associations)

        ad_group_label_associations = create_example_label_associations_by_entity_id(ad_group_ids['long'][0], label_ids)
        output_status_message("Associating all of the labels with an ad group...\n")
        output_array_of_labelassociation(ad_group_label_associations)
        set_label_associations_response = campaign_service.SetLabelAssociations('AdGroup', ad_group_label_associations)

        keyword_label_associations = create_example_label_associations_by_entity_id(keyword_ids['long'][0], label_ids)
        output_status_message("Associating all of the labels with a keyword...\n")
        output_array_of_labelassociation(keyword_label_associations)
        set_label_associations_response = campaign_service.SetLabelAssociations('Keyword', keyword_label_associations)

        ad_label_associations = create_example_label_associations_by_entity_id(ad_ids['long'][0], label_ids)
        output_status_message("Associating all of the labels with an ad...\n")
        output_array_of_labelassociation(ad_label_associations)
        set_label_associations_response = campaign_service.SetLabelAssociations('Ad', ad_label_associations)


        output_status_message("Use paging to get all campaign label associations...\n")
        get_label_associations_by_label_ids = get_label_associations_by_label_ids_helper(
            'Campaign',
            label_ids)
        output_array_of_labelassociation(get_label_associations_by_label_ids)

        output_status_message("Use paging to get all ad group label associations...\n")
        get_label_associations_by_label_ids = get_label_associations_by_label_ids_helper(
            'AdGroup',
            label_ids)
        output_array_of_labelassociation(get_label_associations_by_label_ids)

        output_status_message("Use paging to get all keyword label associations...\n")
        get_label_associations_by_label_ids = get_label_associations_by_label_ids_helper(
            'Keyword',
            label_ids)
        output_array_of_labelassociation(get_label_associations_by_label_ids)

        output_status_message("Use paging to get all ad label associations...\n")
        get_label_associations_by_label_ids = get_label_associations_by_label_ids_helper(
            'Ad',
            label_ids)
        output_array_of_labelassociation(get_label_associations_by_label_ids)

        output_status_message("Get all label associations for all specified campaigns...\n")
        get_label_associations_by_entity_ids = get_label_associations_by_entity_ids_helper(
            'Campaign',
            campaign_ids
        )
        output_array_of_labelassociation(get_label_associations_by_entity_ids)

        output_status_message("Get all label associations for all specified ad groups...\n")
        get_label_associations_by_entity_ids = get_label_associations_by_entity_ids_helper(
            'AdGroup',
            ad_group_ids
        )
        output_array_of_labelassociation(get_label_associations_by_entity_ids)

        output_status_message("Get all label associations for all specified keywords...\n")
        get_label_associations_by_entity_ids = get_label_associations_by_entity_ids_helper(
            'Keyword',
            keyword_ids
        )
        output_array_of_labelassociation(get_label_associations_by_entity_ids)

        output_status_message("Get all label associations for all specified ads...\n")
        get_label_associations_by_entity_ids = get_label_associations_by_entity_ids_helper(
            'Ad',
            ad_ids
        )
        output_array_of_labelassociation(get_label_associations_by_entity_ids)

        output_status_message("Delete all label associations that we set above....\n")

        # This is not necessary if you are deleting the corresponding campaign(s), as the 
        # contained ad groups, keywords, ads, and associations would also be deleted.

        deleteLabelAssociationsResponse = campaign_service.DeleteLabelAssociations('Campaign', campaign_label_associations)
        deleteLabelAssociationsResponse = campaign_service.DeleteLabelAssociations('AdGroup', ad_group_label_associations)
        deleteLabelAssociationsResponse = campaign_service.DeleteLabelAssociations('Keyword', keyword_label_associations)
        deleteLabelAssociationsResponse = campaign_service.DeleteLabelAssociations('Ad', ad_label_associations)

        output_status_message("Delete all labels that we added above....\n")

        # Deleting the campaign(s) removes the corresponding label associations but not remove the labels.

        delete_labels_response = campaign_service.DeleteLabels(label_ids)

        output_status_message("Delete the campaign, ad group, keyword, and ad that were added above....\n")

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

def create_example_label_associations_by_entity_id(entity_id, label_ids):
    label_associations = campaign_service.factory.create('ArrayOfLabelAssociation')
    for label_id in label_ids['long']:
        label_association = campaign_service.factory.create('LabelAssociation')
        label_association.EntityId = entity_id
        label_association.LabelId = label_id
        label_associations.LabelAssociation.append(label_association)

    return label_associations

def get_label_associations_by_label_ids_helper(entity_type, label_ids):
    label_associations = campaign_service.factory.create('ArrayOfLabelAssociation')
    label_ids_page_index = 0

    while (label_ids_page_index * MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS < len(label_ids['long'])):
        start_index = label_ids_page_index * MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS
        label_ids_page_index += 1
        get_label_ids = list(label_ids['long'][start_index : start_index + MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS])
        
        label_associations_page_index = 0
        found_last_page = False

        while (not found_last_page):
            paging=set_elements_to_none(campaign_service.factory.create('Paging'))
            paging.Index=label_associations_page_index
            label_associations_page_index += 1
            paging.Size=MAX_PAGING_SIZE
            get_label_associations_by_label_ids = campaign_service.GetLabelAssociationsByLabelIds(
                entity_type,
                {'long': get_label_ids},
                paging
            )

            label_associations.LabelAssociation.extend(get_label_associations_by_label_ids.LabelAssociations['LabelAssociation'])
            found_last_page = MAX_PAGING_SIZE > len(get_label_associations_by_label_ids.LabelAssociations['LabelAssociation'])

    return label_associations

def get_label_associations_by_entity_ids_helper(entity_type, entity_ids):
    label_associations = campaign_service.factory.create('ArrayOfLabelAssociation')
    entity_ids_page_index = 0

    while (entity_ids_page_index * MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS < len(entity_ids['long'])):
        start_index = entity_ids_page_index * MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS
        entity_ids_page_index += 1
        get_entity_ids = list(entity_ids['long'][start_index : start_index + MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS])

        get_label_associations_by_entity_ids = campaign_service.GetLabelAssociationsByEntityIds(
            {'long': get_entity_ids},
            entity_type
        )

        label_associations.LabelAssociation.extend(get_label_associations_by_entity_ids.LabelAssociations['LabelAssociation'])

    return label_associations

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
