import uuid
import random
from auth_helper import *
from openapi_client.models.campaign import *

# Constants for pagination
MAX_GET_LABELS_BY_IDS = 1000
MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS = 1
MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS = 100
MAX_PAGING_SIZE = 1000

def create_label_associations_by_entity_id(entity_id, label_ids):
    """
    Create label associations for a given entity ID and label IDs.
    
    Args:
        entity_id: The entity ID (campaign or ad group)
        label_ids: List of label IDs to associate
        
    Returns:
        List of LabelAssociation objects
    """
    label_associations = []
    for label_id in label_ids:
        association = LabelAssociation(
            entity_id=entity_id,
            label_id=label_id
        )
        label_associations.append(association)
    return label_associations

def get_label_associations_by_label_ids_helper(campaign_service, entity_type, label_ids):
    """
    Get all label associations by label IDs with pagination.
    
    Args:
        campaign_service: The campaign service client
        entity_type: The entity type (Campaign or AdGroup)
        label_ids: List of label IDs
    """
    print(f"Getting label associations by label IDs for {entity_type}...")
    
    label_associations = []
    label_ids_page_index = 0
    
    while label_ids_page_index * MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS < len(label_ids):
        get_label_ids = label_ids[
            label_ids_page_index * MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS:
            (label_ids_page_index + 1) * MAX_LABEL_IDS_FOR_GET_LABEL_ASSOCIATIONS
        ]
        label_ids_page_index += 1
        
        label_associations_page_index = 0
        found_last_page = False
        
        while not found_last_page:
            paging = Paging(
                index=label_associations_page_index,
                size=MAX_PAGING_SIZE
            )
            label_associations_page_index += 1
            
            get_associations_request = GetLabelAssociationsByLabelIdsRequest(
                entity_type=entity_type,
                label_ids=get_label_ids,
                page_info=paging
            )
            
            get_associations_response = campaign_service.get_label_associations_by_label_ids(
                get_label_associations_by_label_ids_request=get_associations_request
            )
            
            associations = get_associations_response.LabelAssociations
            if associations:
                label_associations.extend(associations)
                found_last_page = len(associations) < MAX_PAGING_SIZE
            else:
                found_last_page = True
    
    print(f"  Found {len(label_associations)} label associations")

def get_label_associations_by_entity_ids_helper(campaign_service, entity_type, entity_ids):
    """
    Get all label associations by entity IDs with pagination.
    
    Args:
        campaign_service: The campaign service client
        entity_type: The entity type (Campaign or AdGroup)
        entity_ids: List of entity IDs
    """
    print(f"Getting label associations by entity IDs for {entity_type}...")
    
    label_associations = []
    entity_ids_page_index = 0
    
    while entity_ids_page_index * MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS < len(entity_ids):
        get_entity_ids = entity_ids[
            entity_ids_page_index * MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS:
            (entity_ids_page_index + 1) * MAX_ENTITY_IDS_FOR_GET_LABEL_ASSOCIATIONS
        ]
        entity_ids_page_index += 1
        
        get_associations_request = GetLabelAssociationsByEntityIdsRequest(
            entity_type=entity_type,
            entity_ids=get_entity_ids
        )
        
        get_associations_response = campaign_service.get_label_associations_by_entity_ids(
            get_label_associations_by_entity_ids_request=get_associations_request
        )
        
        associations = get_associations_response.LabelAssociations
        if associations:
            label_associations.extend(associations)
    
    print(f"  Found {len(label_associations)} label associations")

