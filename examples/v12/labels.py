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
        # Add an ad group in a campaign. Later we will create labels for them. 
        # Although not included in this example you can also create labels for ads and keywords.
        
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

        # Add labels and associate them with the campaign and ad group.

        labels=campaign_service.factory.create('ArrayOfLabel')
        for index in range(5):
            color = "#{0:06x}".format(random.randint(0,100000))
            label=set_elements_to_none(campaign_service.factory.create('Label'))
            label.ColorCode = color
            label.Description = "Label Description"
            label.Name = "Label Name " + color + " " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            labels.Label.append(label)
               
        output_status_message("-----\nAddLabels:")
        add_labels_response=campaign_service.AddLabels(
            Labels=labels
        )
        label_ids={
            'long': add_labels_response.LabelIds['long'] if add_labels_response.LabelIds['long'] else None
        }
        output_status_message("LabelIds:")
        output_array_of_long(label_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_labels_response.PartialErrors)
                
        paging=set_elements_to_none(campaign_service.factory.create('Paging'))
        paging.Index=0
        paging.Size=10
        
        output_status_message("-----\nGetLabelsByIds:")
        get_labels_by_ids_response = campaign_service.GetLabelsByIds(
            LabelIds=label_ids,
            PageInfo=paging
        )
        output_status_message("Labels:")
        output_array_of_label(get_labels_by_ids_response.Labels)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_labels_response.PartialErrors)
                
        campaign_label_associations = create_example_label_associations_by_entity_id(campaign_ids['long'][0], label_ids)
        output_status_message("-----\nAssociating all of the labels with a campaign...")
        output_array_of_labelassociation(campaign_label_associations)
        set_label_associations_response=campaign_service.SetLabelAssociations(
            EntityType='Campaign', 
            LabelAssociations=campaign_label_associations)

        ad_group_label_associations = create_example_label_associations_by_entity_id(ad_group_ids['long'][0], label_ids)
        output_status_message("-----\nAssociating all of the labels with an ad group...")
        output_array_of_labelassociation(ad_group_label_associations)
        set_label_associations_response=campaign_service.SetLabelAssociations(
            EntityType='AdGroup', 
            LabelAssociations=ad_group_label_associations)

        output_status_message("-----\nUse paging to get all campaign label associations...")
        get_label_associations_by_label_ids = get_label_associations_by_label_ids_helper(
            entity_type='Campaign',
            label_ids=label_ids)
        output_array_of_labelassociation(get_label_associations_by_label_ids)

        output_status_message("-----\nUse paging to get all ad group label associations...")
        get_label_associations_by_label_ids = get_label_associations_by_label_ids_helper(
            entity_type='AdGroup',
            label_ids=label_ids)
        output_array_of_labelassociation(get_label_associations_by_label_ids)

        output_status_message("-----\nGet all label associations for the campaigns...")
        get_label_associations_by_entity_ids = get_label_associations_by_entity_ids_helper(
            entity_type='Campaign',
            entity_ids=campaign_ids
        )
        output_array_of_labelassociation(get_label_associations_by_entity_ids)

        output_status_message("-----\nGet all label associations for the ad groups...")
        get_label_associations_by_entity_ids = get_label_associations_by_entity_ids_helper(
            entity_type='AdGroup',
            entity_ids=ad_group_ids
        )
        output_array_of_labelassociation(get_label_associations_by_entity_ids)

        output_status_message("-----\nDelete all label associations that we set above...")

        # Deleting the associations is not necessary if you are deleting the corresponding campaign(s), as the 
        # contained ad groups, ads, and associations would also be deleted.

        deleteLabelAssociationsResponse = campaign_service.DeleteLabelAssociations(
            EntityType='Campaign', 
            LabelAssociations=campaign_label_associations)
        deleteLabelAssociationsResponse = campaign_service.DeleteLabelAssociations(
            EntityType='AdGroup', 
            LabelAssociations=ad_group_label_associations)

        # Deleting the campaign(s) removes the corresponding label associations but not remove the labels.

        output_status_message("-----\nDeleteLabels:")
        delete_labels_response = campaign_service.DeleteLabels(
            LabelIds=label_ids)

        for id in label_ids['long']:
            output_status_message("Deleted Label Id {0}".format(id))

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
                EntityType=entity_type,
                LabelIds={'long': get_label_ids},
                PageInfo=paging
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
            EntityIds={'long': get_entity_ids},
            EntityType=entity_type
        )

        label_associations.LabelAssociation.extend(get_label_associations_by_entity_ids.LabelAssociations['LabelAssociation'])

    return label_associations

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