def main(authorization_data):
    try:
        # Create a campaign
        print("Creating campaign...")
        
        campaign = Campaign(
            name="Women's Shoes " + str(uuid.uuid4()),
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50.00,
            languages=['All'],
            time_zone='PacificTimeUSCanadaTijuana'
        )
        
        add_campaigns_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=[campaign]
        )
        
        add_campaigns_response = campaign_service.add_campaigns(
            add_campaigns_request=add_campaigns_request
        )
        
        campaign_ids = add_campaigns_response.CampaignIds
        print(f"Created Campaign ID: {campaign_ids[0]}")
        
        # Create an ad group
        print("\nCreating ad group...")
        
        current_year = datetime.now().year
        
        ad_group = AdGroup(
            name="Ad Group Women's Red Shoe Sale" + str(uuid.uuid4())[:8],
            cpc_bid=Bid(amount=0.09),
            end_date=ModelDate(day=31, month=12, year=current_year)
        )
        
        add_ad_groups_request = AddAdGroupsRequest(
            campaign_id=campaign_ids[0],
            ad_groups=[ad_group]
        )
        
        add_ad_groups_response = campaign_service.add_ad_groups(
            add_ad_groups_request=add_ad_groups_request
        )
        
        ad_group_ids = add_ad_groups_response.AdGroupIds
        print(f"Created Ad Group ID: {ad_group_ids[0]}")
        
        # Create labels
        print("\nCreating labels...")
        
        labels = []
        for i in range(5):
            # Generate random color code
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            label = Label(
                color_code=color,
                description='Label Description',
                name=f'Label Name {color} {str(uuid.uuid4())[:8]}'
            )
            labels.append(label)
        
        add_labels_request = AddLabelsRequest(
            labels=labels
        )
        
        add_labels_response = campaign_service.add_labels(
            add_labels_request=add_labels_request
        )
        
        label_ids = add_labels_response.LabelIds
        print(f"Created Label IDs: {label_ids}")
        
        if add_labels_response.PartialErrors:
            print(f"Partial Errors: {add_labels_response.PartialErrors}")
        
        # Get labels by IDs
        print("\nGetting labels by IDs...")
        
        paging = Paging(
            index=0,
            size=MAX_GET_LABELS_BY_IDS
        )
        
        get_labels_request = GetLabelsByIdsRequest(
            label_ids=label_ids,
            page_info=paging
        )
        
        get_labels_response = campaign_service.get_labels_by_ids(
            get_labels_by_ids_request=get_labels_request
        )
        
        retrieved_labels = get_labels_response.Labels
        print(f"Retrieved {len(retrieved_labels)} labels")
        
        # Associate labels with campaign
        print("\nAssociating all labels with campaign...")
        
        campaign_label_associations = create_label_associations_by_entity_id(
            campaign_ids[0],
            label_ids
        )
        
        set_campaign_associations_request = SetLabelAssociationsRequest(
            entity_type=EntityType.CAMPAIGN,
            label_associations=campaign_label_associations
        )
        
        set_campaign_associations_response = campaign_service.set_label_associations(
            set_label_associations_request=set_campaign_associations_request
        )
        
        if set_campaign_associations_response.PartialErrors:
            print(f"Partial Errors: {set_campaign_associations_response.PartialErrors}")
        else:
            print("Campaign label associations set successfully")
        
        # Associate labels with ad group
        print("\nAssociating all labels with ad group...")
        
        ad_group_label_associations = create_label_associations_by_entity_id(
            ad_group_ids[0],
            label_ids
        )
        
        set_ad_group_associations_request = SetLabelAssociationsRequest(
            entity_type=EntityType.ADGROUP,
            label_associations=ad_group_label_associations
        )
        
        set_ad_group_associations_response = campaign_service.set_label_associations(
            set_label_associations_request=set_ad_group_associations_request
        )
        
        if set_ad_group_associations_response.PartialErrors:
            print(f"Partial Errors: {set_ad_group_associations_response.PartialErrors}")
        else:
            print("Ad group label associations set successfully")
        
        # Get label associations by label IDs for campaigns
        print("\nGetting campaign label associations by label IDs (with paging)...")
        get_label_associations_by_label_ids_helper(
            campaign_service,
            EntityType.CAMPAIGN,
            label_ids
        )
        
        # Get label associations by label IDs for ad groups
        print("\nGetting ad group label associations by label IDs (with paging)...")
        get_label_associations_by_label_ids_helper(
            campaign_service,
            EntityType.ADGROUP,
            label_ids
        )
        
        # Get label associations by entity IDs for campaigns
        print("\nGetting label associations by campaign entity IDs...")
        get_label_associations_by_entity_ids_helper(
            campaign_service,
            EntityType.CAMPAIGN,
            campaign_ids
        )
        
        # Get label associations by entity IDs for ad groups
        print("\nGetting label associations by ad group entity IDs...")
        get_label_associations_by_entity_ids_helper(
            campaign_service,
            EntityType.ADGROUP,
            ad_group_ids
        )
        
        # Delete label associations
        print("\nDeleting label associations...")
        
        # Delete campaign label associations
        delete_campaign_associations_request = DeleteLabelAssociationsRequest(
            entity_type=EntityType.CAMPAIGN,
            label_associations=campaign_label_associations
        )
        
        delete_campaign_associations_response = campaign_service.delete_label_associations(
            delete_label_associations_request=delete_campaign_associations_request
        )
        
        if delete_campaign_associations_response.PartialErrors:
            print(f"Campaign Partial Errors: {delete_campaign_associations_response.PartialErrors}")
        else:
            print("Campaign label associations deleted successfully")
        
        # Delete ad group label associations
        delete_ad_group_associations_request = DeleteLabelAssociationsRequest(
            entity_type=EntityType.ADGROUP,
            label_associations=ad_group_label_associations
        )
        
        delete_ad_group_associations_response = campaign_service.delete_label_associations(
            delete_label_associations_request=delete_ad_group_associations_request
        )
        
        if delete_ad_group_associations_response.PartialErrors:
            print(f"Ad Group Partial Errors: {delete_ad_group_associations_response.PartialErrors}")
        else:
            print("Ad group label associations deleted successfully")
        
        # Delete labels
        print("\nDeleting labels...")
        
        delete_labels_request = DeleteLabelsRequest(
            label_ids=label_ids
        )
        
        delete_labels_response = campaign_service.delete_labels(
            delete_labels_request=delete_labels_request
        )
        
        if delete_labels_response.PartialErrors:
            print(f"Partial Errors: {delete_labels_response.PartialErrors}")
        else:
            print(f"Deleted Label IDs: {label_ids}")
        
        # Delete campaign
        print("\nDeleting campaign...")
        
        delete_campaigns_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=campaign_ids
        )
        
        campaign_service.delete_campaigns(
            delete_campaigns_request=delete_campaigns_request
        )
        
        print(f"Deleted Campaign ID {campaign_ids[0]}")
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()

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